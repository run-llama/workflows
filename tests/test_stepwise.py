# SPDX-License-Identifier: MIT
# Copyright (c) 2025 LlamaIndex Inc.

import pytest

from workflows.decorators import step
from workflows.events import Event, StartEvent, StopEvent
from workflows.workflow import Context, Workflow


class DummyEvent(Event):
    pass


class IntermediateEvent1(Event):
    value: int


class IntermediateEvent2(Event):
    value: int


class StepWorkflow(Workflow):
    probe: str = ""

    @step
    async def step1(self, ctx: Context, ev: StartEvent) -> None:
        ctx.send_event(IntermediateEvent1(value=21))
        ctx.send_event(IntermediateEvent2(value=23))

    @step
    async def step2a(self, ev: IntermediateEvent1) -> StopEvent:
        return StopEvent(result=ev.value * 2)

    @step
    async def step2b(self, ev: IntermediateEvent2) -> None:
        self.probe = "test"


@pytest.mark.asyncio
async def test_simple_stepwise() -> None:
    workflow = StepWorkflow(disable_validation=True)
    handler = workflow.run(stepwise=True)
    while produced_events := await handler.run_step():
        for ev in produced_events:
            handler.ctx.send_event(ev)  # type: ignore

    result = await handler
    assert result == 42
    # Ensure step2b was executed before exiting the workflow
    assert workflow.probe == "test"
