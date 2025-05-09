import logging
from typing import AsyncIterable, Union, AsyncIterator

from llama_stack_client import Agent, AgentEventLogger

import common.server.utils as utils
from common.server.task_manager import InMemoryTaskManager
from common.types import (
    SendTaskRequest, SendTaskResponse,
    SendTaskStreamingRequest, SendTaskStreamingResponse,
    TaskStatus, Artifact,
    Message, TaskState,
    TaskStatusUpdateEvent, TaskArtifactUpdateEvent,
    JSONRPCResponse,
)

logger = logging.getLogger(__name__)

SUPPORTED_CONTENT_TYPES = ["text", "text/plain", "application/json"]


class AgentTaskManager(InMemoryTaskManager):
    def __init__(self, agent: Agent, internal_session_id=False):
        super().__init__()
        self.agent = agent
        if internal_session_id:
            self.session_id = self.agent.create_session("custom-agent-session")
        else:
            self.session_id = None

    def _validate_request(
        self, request: Union[SendTaskRequest, SendTaskStreamingRequest]
    ) -> JSONRPCResponse | None:
        params = request.params
        if not utils.are_modalities_compatible(
            params.acceptedOutputModes,
            SUPPORTED_CONTENT_TYPES
        ):
            logger.warning("Unsupported output modes: %s", params.acceptedOutputModes)
            return utils.new_incompatible_types_error(request.id)
        return None

    async def on_send_task(self, request: SendTaskRequest) -> SendTaskResponse:
        err = self._validate_request(request)
        if err:
            return err

        await self.upsert_task(request.params)
        result = self._invoke(
            request.params.message.parts[0].text,
            request.params.sessionId
        )
        parts = [{"type": "text", "text": result}]
        status = TaskStatus(state=TaskState.COMPLETED, message=Message(role="agent", parts=parts))
        task = await self._update_store(request.params.id, status, [Artifact(parts=parts)])
        return SendTaskResponse(id=request.id, result=task)

    async def on_send_task_subscribe(
        self, request: SendTaskStreamingRequest
    ) -> AsyncIterable[SendTaskStreamingResponse] | JSONRPCResponse:
        err = self._validate_request(request)
        if err:
            return err

        await self.upsert_task(request.params)
        return self._stream_generator(request)

    async def _stream_generator(
        self, request: SendTaskStreamingRequest
    ) -> AsyncIterable[SendTaskStreamingResponse]:
        params = request.params
        query = params.message.parts[0].text

        async for update in self._stream(query, params.sessionId):
            done = update["is_task_complete"]
            content = update["content"]
            delta = update["updates"]

            state = TaskState.COMPLETED if done else TaskState.WORKING
            text = content if done else delta
            parts = [{"type": "text", "text": text}]
            artifacts = [Artifact(parts=parts)] if done else None

            status = TaskStatus(state=state, message=Message(role="agent", parts=parts))
            await self._update_store(request.params.id, status, artifacts or [])

            yield SendTaskStreamingResponse(
                id=request.id,
                result=TaskStatusUpdateEvent(id=params.id, status=status, final=done)
            )
            if artifacts:
                yield SendTaskStreamingResponse(
                    id=request.id,
                    result=TaskArtifactUpdateEvent(id=params.id, artifact=artifacts[0])
                )

    async def _update_store(self, task_id: str, status: TaskStatus, artifacts):
        async with self.lock:
            task = self.tasks[task_id]
            task.status = status
            if artifacts:
                task.artifacts = (task.artifacts or []) + artifacts
            return task

    def _invoke(self, query: str, session_id: str) -> str:
        """
        Route the user query through the Agent, executing tools as needed.
        """
        # Determine which session to use
        if self.session_id is not None:
            sid = self.session_id
        else:
            sid = self.agent.create_session(session_id)

        # Send the user query to the Agent
        turn_resp = self.agent.create_turn(
            messages=[{"role": "user", "content": query}],
            session_id=sid,
        )

        # Extract tool and LLM outputs from events
        logs = AgentEventLogger().log(turn_resp)
        output = ""
        for event in logs:
            if hasattr(event, "content") and event.content:
                output += event.content
        return output

    async def _stream(self, query: str, session_id: str) -> AsyncIterator[dict]:
        """
        Simplest streaming stub: synchronously invoke and emit once.
        """
        result = self._invoke(query, session_id)
        yield {"updates": result, "is_task_complete": True, "content": result}
