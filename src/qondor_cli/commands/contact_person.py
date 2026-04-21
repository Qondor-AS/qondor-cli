"""qondor contact-person — Contact person commands."""

from __future__ import annotations

from typing import Annotated

import typer
from qondor_api_sdk.models.contact_person import (
    CreateContactPerson,
    UpdateContactPerson,
    UpdateContactPersonCustomer,
    UpdateContactPersonSupplier,
)

from .._run import run_async

app = typer.Typer(no_args_is_help=True)


@app.command()
def get(
    id: Annotated[int, typer.Argument(help="Contact person ID")],
    subscription_key: Annotated[
        str | None, typer.Option("--subscription-key", "-k", envvar="QONDOR_SUBSCRIPTION_KEY")
    ] = None,
    env: Annotated[str | None, typer.Option("--env", "-e", envvar="QONDOR_ENV")] = None,
    raw: Annotated[bool, typer.Option("--raw", help="Compact JSON")] = False,
) -> None:
    """Get a contact person by ID."""
    run_async(lambda c: c.contact_person.get(id), subscription_key=subscription_key, env=env, raw=raw)


@app.command()
def create(
    first_name: Annotated[str | None, typer.Option("--first-name", help="First name")] = None,
    last_name: Annotated[str | None, typer.Option("--last-name", help="Last name")] = None,
    email: Annotated[str | None, typer.Option("--email", help="Email address")] = None,
    phone_number: Annotated[str | None, typer.Option("--phone-number", help="Phone number")] = None,
    external_reference: Annotated[
        str | None, typer.Option("--external-reference", help="Your unique external reference")
    ] = None,
    phone_country_code: Annotated[
        str | None, typer.Option("--phone-country-code", help="Country code for phone number")
    ] = None,
    phone_country_code2: Annotated[
        str | None, typer.Option("--phone-country-code2", help="Country code for second phone number")
    ] = None,
    phone_number2: Annotated[str | None, typer.Option("--phone-number2", help="Second phone number")] = None,
    subscription_key: Annotated[
        str | None, typer.Option("--subscription-key", "-k", envvar="QONDOR_SUBSCRIPTION_KEY")
    ] = None,
    env: Annotated[str | None, typer.Option("--env", "-e", envvar="QONDOR_ENV")] = None,
    raw: Annotated[bool, typer.Option("--raw", help="Compact JSON")] = False,
) -> None:
    """Create a contact person."""
    req = CreateContactPerson(
        first_name=first_name,
        last_name=last_name,
        email=email,
        phone_number=phone_number,
        external_reference=external_reference,
        phone_country_code=phone_country_code,
        phone_country_code2=phone_country_code2,
        phone_number2=phone_number2,
    )
    run_async(lambda c: c.contact_person.create(req), subscription_key=subscription_key, env=env, raw=raw)


@app.command()
def update(
    id: Annotated[int, typer.Option("--id", help="Contact person ID")],
    first_name: Annotated[str | None, typer.Option("--first-name", help="First name")] = None,
    last_name: Annotated[str | None, typer.Option("--last-name", help="Last name")] = None,
    email: Annotated[str | None, typer.Option("--email", help="Email address")] = None,
    phone_number: Annotated[str | None, typer.Option("--phone-number", help="Phone number")] = None,
    external_reference: Annotated[
        str | None, typer.Option("--external-reference", help="Your unique external reference")
    ] = None,
    phone_country_code: Annotated[
        str | None, typer.Option("--phone-country-code", help="Country code for phone number")
    ] = None,
    phone_country_code2: Annotated[
        str | None, typer.Option("--phone-country-code2", help="Country code for second phone number")
    ] = None,
    phone_number2: Annotated[str | None, typer.Option("--phone-number2", help="Second phone number")] = None,
    subscription_key: Annotated[
        str | None, typer.Option("--subscription-key", "-k", envvar="QONDOR_SUBSCRIPTION_KEY")
    ] = None,
    env: Annotated[str | None, typer.Option("--env", "-e", envvar="QONDOR_ENV")] = None,
    raw: Annotated[bool, typer.Option("--raw", help="Compact JSON")] = False,
) -> None:
    """Update a contact person."""
    req = UpdateContactPerson(
        id=id,
        first_name=first_name,
        last_name=last_name,
        email=email,
        phone_number=phone_number,
        external_reference=external_reference,
        phone_country_code=phone_country_code,
        phone_country_code2=phone_country_code2,
        phone_number2=phone_number2,
    )
    run_async(lambda c: c.contact_person.update(req), subscription_key=subscription_key, env=env, raw=raw)


@app.command()
def delete(
    id: Annotated[int, typer.Argument(help="Contact person ID")],
    subscription_key: Annotated[
        str | None, typer.Option("--subscription-key", "-k", envvar="QONDOR_SUBSCRIPTION_KEY")
    ] = None,
    env: Annotated[str | None, typer.Option("--env", "-e", envvar="QONDOR_ENV")] = None,
    raw: Annotated[bool, typer.Option("--raw", help="Compact JSON")] = False,
) -> None:
    """Delete a contact person by ID."""
    run_async(lambda c: c.contact_person.delete(id), subscription_key=subscription_key, env=env, raw=raw)


@app.command("get-by-email")
def get_by_email(
    email: Annotated[str, typer.Option("--email", help="Email address")],
    subscription_key: Annotated[
        str | None, typer.Option("--subscription-key", "-k", envvar="QONDOR_SUBSCRIPTION_KEY")
    ] = None,
    env: Annotated[str | None, typer.Option("--env", "-e", envvar="QONDOR_ENV")] = None,
    raw: Annotated[bool, typer.Option("--raw", help="Compact JSON")] = False,
) -> None:
    """Get a contact person by email."""
    run_async(lambda c: c.contact_person.get_by_email(email=email), subscription_key=subscription_key, env=env, raw=raw)


@app.command("get-by-ref")
def get_by_ref(
    external_reference: Annotated[str, typer.Option("--external-reference", help="External reference")],
    subscription_key: Annotated[
        str | None, typer.Option("--subscription-key", "-k", envvar="QONDOR_SUBSCRIPTION_KEY")
    ] = None,
    env: Annotated[str | None, typer.Option("--env", "-e", envvar="QONDOR_ENV")] = None,
    raw: Annotated[bool, typer.Option("--raw", help="Compact JSON")] = False,
) -> None:
    """Get a contact person by external reference."""
    run_async(
        lambda c: c.contact_person.get_by_external_reference(external_reference=external_reference),
        subscription_key=subscription_key,
        env=env,
        raw=raw,
    )


@app.command("delete-by-email")
def delete_by_email(
    email: Annotated[str, typer.Option("--email", help="Email address")],
    subscription_key: Annotated[
        str | None, typer.Option("--subscription-key", "-k", envvar="QONDOR_SUBSCRIPTION_KEY")
    ] = None,
    env: Annotated[str | None, typer.Option("--env", "-e", envvar="QONDOR_ENV")] = None,
    raw: Annotated[bool, typer.Option("--raw", help="Compact JSON")] = False,
) -> None:
    """Delete a contact person by email."""
    run_async(
        lambda c: c.contact_person.delete_by_email(email=email), subscription_key=subscription_key, env=env, raw=raw
    )


@app.command("delete-by-ref")
def delete_by_ref(
    external_reference: Annotated[str, typer.Option("--external-reference", help="External reference")],
    subscription_key: Annotated[
        str | None, typer.Option("--subscription-key", "-k", envvar="QONDOR_SUBSCRIPTION_KEY")
    ] = None,
    env: Annotated[str | None, typer.Option("--env", "-e", envvar="QONDOR_ENV")] = None,
    raw: Annotated[bool, typer.Option("--raw", help="Compact JSON")] = False,
) -> None:
    """Delete a contact person by external reference."""
    run_async(
        lambda c: c.contact_person.delete_by_external_reference(external_reference=external_reference),
        subscription_key=subscription_key,
        env=env,
        raw=raw,
    )


@app.command("update-customer-relation")
def update_customer_relation(
    contact_person_id: Annotated[
        int | None, typer.Option("--contact-person-id", help="Contact person ID (or use email/external-reference)")
    ] = None,
    contact_person_email: Annotated[
        str | None, typer.Option("--contact-person-email", help="Contact person email (used if id not supplied)")
    ] = None,
    contact_person_external_reference: Annotated[
        str | None,
        typer.Option(
            "--contact-person-external-reference",
            help="Contact person external ref (used if id and email not supplied)",
        ),
    ] = None,
    customer_id: Annotated[
        int | None, typer.Option("--customer-id", help="Customer ID (or use --customer-external-reference)")
    ] = None,
    customer_external_reference: Annotated[
        str | None,
        typer.Option("--customer-external-reference", help="Customer external ref (used if id not supplied)"),
    ] = None,
    is_active: Annotated[
        bool | None, typer.Option("--is-active/--no-is-active", help="Whether the relation is active")
    ] = None,
    delete_relation: Annotated[
        bool | None, typer.Option("--delete-relation/--no-delete-relation", help="Delete the relation")
    ] = None,
    subscription_key: Annotated[
        str | None, typer.Option("--subscription-key", "-k", envvar="QONDOR_SUBSCRIPTION_KEY")
    ] = None,
    env: Annotated[str | None, typer.Option("--env", "-e", envvar="QONDOR_ENV")] = None,
    raw: Annotated[bool, typer.Option("--raw", help="Compact JSON")] = False,
) -> None:
    """Update a contact person's customer relation."""
    req = UpdateContactPersonCustomer(
        contact_person_id=contact_person_id,
        contact_person_email=contact_person_email,
        contact_person_external_reference=contact_person_external_reference,
        customer_id=customer_id,
        customer_external_reference=customer_external_reference,
        is_active=is_active,
        delete_relation=delete_relation,
    )
    run_async(
        lambda c: c.contact_person.update_customer_relation(req), subscription_key=subscription_key, env=env, raw=raw
    )


@app.command("update-supplier-relation")
def update_supplier_relation(
    contact_person_id: Annotated[
        int | None, typer.Option("--contact-person-id", help="Contact person ID (or use email/external-reference)")
    ] = None,
    contact_person_email: Annotated[
        str | None, typer.Option("--contact-person-email", help="Contact person email (used if id not supplied)")
    ] = None,
    contact_person_external_reference: Annotated[
        str | None,
        typer.Option(
            "--contact-person-external-reference",
            help="Contact person external ref (used if id and email not supplied)",
        ),
    ] = None,
    supplier_id: Annotated[
        int | None, typer.Option("--supplier-id", help="Supplier ID (or use --supplier-external-reference)")
    ] = None,
    supplier_external_reference: Annotated[
        str | None,
        typer.Option("--supplier-external-reference", help="Supplier external ref (used if id not supplied)"),
    ] = None,
    is_active: Annotated[
        bool | None, typer.Option("--is-active/--no-is-active", help="Whether the relation is active")
    ] = None,
    delete_relation: Annotated[
        bool | None, typer.Option("--delete-relation/--no-delete-relation", help="Delete the relation")
    ] = None,
    subscription_key: Annotated[
        str | None, typer.Option("--subscription-key", "-k", envvar="QONDOR_SUBSCRIPTION_KEY")
    ] = None,
    env: Annotated[str | None, typer.Option("--env", "-e", envvar="QONDOR_ENV")] = None,
    raw: Annotated[bool, typer.Option("--raw", help="Compact JSON")] = False,
) -> None:
    """Update a contact person's supplier relation."""
    req = UpdateContactPersonSupplier(
        contact_person_id=contact_person_id,
        contact_person_email=contact_person_email,
        contact_person_external_reference=contact_person_external_reference,
        supplier_id=supplier_id,
        supplier_external_reference=supplier_external_reference,
        is_active=is_active,
        delete_relation=delete_relation,
    )
    run_async(
        lambda c: c.contact_person.update_supplier_relation(req), subscription_key=subscription_key, env=env, raw=raw
    )
