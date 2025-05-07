import logging
from typing import AsyncIterable, Union
import common.server.utils as utils
from common.server.task_manager import InMemoryTaskManager
from common.types import (
    SendTaskRequest, SendTaskResponse,
    SendTaskStreamingRequest, SendTaskStreamingResponse,
    TaskSendParams, TaskStatus, Artifact,
    Message, TaskState,
    TaskStatusUpdateEvent, TaskArtifactUpdateEvent,
    JSONRPCResponse,
)
from .agent import MyCustomAgent

logger = logging.getLogger(__name__)

class AgentTaskManager(InMemoryTaskManager):
    def __init__(self, agent: MyCustomAgent):
        super().__init__()
        self.agent = agent

    def _validate_request(
        self, request: Union[SendTaskRequest, SendTaskStreamingRequest]
    ) -> JSONRPCResponse | None:
        params = request.params
        if not utils.are_modalities_compatible(
            params.acceptedOutputModes,
            MyCustomAgent.SUPPORTED_CONTENT_TYPES
        ):
            logger.warning("Unsupported output modes: %s", params.acceptedOutputModes)
            return utils.new_incompatible_types_error(request.id)
        return None

    async def on_send_task(self, request: SendTaskRequest) -> SendTaskResponse:
        err = self._validate_request(request)
        if err:
            return err

        await self.upsert_task(request.params)
        result = self.agent.invoke(
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

        async for update in self.agent.stream(query, params.sessionId):
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
