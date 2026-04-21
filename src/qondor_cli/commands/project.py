"""qondor project — Project commands."""

from __future__ import annotations

from typing import Annotated

import typer
from qondor_api_sdk.models.project import CreateProject, SetAsFinished

from .._run import run_async

app = typer.Typer(no_args_is_help=True)


@app.command()
def get(
    id: Annotated[int, typer.Argument(help="Project ID")],
    subscription_key: Annotated[
        str | None, typer.Option("--subscription-key", "-k", envvar="QONDOR_SUBSCRIPTION_KEY")
    ] = None,
    env: Annotated[str | None, typer.Option("--env", "-e", envvar="QONDOR_ENV")] = None,
    raw: Annotated[bool, typer.Option("--raw", help="Compact JSON")] = False,
) -> None:
    """Get a project by ID."""
    run_async(lambda c: c.project.get(id), subscription_key=subscription_key, env=env, raw=raw)


@app.command("list")
def list_projects(
    office_id: Annotated[int | None, typer.Option("--office-id", help="Filter by office")] = None,
    subscription_key: Annotated[
        str | None, typer.Option("--subscription-key", "-k", envvar="QONDOR_SUBSCRIPTION_KEY")
    ] = None,
    env: Annotated[str | None, typer.Option("--env", "-e", envvar="QONDOR_ENV")] = None,
    raw: Annotated[bool, typer.Option("--raw", help="Compact JSON")] = False,
) -> None:
    """List projects."""
    run_async(lambda c: c.project.get_all(office_id=office_id), subscription_key=subscription_key, env=env, raw=raw)


@app.command()
def create(
    name: Annotated[str, typer.Option("--name", help="Project name (mandatory)")],
    office_id: Annotated[
        int | None, typer.Option("--office-id", help="Office ID (mandatory if you have multiple offices)")
    ] = None,
    customer_id: Annotated[
        int | None,
        typer.Option("--customer-id", help="Customer ID (or use --customer-external-reference/--customer-number)"),
    ] = None,
    pax: Annotated[int | None, typer.Option("--pax", help="Expected number of participants")] = None,
    start_date: Annotated[str | None, typer.Option("--start-date", help="Project start date")] = None,
    end_date: Annotated[str | None, typer.Option("--end-date", help="Project end date")] = None,
    location: Annotated[
        str | None, typer.Option("--location", help="Free-text location; auto-set from location-code if empty")
    ] = None,
    copy_from_project_no: Annotated[
        str | None,
        typer.Option("--copy-from-project-no", help="Project number to copy from (large projects may be slow)"),
    ] = None,
    project_no: Annotated[
        str | None, typer.Option("--project-no", help="Project number incl. prefix (omit if autonumbering is on)")
    ] = None,
    main_project_manager_id: Annotated[
        int | None,
        typer.Option("--main-project-manager-id", help="Project manager ID (or use --main-project-manager-user-name)"),
    ] = None,
    main_project_manager_user_name: Annotated[
        str | None,
        typer.Option(
            "--main-project-manager-user-name", help="Project manager username (or use --main-project-manager-id)"
        ),
    ] = None,
    customer_external_reference: Annotated[
        str | None,
        typer.Option(
            "--customer-external-reference", help="Customer external ref (or use --customer-id/--customer-number)"
        ),
    ] = None,
    customer_number: Annotated[
        str | None,
        typer.Option("--customer-number", help="Customer number (or use --customer-id/--customer-external-reference)"),
    ] = None,
    main_contact_person_id: Annotated[
        int | None, typer.Option("--main-contact-person-id", help="Contact person ID (or use email/external-reference)")
    ] = None,
    main_contact_person_email: Annotated[
        str | None,
        typer.Option("--main-contact-person-email", help="Contact person email (or use id/external-reference)"),
    ] = None,
    main_contact_person_external_reference: Annotated[
        str | None,
        typer.Option("--main-contact-person-external-reference", help="Contact person external ref (or use id/email)"),
    ] = None,
    team_id: Annotated[int | None, typer.Option("--team-id", help="Team ID (or use --team-external-reference)")] = None,
    team_external_reference: Annotated[
        str | None, typer.Option("--team-external-reference", help="Team external ref (or use --team-id)")
    ] = None,
    location_code: Annotated[str | None, typer.Option("--location-code", help="IATA airport code")] = None,
    budgeted_sales: Annotated[float | None, typer.Option("--budgeted-sales", help="Budgeted sales")] = None,
    budgeted_revenue: Annotated[float | None, typer.Option("--budgeted-revenue", help="Budgeted revenue")] = None,
    currency: Annotated[
        str | None, typer.Option("--currency", help="Three-letter ISO 4217 code; defaults to customer/office currency")
    ] = None,
    lead_from: Annotated[
        str | None, typer.Option("--lead-from", help="Lead from (must match a lead-from in the office)")
    ] = None,
    project_category: Annotated[
        str | None, typer.Option("--project-category", help="Project category (must match a category in the office)")
    ] = None,
    subscription_key: Annotated[
        str | None, typer.Option("--subscription-key", "-k", envvar="QONDOR_SUBSCRIPTION_KEY")
    ] = None,
    env: Annotated[str | None, typer.Option("--env", "-e", envvar="QONDOR_ENV")] = None,
    raw: Annotated[bool, typer.Option("--raw", help="Compact JSON")] = False,
) -> None:
    """Create a project."""
    req = CreateProject(
        name=name,
        office_id=office_id,
        customer_id=customer_id,
        pax=pax,
        start_date=start_date,
        end_date=end_date,
        location=location,
        copy_from_project_no=copy_from_project_no,
        project_no=project_no,
        main_project_manager_id=main_project_manager_id,
        main_project_manager_user_name=main_project_manager_user_name,
        customer_external_reference=customer_external_reference,
        customer_number=customer_number,
        main_contact_person_id=main_contact_person_id,
        main_contact_person_email=main_contact_person_email,
        main_contact_person_external_reference=main_contact_person_external_reference,
        team_id=team_id,
        team_external_reference=team_external_reference,
        location_code=location_code,
        budgeted_sales=budgeted_sales,
        budgeted_revenue=budgeted_revenue,
        currency=currency,
        lead_from=lead_from,
        project_category=project_category,
    )
    run_async(lambda c: c.project.create(req), subscription_key=subscription_key, env=env, raw=raw)


@app.command("get-by-project-no")
def get_by_project_no(
    project_no: Annotated[str, typer.Option("--project-no", help="Project number")],
    office_id: Annotated[
        int | None, typer.Option("--office-id", help="Office ID (needed if project-no is not globally unique)")
    ] = None,
    subscription_key: Annotated[
        str | None, typer.Option("--subscription-key", "-k", envvar="QONDOR_SUBSCRIPTION_KEY")
    ] = None,
    env: Annotated[str | None, typer.Option("--env", "-e", envvar="QONDOR_ENV")] = None,
    raw: Annotated[bool, typer.Option("--raw", help="Compact JSON")] = False,
) -> None:
    """Get a project by project number."""
    run_async(
        lambda c: c.project.get_by_project_no(project_no=project_no, office_id=office_id),
        subscription_key=subscription_key,
        env=env,
        raw=raw,
    )


@app.command("set-as-finished")
def set_as_finished(
    project_id: Annotated[int, typer.Option("--project-id", help="Project ID (or use --project-no)")],
    project_no: Annotated[str | None, typer.Option("--project-no", help="Project number (or use --project-id)")] = None,
    office_id: Annotated[
        int | None, typer.Option("--office-id", help="Office ID (mandatory when using --project-no)")
    ] = None,
    real_sales: Annotated[
        float | None, typer.Option("--real-sales", help="Real sales (mandatory if not set by project manager)")
    ] = None,
    real_revenue: Annotated[
        float | None, typer.Option("--real-revenue", help="Real revenue (mandatory if not set by project manager)")
    ] = None,
    subscription_key: Annotated[
        str | None, typer.Option("--subscription-key", "-k", envvar="QONDOR_SUBSCRIPTION_KEY")
    ] = None,
    env: Annotated[str | None, typer.Option("--env", "-e", envvar="QONDOR_ENV")] = None,
    raw: Annotated[bool, typer.Option("--raw", help="Compact JSON")] = False,
) -> None:
    """Set a project as finished."""
    req = SetAsFinished(
        project_id=project_id,
        project_no=project_no,
        office_id=office_id,
        real_sales=real_sales,
        real_revenue=real_revenue,
    )
    run_async(lambda c: c.project.set_as_finished(req), subscription_key=subscription_key, env=env, raw=raw)
