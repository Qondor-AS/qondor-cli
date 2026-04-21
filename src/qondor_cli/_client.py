"""Build a QondorClient from CLI config."""

from __future__ import annotations

from collections.abc import AsyncIterator
from contextlib import asynccontextmanager

from qondor_api_sdk.client import QondorClient

from ._config import Config


@asynccontextmanager
async def build_client(config: Config) -> AsyncIterator[QondorClient]:
    client = QondorClient(
        base_url=config.base_url,
        subscription_key=config.subscription_key,
    )
    try:
        yield client
    finally:
        await client.close()
