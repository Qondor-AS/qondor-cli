"""qondor supplier — Supplier commands."""

from __future__ import annotations

from typing import Annotated

import typer
from qondor_api_sdk.models.supplier import CreateSupplier, UpdateSupplier

from .._run import run_async

app = typer.Typer(no_args_is_help=True)


@app.command()
def get(
    id: Annotated[int, typer.Argument(help="Supplier ID")],
    subscription_key: Annotated[
        str | None, typer.Option("--subscription-key", "-k", envvar="QONDOR_SUBSCRIPTION_KEY")
    ] = None,
    env: Annotated[str | None, typer.Option("--env", "-e", envvar="QONDOR_ENV")] = None,
    raw: Annotated[bool, typer.Option("--raw", help="Compact JSON")] = False,
) -> None:
    """Get a supplier by ID."""
    run_async(lambda c: c.supplier.get(id), subscription_key=subscription_key, env=env, raw=raw)


@app.command("list")
def list_suppliers(
    office_id: Annotated[
        int | None, typer.Option("--office-id", help="Filter by office; null for global suppliers")
    ] = None,
    subscription_key: Annotated[
        str | None, typer.Option("--subscription-key", "-k", envvar="QONDOR_SUBSCRIPTION_KEY")
    ] = None,
    env: Annotated[str | None, typer.Option("--env", "-e", envvar="QONDOR_ENV")] = None,
    raw: Annotated[bool, typer.Option("--raw", help="Compact JSON")] = False,
) -> None:
    """List suppliers."""
    run_async(lambda c: c.supplier.get_all(office_id=office_id), subscription_key=subscription_key, env=env, raw=raw)


@app.command()
def create(
    name: Annotated[str, typer.Option("--name", help="Supplier name")],
    office_id: Annotated[int | None, typer.Option("--office-id", help="Office the supplier belongs to")] = None,
    email: Annotated[str | None, typer.Option("--email", help="Supplier email")] = None,
    external_reference: Annotated[
        str | None, typer.Option("--external-reference", help="Your unique external reference")
    ] = None,
    city: Annotated[str | None, typer.Option("--city", help="City")] = None,
    country_code: Annotated[str | None, typer.Option("--country-code", help="Two-letter ISO country code")] = None,
    address: Annotated[str | None, typer.Option("--address", help="Address line 1")] = None,
    address2: Annotated[str | None, typer.Option("--address2", help="Address line 2")] = None,
    zip_code: Annotated[str | None, typer.Option("--zip-code", help="Zip/postal code")] = None,
    organisation_number: Annotated[
        str | None, typer.Option("--organisation-number", help="Organisation number")
    ] = None,
    vat_number: Annotated[str | None, typer.Option("--vat-number", help="VAT number")] = None,
    phone_number: Annotated[str | None, typer.Option("--phone-number", help="Phone number")] = None,
    fax_number: Annotated[str | None, typer.Option("--fax-number", help="Fax number")] = None,
    status: Annotated[int | None, typer.Option("--status", help="1=Normal, 2=Preferred, 3=Do not use")] = None,
    chain: Annotated[str | None, typer.Option("--chain", help="Supplier chain")] = None,
    brand: Annotated[str | None, typer.Option("--brand", help="Supplier brand")] = None,
    supplier_number: Annotated[str | None, typer.Option("--supplier-number", help="Supplier number")] = None,
    is_internal_supplier: Annotated[
        bool | None,
        typer.Option("--is-internal-supplier/--no-is-internal-supplier", help="In-house vs external supplier"),
    ] = None,
    invoice_address_enabled: Annotated[
        bool | None,
        typer.Option("--invoice-address-enabled/--no-invoice-address-enabled", help="Enable separate invoice address"),
    ] = None,
    invoice_address: Annotated[str | None, typer.Option("--invoice-address", help="Invoice address line 1")] = None,
    invoice_address2: Annotated[str | None, typer.Option("--invoice-address2", help="Invoice address line 2")] = None,
    invoice_zip_code: Annotated[str | None, typer.Option("--invoice-zip-code", help="Invoice zip/postal code")] = None,
    invoice_city: Annotated[str | None, typer.Option("--invoice-city", help="Invoice city")] = None,
    invoice_country_code: Annotated[
        str | None, typer.Option("--invoice-country-code", help="Two-letter ISO code for invoice country")
    ] = None,
    invoice_additional_information: Annotated[
        str | None, typer.Option("--invoice-additional-information", help="Additional invoice information")
    ] = None,
    supplier_category_id: Annotated[
        int | None, typer.Option("--supplier-category-id", help="Supplier category ID")
    ] = None,
    remarks: Annotated[str | None, typer.Option("--remarks", help="Internal remarks (HTML sanitised)")] = None,
    subscription_key: Annotated[
        str | None, typer.Option("--subscription-key", "-k", envvar="QONDOR_SUBSCRIPTION_KEY")
    ] = None,
    env: Annotated[str | None, typer.Option("--env", "-e", envvar="QONDOR_ENV")] = None,
    raw: Annotated[bool, typer.Option("--raw", help="Compact JSON")] = False,
) -> None:
    """Create a supplier."""
    req = CreateSupplier(
        name=name,
        office_id=office_id,
        email=email,
        external_reference=external_reference,
        city=city,
        country_code=country_code,
        address=address,
        address2=address2,
        zip_code=zip_code,
        organisation_number=organisation_number,
        vat_number=vat_number,
        phone_number=phone_number,
        fax_number=fax_number,
        status=status,
        chain=chain,
        brand=brand,
        supplier_number=supplier_number,
        is_internal_supplier=is_internal_supplier,
        invoice_address_enabled=invoice_address_enabled,
        invoice_address=invoice_address,
        invoice_address2=invoice_address2,
        invoice_zip_code=invoice_zip_code,
        invoice_city=invoice_city,
        invoice_country_code=invoice_country_code,
        invoice_additional_information=invoice_additional_information,
        supplier_category_id=supplier_category_id,
        remarks=remarks,
    )
    run_async(lambda c: c.supplier.create(req), subscription_key=subscription_key, env=env, raw=raw)


@app.command()
def update(
    id: Annotated[int, typer.Option("--id", help="Supplier ID (required if no external-reference)")],
    name: Annotated[str | None, typer.Option("--name", help="Supplier name")] = None,
    external_reference: Annotated[
        str | None, typer.Option("--external-reference", help="Your unique external reference (required if no id)")
    ] = None,
    email: Annotated[str | None, typer.Option("--email", help="Supplier email")] = None,
    city: Annotated[str | None, typer.Option("--city", help="City")] = None,
    country_code: Annotated[str | None, typer.Option("--country-code", help="Two-letter ISO country code")] = None,
    address: Annotated[str | None, typer.Option("--address", help="Address line 1")] = None,
    address2: Annotated[str | None, typer.Option("--address2", help="Address line 2")] = None,
    zip_code: Annotated[str | None, typer.Option("--zip-code", help="Zip/postal code")] = None,
    organisation_number: Annotated[
        str | None, typer.Option("--organisation-number", help="Organisation number")
    ] = None,
    vat_number: Annotated[str | None, typer.Option("--vat-number", help="VAT number")] = None,
    phone_number: Annotated[str | None, typer.Option("--phone-number", help="Phone number")] = None,
    fax_number: Annotated[str | None, typer.Option("--fax-number", help="Fax number")] = None,
    status: Annotated[int | None, typer.Option("--status", help="1=Normal, 2=Preferred, 3=Do not use")] = None,
    chain: Annotated[str | None, typer.Option("--chain", help="Supplier chain")] = None,
    brand: Annotated[str | None, typer.Option("--brand", help="Supplier brand")] = None,
    supplier_number: Annotated[str | None, typer.Option("--supplier-number", help="Supplier number")] = None,
    is_internal_supplier: Annotated[
        bool | None,
        typer.Option("--is-internal-supplier/--no-is-internal-supplier", help="In-house vs external supplier"),
    ] = None,
    invoice_address_enabled: Annotated[
        bool | None,
        typer.Option("--invoice-address-enabled/--no-invoice-address-enabled", help="Enable separate invoice address"),
    ] = None,
    invoice_address: Annotated[str | None, typer.Option("--invoice-address", help="Invoice address line 1")] = None,
    invoice_address2: Annotated[str | None, typer.Option("--invoice-address2", help="Invoice address line 2")] = None,
    invoice_zip_code: Annotated[str | None, typer.Option("--invoice-zip-code", help="Invoice zip/postal code")] = None,
    invoice_city: Annotated[str | None, typer.Option("--invoice-city", help="Invoice city")] = None,
    invoice_country_code: Annotated[
        str | None, typer.Option("--invoice-country-code", help="Two-letter ISO code for invoice country")
    ] = None,
    invoice_additional_information: Annotated[
        str | None, typer.Option("--invoice-additional-information", help="Additional invoice information")
    ] = None,
    supplier_category_id: Annotated[
        int | None, typer.Option("--supplier-category-id", help="Supplier category ID")
    ] = None,
    remarks: Annotated[str | None, typer.Option("--remarks", help="Internal remarks (HTML sanitised)")] = None,
    subscription_key: Annotated[
        str | None, typer.Option("--subscription-key", "-k", envvar="QONDOR_SUBSCRIPTION_KEY")
    ] = None,
    env: Annotated[str | None, typer.Option("--env", "-e", envvar="QONDOR_ENV")] = None,
    raw: Annotated[bool, typer.Option("--raw", help="Compact JSON")] = False,
) -> None:
    """Update a supplier."""
    req = UpdateSupplier(
        id=id,
        name=name,
        external_reference=external_reference,
        email=email,
        city=city,
        country_code=country_code,
        address=address,
        address2=address2,
        zip_code=zip_code,
        organisation_number=organisation_number,
        vat_number=vat_number,
        phone_number=phone_number,
        fax_number=fax_number,
        status=status,
        chain=chain,
        brand=brand,
        supplier_number=supplier_number,
        is_internal_supplier=is_internal_supplier,
        invoice_address_enabled=invoice_address_enabled,
        invoice_address=invoice_address,
        invoice_address2=invoice_address2,
        invoice_zip_code=invoice_zip_code,
        invoice_city=invoice_city,
        invoice_country_code=invoice_country_code,
        invoice_additional_information=invoice_additional_information,
        supplier_category_id=supplier_category_id,
        remarks=remarks,
    )
    run_async(lambda c: c.supplier.update(req), subscription_key=subscription_key, env=env, raw=raw)


@app.command()
def delete(
    id: Annotated[int, typer.Argument(help="Supplier ID")],
    subscription_key: Annotated[
        str | None, typer.Option("--subscription-key", "-k", envvar="QONDOR_SUBSCRIPTION_KEY")
    ] = None,
    env: Annotated[str | None, typer.Option("--env", "-e", envvar="QONDOR_ENV")] = None,
    raw: Annotated[bool, typer.Option("--raw", help="Compact JSON")] = False,
) -> None:
    """Delete a supplier by ID."""
    run_async(lambda c: c.supplier.delete(id), subscription_key=subscription_key, env=env, raw=raw)


@app.command("get-by-ref")
def get_by_ref(
    external_reference: Annotated[str, typer.Option("--external-reference", help="External reference")],
    subscription_key: Annotated[
        str | None, typer.Option("--subscription-key", "-k", envvar="QONDOR_SUBSCRIPTION_KEY")
    ] = None,
    env: Annotated[str | None, typer.Option("--env", "-e", envvar="QONDOR_ENV")] = None,
    raw: Annotated[bool, typer.Option("--raw", help="Compact JSON")] = False,
) -> None:
    """Get a supplier by external reference."""
    run_async(
        lambda c: c.supplier.get_by_external_reference(external_reference=external_reference),
        subscription_key=subscription_key,
        env=env,
        raw=raw,
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
    """Delete a supplier by external reference."""
    run_async(
        lambda c: c.supplier.delete_by_external_reference(external_reference=external_reference),
        subscription_key=subscription_key,
        env=env,
        raw=raw,
    )
