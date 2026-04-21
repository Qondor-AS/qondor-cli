"""Shared async runner for CLI commands."""

from __future__ import annotations

import asyncio
import sys
from typing import Any

from ._client import build_client
from ._config import resolve_config
from ._output import format_output


def run_async(
    coro_factory: Any,
    *,
    subscription_key: str | None = None,
    env: str | None = None,
    raw: bool = False,
) -> None:
    """Resolve config, build client, run an async SDK call, print result."""
    config = resolve_config(subscription_key=subscription_key, env=env)

    async def _run() -> None:
        async with build_client(config) as client:
            result = await coro_factory(client)
            output = format_output(result, raw=raw)
            if output:
                print(output)

    try:
        asyncio.run(_run())
    except SystemExit:
        raise
    except Exception as exc:
        print(f"Error: {exc}", file=sys.stderr)
        raise SystemExit(1)
