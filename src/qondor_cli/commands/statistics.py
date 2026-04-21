"""qondor statistics — Statistics commands."""

from __future__ import annotations

from typing import Annotated

import typer

from .._run import run_async

app = typer.Typer(no_args_is_help=True)


@app.command("offer-sales")
def offer_sales(
    office_id: Annotated[int | None, typer.Option("--office-id", help="Filter by office")] = None,
    project_id: Annotated[int | None, typer.Option("--project-id", help="Filter by project")] = None,
    subscription_key: Annotated[
        str | None, typer.Option("--subscription-key", "-k", envvar="QONDOR_SUBSCRIPTION_KEY")
    ] = None,
    env: Annotated[str | None, typer.Option("--env", "-e", envvar="QONDOR_ENV")] = None,
    raw: Annotated[bool, typer.Option("--raw", help="Compact JSON")] = False,
) -> None:
    """Get offer sales statistics."""
    run_async(
        lambda c: c.statistics.get_offer_sales(office_id=office_id, project_id=project_id),
        subscription_key=subscription_key,
        env=env,
        raw=raw,
    )
