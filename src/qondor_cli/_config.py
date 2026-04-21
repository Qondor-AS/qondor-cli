"""CLI configuration: subscription key and environment."""

from __future__ import annotations

import os
import sys
from dataclasses import dataclass

_ENV_URLS = {
    "prod": "https://qondor.azure-api.net/Prod",
    "test": "https://qondor.azure-api.net/Test",
    "dev": "https://qondor.azure-api.net/Dev",
}


@dataclass(frozen=True)
class Config:
    subscription_key: str
    env: str = "prod"

    @property
    def base_url(self) -> str:
        return _ENV_URLS[self.env]


def resolve_config(
    subscription_key: str | None,
    env: str | None,
) -> Config:
    """Resolve config from flags → env vars → defaults."""
    key = subscription_key or os.environ.get("QONDOR_SUBSCRIPTION_KEY")
    if not key:
        print("Error: --subscription-key or QONDOR_SUBSCRIPTION_KEY is required.", file=sys.stderr)
        raise SystemExit(2)

    environment = env or os.environ.get("QONDOR_ENV", "prod")
    return Config(subscription_key=key, env=environment)
