"""qondor office — Office commands."""

from __future__ import annotations

from typing import Annotated

import typer

from .._run import run_async

app = typer.Typer(no_args_is_help=True)


@app.command("list")
def list_offices(
    subscription_key: Annotated[
        str | None, typer.Option("--subscription-key", "-k", envvar="QONDOR_SUBSCRIPTION_KEY")
    ] = None,
    env: Annotated[str | None, typer.Option("--env", "-e", envvar="QONDOR_ENV")] = None,
    raw: Annotated[bool, typer.Option("--raw", help="Compact JSON")] = False,
) -> None:
    """List all offices."""
    run_async(lambda c: c.office.get_all(), subscription_key=subscription_key, env=env, raw=raw)


@app.command("categories")
def categories(
    office_id: Annotated[int, typer.Option("--office-id", help="Office to list categories for")],
    subscription_key: Annotated[
        str | None, typer.Option("--subscription-key", "-k", envvar="QONDOR_SUBSCRIPTION_KEY")
    ] = None,
    env: Annotated[str | None, typer.Option("--env", "-e", envvar="QONDOR_ENV")] = None,
    raw: Annotated[bool, typer.Option("--raw", help="Compact JSON")] = False,
) -> None:
    """List customer categories for an office."""
    run_async(
        lambda c: c.office.get_all_customer_categories(office_id=office_id),
        subscription_key=subscription_key,
        env=env,
        raw=raw,
    )
