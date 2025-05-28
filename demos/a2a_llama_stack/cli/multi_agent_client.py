#!/usr/bin/env python3
import asyncio
import json
import logging
import urllib.parse
from uuid import uuid4
from typing import Tuple, Dict, Any, Optional, List

import asyncclick as click

from common.client import A2AClient, A2ACardResolver
from hosts.cli.push_notification_listener import PushNotificationListener
from common.utils.push_notification_auth import PushNotificationReceiverAuth

logging.basicConfig(level=logging.INFO, format="%(asctime)s %(levelname)s %(name)s: %(message)s")
logger = logging.getLogger(__name__)

AgentInfo = Tuple[str, Any, A2AClient, str]

def _build_skill_meta(agent_manager: 'AgentManager') -> List[Dict[str, Any]]:
    unique_skills: Dict[str, Dict[str, Any]] = {}
    if agent_manager.skills:
        for _, card_obj, _, _ in agent_manager.skills.values():
            if hasattr(card_obj, 'skills') and isinstance(card_obj.skills, list):
                for s in card_obj.skills:
                    if s.id not in unique_skills:
                        unique_skills[s.id] = {
                            "skill_id": s.id,
                            "name": s.name,
                            "description": getattr(s, "description", None),
                            "tags": getattr(s, "tags", []),
                            "examples": getattr(s, "examples", None),
                        }
    return list(unique_skills.values())

class AgentManager:
    def __init__(self, urls: List[str]):
        if not urls:
            raise ValueError("URLs list cannot be empty for AgentManager")

        self.orchestrator: AgentInfo = self._make_agent_info(urls[0])

        self.skills: Dict[str, AgentInfo] = {}
        if len(urls) > 1:
            for skill_agent_url in urls[1:]:
                agent_info_tuple = self._make_agent_info(skill_agent_url)
                agent_card = agent_info_tuple[1]
                if hasattr(agent_card, 'skills') and isinstance(agent_card.skills, list):
                    for skill_item in agent_card.skills:
                        self.skills[skill_item.id] = agent_info_tuple

    @staticmethod
    def _make_agent_info(url: str) -> AgentInfo:
        card: Any = A2ACardResolver(url).get_agent_card()
        client = A2AClient(agent_card=card)
        session_id = uuid4().hex
        return url, card, client, session_id

async def _send_payload(client: A2AClient, card: Any, session_id: str, payload: Dict[str, Any], streaming: bool) -> str:
    response_text = ""
    if streaming:
        async for ev in client.send_task_streaming(payload):
            part = ev.result.status.message.parts[0].text or ""
            print(part, end="", flush=True)
            response_text = part
        print()
    else:
        res = await client.send_task(payload)
        response_text = res.result.status.message.parts[0].text.strip()
    return response_text

async def _send_task_to_agent(
    client: A2AClient,
    card: Any,
    session_id: str,
    input_text: str,
    push_enabled: bool,
    push_host: Optional[str],
    push_port: Optional[int]
) -> str:
    payload: Dict[str, Any] = {
        "id": uuid4().hex,
        "sessionId": session_id,
        "acceptedOutputModes": card.defaultOutputModes,
        "message": {"role": "user", "parts": [{"type": "text", "text": input_text}]},
    }

    if push_enabled and push_host and push_port:
        push_url = urllib.parse.urljoin(f"http://{push_host}:{push_port}", "/notify")
        schemes = getattr(card.authentication, "supportedSchemes", ["bearer"])
        payload["pushNotification"] = {
            "url": push_url,
            "authentication": {"schemes": schemes},
        }

    streaming_capability = getattr(getattr(card, "capabilities", object()), "streaming", False)
    return await _send_payload(client, card, session_id, payload, streaming_capability)

@click.command(context_settings={"help_option_names": ["-h", "--help"]})
@click.version_option(version="1.0.0")
@click.option("--agent", "cli_urls", multiple=True, required=True, help="Orchestrator + executor URLs.")
@click.option("--history/--no-history", "cli_history", default=False, help="Show history after each step.")
@click.option("--use-push-notifications/--no-push-notifications", "cli_use_push_notifications", default=False)
@click.option("--push-notification-receiver", "cli_push_notification_receiver", default="http://localhost:5000", show_default=True)
async def cli(cli_urls: List[str], cli_history: bool, cli_use_push_notifications: bool, cli_push_notification_receiver: str):
    if len(cli_urls) < 2:
        click.secho("Error: Provide at least orchestrator + executor URLs.", fg="red", err=True)
        raise click.Abort()

    push_host_val: Optional[str] = None
    push_port_val: Optional[int] = None
    if cli_use_push_notifications:
        parsed_url = urllib.parse.urlparse(cli_push_notification_receiver)
        push_host_val, push_port_val = parsed_url.hostname, parsed_url.port
        if not push_host_val or not push_port_val:
            click.secho(f"Error: Invalid push notification receiver URL: {cli_push_notification_receiver}", fg="red", err=True)
            raise click.Abort()
        auth_handler = PushNotificationReceiverAuth()
        orchestrator_jwks_url = f"{cli_urls[0]}/.well-known/jwks.json"
        try:
            await auth_handler.load_jwks(orchestrator_jwks_url)
        except Exception as e:
            click.secho(f"Error loading JWKS for push notifications from {orchestrator_jwks_url}: {e}", fg="red", err=True)
            raise click.Abort()

        PushNotificationListener(host=push_host_val, port=push_port_val, notification_receiver_auth=auth_handler).start()
        click.secho(f"Push notification listener started at http://{push_host_val}:{push_port_val}/notify", fg="blue")

    agent_manager = AgentManager(cli_urls)

    orch_url, orch_card, orch_client, orch_session_id = agent_manager.orchestrator

    click.secho("\n=========== 🛰️ Connected Agents ===========", fg="cyan")
    click.echo(f"Orchestrator: {orch_url} ({orch_card.name})")
    if agent_manager.skills:
        click.echo("Executors:")
        for skill_id, (skill_agent_url, skill_agent_card, _, _) in agent_manager.skills.items():
            click.echo(f"  • {skill_id} -> {skill_agent_url} ({skill_agent_card.name})")
    else:
        click.echo("No skill executors configured.")
    click.secho("========================================", fg="cyan")

    skills_meta = _build_skill_meta(agent_manager)

    while True:
        try:
            question = await asyncio.to_thread(click.prompt, "💬 Your question (:q to quit)", default="", type=str)
        except RuntimeError:
            question = click.prompt("💬 Your question (:q to quit)", default="", type=str)

        if question.strip().lower() in {":q", "quit"}:
            click.secho("Goodbye! 👋", fg="green")
            break
        if not question.strip():
            continue

        _call_agent_lambda = lambda current_client, current_card, current_session_id, text_input: _send_task_to_agent(
            current_client, current_card, current_session_id, text_input, cli_use_push_notifications, push_host_val, push_port_val
        )

        click.secho("\n=========== 🧠 Planning Phase ===========", fg="yellow")

        plan_instructions = (
            "You are an orchestration assistant.\n"
            "Available skills (id & name & description & tags & examples):\n"
            f"{json.dumps(skills_meta, indent=2)}\n\n"
            "When given a user question, respond _only_ with a JSON array of objects, "
            "each with key `skill_id`, without any surrounding object. You may be asked to write single or multiple skills.\n"
            "For example for multiple tools:\n"
            "[\n"
            "  {\"skill_id\": \"tool_1\"},\n"
            "  {\"skill_id\": \"tool_2\"}\n"
            "]"
        )
        combined_planner_input = plan_instructions + "\n\nUser question: " + question

        raw_plan = await _call_agent_lambda(orch_client, orch_card, orch_session_id, combined_planner_input)
        click.echo(f"Raw plan ➡️ {raw_plan}")

        plan = []
        try:
            plan = json.loads(raw_plan[: raw_plan.rfind("]") + 1])
        except Exception as e:
            click.secho(f"Plan parse failed: {e}. Attempting to fix...", fg="red")
            fix_json_input = "fix this json to be valid: " + raw_plan
            fixed_plan_json = await _call_agent_lambda(orch_client, orch_card, orch_session_id, fix_json_input)
            try:
                plan = json.loads(fixed_plan_json)
                click.secho(f"\nFixed Raw plan ➡️ {json.dumps(plan, indent=2)}\n", fg="green")
            except Exception as fix_e:
                click.secho(f"Failed to fix and parse plan: {fix_e}. Skipping execution.", fg="red", err=True)
                continue

        if not isinstance(plan, list) or not all(isinstance(item, dict) and 'skill_id' in item for item in plan):
            click.secho(f"Parsed plan is not a valid list of skill tasks: {plan}. Skipping execution.", fg="red", err=True)
            continue

        click.secho(f"\nFinal plan ➡️ {json.dumps(plan, indent=2)}", fg="green")

        click.secho("\n=========== ⚡️ Execution Phase ===========", fg="yellow")
        execution_results = []
        for i, step_details in enumerate(plan, 1):
            skill_id_to_execute = step_details.get("skill_id")
            skill_input_params_json = json.dumps(step_details.get("input", {}))
            skill_invocation_text = f"{skill_id_to_execute}({skill_input_params_json})"

            click.echo(f"➡️ Step {i}: {skill_invocation_text}")

            skill_agent_info_tuple = agent_manager.skills.get(skill_id_to_execute)

            if not skill_agent_info_tuple:
                click.secho(f"No executor for '{skill_id_to_execute}', skipping.", fg="red")
                execution_results.append({"skill_id": skill_id_to_execute, "output": None, "error": "Skill agent not found"})
                continue

            _, skill_card, skill_client, skill_session_id = skill_agent_info_tuple

            skill_output = await _call_agent_lambda(skill_client, skill_card, skill_session_id, skill_invocation_text)
            click.secho(f"   ✅ → {skill_output}", fg="green")
            execution_results.append({"skill_id": skill_id_to_execute, "output": skill_output})

        click.secho("\n=========== 🛠️ Composing Answer ===========", fg="yellow")

        composition_prompt = (
            f"Using the following information: {json.dumps(execution_results)}, write a clear and human-friendly response to the question: '{question}'. "
            "Keep it concise and easy to understand and respond like a human with character. Only use the information provided in the Response: \n"
            "If you cannot answer the question, say 'I don't know'. \n"
            "Never show any code or JSON, just the answer.\n\n"
        )

        final_answer = await _call_agent_lambda(orch_client, orch_card, orch_session_id, composition_prompt)
        click.secho("\n🎉 FINAL ANSWER", fg="cyan")
        click.echo(final_answer)
        click.secho("====================================", fg="cyan")

if __name__ == "__main__":
    asyncio.run(cli())
