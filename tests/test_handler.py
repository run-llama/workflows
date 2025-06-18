# SPDX-License-Identifier: MIT
# Copyright (c) 2025 LlamaIndex Inc.

from unittest import mock

import pytest

from workflows.context import Context
from workflows.handler import WorkflowHandler


def test_str() -> None:
    h = WorkflowHandler()
    h.set_result([])
    assert str(h) == "[]"


@pytest.mark.asyncio
async def test_stream_no_context() -> None:
    h = WorkflowHandler()
    with pytest.raises(ValueError, match="Context is not set!"):
        async for ev in h.stream_events():
            pass


@pytest.mark.asyncio
async def test_run_step_no_context() -> None:
    h = WorkflowHandler()
    with pytest.raises(
        ValueError,
        match="Context must be set to run a workflow step-wise!",
    ):
        await h.run_step()


@pytest.mark.asyncio
async def test_run_step_no_stepwise() -> None:
    ctx = mock.MagicMock(spec=Context, stepwise=False)
    h = WorkflowHandler(ctx=ctx)
    with pytest.raises(
        ValueError,
        match="Workflow must be created passing stepwise=True to call this method.",
    ):
        await h.run_step()
