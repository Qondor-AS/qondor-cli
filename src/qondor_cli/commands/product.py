"""qondor product — Product commands."""

from __future__ import annotations

from typing import Annotated

import typer
from qondor_api_sdk.models.product import (
    AddPrice,
    AttachTicketToTransportProduct,
    ConfirmProduct,
    CreateProduct,
    UpdatePrice,
    UpdateProduct,
)

from .._run import run_async

app = typer.Typer(no_args_is_help=True)


@app.command()
def get(
    id: Annotated[int, typer.Argument(help="Product ID")],
    subscription_key: Annotated[
        str | None, typer.Option("--subscription-key", "-k", envvar="QONDOR_SUBSCRIPTION_KEY")
    ] = None,
    env: Annotated[str | None, typer.Option("--env", "-e", envvar="QONDOR_ENV")] = None,
    raw: Annotated[bool, typer.Option("--raw", help="Compact JSON")] = False,
) -> None:
    """Get a product by ID."""
    run_async(lambda c: c.product.get(id), subscription_key=subscription_key, env=env, raw=raw)


@app.command("list")
def list_products(
    project_id: Annotated[int | None, typer.Option("--project-id", help="Project to list products for")] = None,
    subscription_key: Annotated[
        str | None, typer.Option("--subscription-key", "-k", envvar="QONDOR_SUBSCRIPTION_KEY")
    ] = None,
    env: Annotated[str | None, typer.Option("--env", "-e", envvar="QONDOR_ENV")] = None,
    raw: Annotated[bool, typer.Option("--raw", help="Compact JSON")] = False,
) -> None:
    """List products for a project."""
    run_async(
        lambda c: c.product.get_all_for_project(project_id=project_id),
        subscription_key=subscription_key,
        env=env,
        raw=raw,
    )


@app.command()
def create(
    name: Annotated[str, typer.Option("--name", help="Product name")],
    offer_id: Annotated[int | None, typer.Option("--offer-id", help="Offer the product belongs to")] = None,
    product_group_id: Annotated[int | None, typer.Option("--product-group-id", help="Product group ID")] = None,
    supplier_id: Annotated[int | None, typer.Option("--supplier-id", help="Supplier ID")] = None,
    offer_quantity: Annotated[
        float | None, typer.Option("--offer-quantity", help="Quantity shown on the offer")
    ] = None,
    external_reference: Annotated[
        str | None, typer.Option("--external-reference", help="Your unique external reference")
    ] = None,
    product_type: Annotated[int | None, typer.Option("--product-type", help="1=Standard, 2=Transport")] = None,
    offer_external_reference: Annotated[
        str | None, typer.Option("--offer-external-reference", help="External reference of the offer")
    ] = None,
    product_group_external_reference: Annotated[
        str | None, typer.Option("--product-group-external-reference", help="External reference of the product group")
    ] = None,
    offer_intro_text: Annotated[
        str | None, typer.Option("--offer-intro-text", help="Introduction text on offer (HTML sanitised)")
    ] = None,
    offer_description: Annotated[
        str | None, typer.Option("--offer-description", help="Description text on offer (HTML sanitised)")
    ] = None,
    offer_terms_and_conditions_text: Annotated[
        str | None, typer.Option("--offer-terms-and-conditions-text", help="T&C text shown on offer")
    ] = None,
    name_on_invoice: Annotated[str | None, typer.Option("--name-on-invoice", help="Name displayed on invoices")] = None,
    name_on_offer: Annotated[str | None, typer.Option("--name-on-offer", help="Name displayed on the offer")] = None,
    supplier_external_reference: Annotated[
        str | None, typer.Option("--supplier-external-reference", help="External reference of the supplier")
    ] = None,
    supplier_specified: Annotated[
        bool | None,
        typer.Option("--supplier-specified/--no-supplier-specified", help="Explicitly set the supplier (even if null)"),
    ] = None,
    supplier_invoice_reference: Annotated[
        str | None, typer.Option("--supplier-invoice-reference", help="Supplier invoice reference")
    ] = None,
    product_category_id: Annotated[
        int | None, typer.Option("--product-category-id", help="Product category ID")
    ] = None,
    product_category_external_reference: Annotated[
        str | None,
        typer.Option("--product-category-external-reference", help="External reference of the product category"),
    ] = None,
    product_category_specified: Annotated[
        bool | None,
        typer.Option(
            "--product-category-specified/--no-product-category-specified",
            help="Explicitly set the category (even if null)",
        ),
    ] = None,
    is_published_on_offer: Annotated[
        bool | None,
        typer.Option("--is-published-on-offer/--no-is-published-on-offer", help="Publish product on the offer"),
    ] = None,
    is_mandatory_on_offer: Annotated[
        bool | None,
        typer.Option("--is-mandatory-on-offer/--no-is-mandatory-on-offer", help="Product is mandatory on the offer"),
    ] = None,
    hide_feedback_on_offer: Annotated[
        bool | None,
        typer.Option(
            "--hide-feedback-on-offer/--no-hide-feedback-on-offer", help="Hide feedback when displayed on offer"
        ),
    ] = None,
    commission_percent: Annotated[
        float | None, typer.Option("--commission-percent", help="Commission percentage")
    ] = None,
    billing_model: Annotated[
        int | None, typer.Option("--billing-model", help="0=Standard/Margin, 1=Referral, 2=Pass-through")
    ] = None,
    initial_rate: Annotated[
        float | None, typer.Option("--initial-rate", help="Base rate for out-price savings calculation")
    ] = None,
    is_initial_rate_incl_vat: Annotated[
        bool | None,
        typer.Option(
            "--is-initial-rate-incl-vat/--no-is-initial-rate-incl-vat", help="Whether initial-rate includes VAT"
        ),
    ] = None,
    subscription_key: Annotated[
        str | None, typer.Option("--subscription-key", "-k", envvar="QONDOR_SUBSCRIPTION_KEY")
    ] = None,
    env: Annotated[str | None, typer.Option("--env", "-e", envvar="QONDOR_ENV")] = None,
    raw: Annotated[bool, typer.Option("--raw", help="Compact JSON")] = False,
) -> None:
    """Create a product."""
    req = CreateProduct(
        name=name,
        offer_id=offer_id,
        product_group_id=product_group_id,
        supplier_id=supplier_id,
        offer_quantity=offer_quantity,
        external_reference=external_reference,
        product_type=product_type,
        offer_external_reference=offer_external_reference,
        product_group_external_reference=product_group_external_reference,
        offer_intro_text=offer_intro_text,
        offer_description=offer_description,
        offer_terms_and_conditions_text=offer_terms_and_conditions_text,
        name_on_invoice=name_on_invoice,
        name_on_offer=name_on_offer,
        supplier_external_reference=supplier_external_reference,
        supplier_specified=supplier_specified,
        supplier_invoice_reference=supplier_invoice_reference,
        product_category_id=product_category_id,
        product_category_external_reference=product_category_external_reference,
        product_category_specified=product_category_specified,
        is_published_on_offer=is_published_on_offer,
        is_mandatory_on_offer=is_mandatory_on_offer,
        hide_feedback_on_offer=hide_feedback_on_offer,
        commission_percent=commission_percent,
        billing_model=billing_model,
        initial_rate=initial_rate,
        is_initial_rate_incl_vat=is_initial_rate_incl_vat,
    )
    run_async(lambda c: c.product.create(req), subscription_key=subscription_key, env=env, raw=raw)


@app.command()
def update(
    id: Annotated[int, typer.Option("--id", help="Product ID")],
    name: Annotated[str | None, typer.Option("--name", help="Product name")] = None,
    external_reference: Annotated[
        str | None, typer.Option("--external-reference", help="Your unique external reference")
    ] = None,
    product_group_id: Annotated[int | None, typer.Option("--product-group-id", help="Product group ID")] = None,
    product_group_external_reference: Annotated[
        str | None, typer.Option("--product-group-external-reference", help="External reference of the product group")
    ] = None,
    offer_intro_text: Annotated[
        str | None, typer.Option("--offer-intro-text", help="Introduction text on offer (HTML sanitised)")
    ] = None,
    offer_description: Annotated[
        str | None, typer.Option("--offer-description", help="Description text on offer (HTML sanitised)")
    ] = None,
    offer_quantity: Annotated[
        float | None, typer.Option("--offer-quantity", help="Quantity shown on the offer")
    ] = None,
    offer_terms_and_conditions_text: Annotated[
        str | None, typer.Option("--offer-terms-and-conditions-text", help="T&C text shown on offer")
    ] = None,
    name_on_invoice: Annotated[str | None, typer.Option("--name-on-invoice", help="Name displayed on invoices")] = None,
    name_on_offer: Annotated[str | None, typer.Option("--name-on-offer", help="Name displayed on the offer")] = None,
    supplier_id: Annotated[int | None, typer.Option("--supplier-id", help="Supplier ID")] = None,
    supplier_external_reference: Annotated[
        str | None, typer.Option("--supplier-external-reference", help="External reference of the supplier")
    ] = None,
    supplier_specified: Annotated[
        bool | None,
        typer.Option("--supplier-specified/--no-supplier-specified", help="Explicitly set the supplier (even if null)"),
    ] = None,
    supplier_invoice_reference: Annotated[
        str | None, typer.Option("--supplier-invoice-reference", help="Supplier invoice reference")
    ] = None,
    product_category_id: Annotated[
        int | None, typer.Option("--product-category-id", help="Product category ID")
    ] = None,
    product_category_external_reference: Annotated[
        str | None,
        typer.Option("--product-category-external-reference", help="External reference of the product category"),
    ] = None,
    product_category_specified: Annotated[
        bool | None,
        typer.Option(
            "--product-category-specified/--no-product-category-specified",
            help="Explicitly set the category (even if null)",
        ),
    ] = None,
    is_published_on_offer: Annotated[
        bool | None,
        typer.Option("--is-published-on-offer/--no-is-published-on-offer", help="Publish product on the offer"),
    ] = None,
    is_mandatory_on_offer: Annotated[
        bool | None,
        typer.Option("--is-mandatory-on-offer/--no-is-mandatory-on-offer", help="Product is mandatory on the offer"),
    ] = None,
    hide_feedback_on_offer: Annotated[
        bool | None,
        typer.Option(
            "--hide-feedback-on-offer/--no-hide-feedback-on-offer", help="Hide feedback when displayed on offer"
        ),
    ] = None,
    commission_percent: Annotated[
        float | None, typer.Option("--commission-percent", help="Commission percentage")
    ] = None,
    billing_model: Annotated[
        int | None, typer.Option("--billing-model", help="0=Standard/Margin, 1=Referral, 2=Pass-through")
    ] = None,
    initial_rate: Annotated[
        float | None, typer.Option("--initial-rate", help="Base rate for out-price savings calculation")
    ] = None,
    is_initial_rate_incl_vat: Annotated[
        bool | None,
        typer.Option(
            "--is-initial-rate-incl-vat/--no-is-initial-rate-incl-vat", help="Whether initial-rate includes VAT"
        ),
    ] = None,
    subscription_key: Annotated[
        str | None, typer.Option("--subscription-key", "-k", envvar="QONDOR_SUBSCRIPTION_KEY")
    ] = None,
    env: Annotated[str | None, typer.Option("--env", "-e", envvar="QONDOR_ENV")] = None,
    raw: Annotated[bool, typer.Option("--raw", help="Compact JSON")] = False,
) -> None:
    """Update a product."""
    req = UpdateProduct(
        id=id,
        name=name,
        external_reference=external_reference,
        product_group_id=product_group_id,
        product_group_external_reference=product_group_external_reference,
        offer_intro_text=offer_intro_text,
        offer_description=offer_description,
        offer_quantity=offer_quantity,
        offer_terms_and_conditions_text=offer_terms_and_conditions_text,
        name_on_invoice=name_on_invoice,
        name_on_offer=name_on_offer,
        supplier_id=supplier_id,
        supplier_external_reference=supplier_external_reference,
        supplier_specified=supplier_specified,
        supplier_invoice_reference=supplier_invoice_reference,
        product_category_id=product_category_id,
        product_category_external_reference=product_category_external_reference,
        product_category_specified=product_category_specified,
        is_published_on_offer=is_published_on_offer,
        is_mandatory_on_offer=is_mandatory_on_offer,
        hide_feedback_on_offer=hide_feedback_on_offer,
        commission_percent=commission_percent,
        billing_model=billing_model,
        initial_rate=initial_rate,
        is_initial_rate_incl_vat=is_initial_rate_incl_vat,
    )
    run_async(lambda c: c.product.update(req), subscription_key=subscription_key, env=env, raw=raw)


@app.command()
def delete(
    id: Annotated[int, typer.Argument(help="Product ID")],
    subscription_key: Annotated[
        str | None, typer.Option("--subscription-key", "-k", envvar="QONDOR_SUBSCRIPTION_KEY")
    ] = None,
    env: Annotated[str | None, typer.Option("--env", "-e", envvar="QONDOR_ENV")] = None,
    raw: Annotated[bool, typer.Option("--raw", help="Compact JSON")] = False,
) -> None:
    """Delete a product by ID."""
    run_async(lambda c: c.product.delete(id), subscription_key=subscription_key, env=env, raw=raw)


@app.command("get-by-ref")
def get_by_ref(
    external_reference: Annotated[str, typer.Option("--external-reference", help="External reference")],
    subscription_key: Annotated[
        str | None, typer.Option("--subscription-key", "-k", envvar="QONDOR_SUBSCRIPTION_KEY")
    ] = None,
    env: Annotated[str | None, typer.Option("--env", "-e", envvar="QONDOR_ENV")] = None,
    raw: Annotated[bool, typer.Option("--raw", help="Compact JSON")] = False,
) -> None:
    """Get a product by external reference."""
    run_async(
        lambda c: c.product.get_by_external_reference(external_reference=external_reference),
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
    """Delete a product by external reference."""
    run_async(
        lambda c: c.product.delete_by_external_reference(external_reference=external_reference),
        subscription_key=subscription_key,
        env=env,
        raw=raw,
    )


@app.command("add-price")
def add_price(
    product_id: Annotated[int, typer.Option("--product-id", help="Product ID")],
    out_price_excl_vat: Annotated[
        float | None, typer.Option("--out-price-excl-vat", help="Out price excl. VAT")
    ] = None,
    out_price_incl_vat: Annotated[
        float | None, typer.Option("--out-price-incl-vat", help="Out price incl. VAT")
    ] = None,
    in_price_excl_vat: Annotated[float | None, typer.Option("--in-price-excl-vat", help="In price excl. VAT")] = None,
    in_price_incl_vat: Annotated[float | None, typer.Option("--in-price-incl-vat", help="In price incl. VAT")] = None,
    external_reference: Annotated[
        str | None, typer.Option("--external-reference", help="Your reference (must be unique within the product)")
    ] = None,
    product_external_reference: Annotated[
        str | None, typer.Option("--product-external-reference", help="External reference of the product")
    ] = None,
    art_no: Annotated[str | None, typer.Option("--art-no", help="Article number")] = None,
    foreign_in_price: Annotated[
        float | None, typer.Option("--foreign-in-price", help="In price in foreign currency")
    ] = None,
    foreign_in_price_offer_currency_id: Annotated[
        int | None,
        typer.Option("--foreign-in-price-offer-currency-id", help="Offer currency ID for the foreign in price"),
    ] = None,
    foreign_in_price_offer_currency_external_reference: Annotated[
        str | None,
        typer.Option(
            "--foreign-in-price-offer-currency-external-reference",
            help="Offer currency external ref for the foreign in price",
        ),
    ] = None,
    subscription_key: Annotated[
        str | None, typer.Option("--subscription-key", "-k", envvar="QONDOR_SUBSCRIPTION_KEY")
    ] = None,
    env: Annotated[str | None, typer.Option("--env", "-e", envvar="QONDOR_ENV")] = None,
    raw: Annotated[bool, typer.Option("--raw", help="Compact JSON")] = False,
) -> None:
    """Add a price to a product."""
    req = AddPrice(
        product_id=product_id,
        out_price_excl_vat=out_price_excl_vat,
        out_price_incl_vat=out_price_incl_vat,
        in_price_excl_vat=in_price_excl_vat,
        in_price_incl_vat=in_price_incl_vat,
        external_reference=external_reference,
        product_external_reference=product_external_reference,
        art_no=art_no,
        foreign_in_price=foreign_in_price,
        foreign_in_price_offer_currency_id=foreign_in_price_offer_currency_id,
        foreign_in_price_offer_currency_external_reference=foreign_in_price_offer_currency_external_reference,
    )
    run_async(lambda c: c.product.add_price(req), subscription_key=subscription_key, env=env, raw=raw)


@app.command("update-price")
def update_price(
    id: Annotated[
        int, typer.Option("--id", help="Price ID (or use --external-reference + --product-external-reference)")
    ],
    product_id: Annotated[int | None, typer.Option("--product-id", help="Product ID")] = None,
    out_price_excl_vat: Annotated[
        float | None, typer.Option("--out-price-excl-vat", help="Out price excl. VAT")
    ] = None,
    out_price_incl_vat: Annotated[
        float | None, typer.Option("--out-price-incl-vat", help="Out price incl. VAT")
    ] = None,
    in_price_excl_vat: Annotated[float | None, typer.Option("--in-price-excl-vat", help="In price excl. VAT")] = None,
    in_price_incl_vat: Annotated[float | None, typer.Option("--in-price-incl-vat", help="In price incl. VAT")] = None,
    external_reference: Annotated[
        str | None, typer.Option("--external-reference", help="Your reference (or use --id)")
    ] = None,
    product_external_reference: Annotated[
        str | None, typer.Option("--product-external-reference", help="External reference of the product")
    ] = None,
    art_no: Annotated[str | None, typer.Option("--art-no", help="Article number")] = None,
    foreign_in_price: Annotated[
        float | None, typer.Option("--foreign-in-price", help="In price in foreign currency")
    ] = None,
    foreign_in_price_offer_currency_id: Annotated[
        int | None,
        typer.Option("--foreign-in-price-offer-currency-id", help="Offer currency ID for the foreign in price"),
    ] = None,
    foreign_in_price_offer_currency_external_reference: Annotated[
        str | None,
        typer.Option(
            "--foreign-in-price-offer-currency-external-reference",
            help="Offer currency external ref for the foreign in price",
        ),
    ] = None,
    subscription_key: Annotated[
        str | None, typer.Option("--subscription-key", "-k", envvar="QONDOR_SUBSCRIPTION_KEY")
    ] = None,
    env: Annotated[str | None, typer.Option("--env", "-e", envvar="QONDOR_ENV")] = None,
    raw: Annotated[bool, typer.Option("--raw", help="Compact JSON")] = False,
) -> None:
    """Update a price on a product."""
    req = UpdatePrice(
        id=id,
        product_id=product_id,
        out_price_excl_vat=out_price_excl_vat,
        out_price_incl_vat=out_price_incl_vat,
        in_price_excl_vat=in_price_excl_vat,
        in_price_incl_vat=in_price_incl_vat,
        external_reference=external_reference,
        product_external_reference=product_external_reference,
        art_no=art_no,
        foreign_in_price=foreign_in_price,
        foreign_in_price_offer_currency_id=foreign_in_price_offer_currency_id,
        foreign_in_price_offer_currency_external_reference=foreign_in_price_offer_currency_external_reference,
    )
    run_async(lambda c: c.product.update_price(req), subscription_key=subscription_key, env=env, raw=raw)


@app.command("delete-price")
def delete_price(
    id: Annotated[int, typer.Option("--id", help="Price ID to delete")],
    product_id: Annotated[int | None, typer.Option("--product-id", help="Product the price belongs to")] = None,
    subscription_key: Annotated[
        str | None, typer.Option("--subscription-key", "-k", envvar="QONDOR_SUBSCRIPTION_KEY")
    ] = None,
    env: Annotated[str | None, typer.Option("--env", "-e", envvar="QONDOR_ENV")] = None,
    raw: Annotated[bool, typer.Option("--raw", help="Compact JSON")] = False,
) -> None:
    """Delete a price from a product."""
    run_async(
        lambda c: c.product.delete_price(id=id, product_id=product_id),
        subscription_key=subscription_key,
        env=env,
        raw=raw,
    )


@app.command("confirm")
def confirm(
    product_id: Annotated[int, typer.Option("--product-id", help="Product ID to confirm")],
    product_external_reference: Annotated[
        str | None, typer.Option("--product-external-reference", help="External reference of the product")
    ] = None,
    subscription_key: Annotated[
        str | None, typer.Option("--subscription-key", "-k", envvar="QONDOR_SUBSCRIPTION_KEY")
    ] = None,
    env: Annotated[str | None, typer.Option("--env", "-e", envvar="QONDOR_ENV")] = None,
    raw: Annotated[bool, typer.Option("--raw", help="Compact JSON")] = False,
) -> None:
    """Confirm a product."""
    req = ConfirmProduct(product_id=product_id, product_external_reference=product_external_reference)
    run_async(lambda c: c.product.confirm_product(req), subscription_key=subscription_key, env=env, raw=raw)


@app.command("attach-ticket")
def attach_ticket(
    transport_product_id: Annotated[
        int | None, typer.Option("--transport-product-id", help="Transport product ID")
    ] = None,
    transport_product_external_reference: Annotated[
        str | None, typer.Option("--transport-product-external-reference", help="Transport product external reference")
    ] = None,
    ticket_id: Annotated[int | None, typer.Option("--ticket-id", help="Ticket ID to attach")] = None,
    ticket_external_reference: Annotated[
        str | None, typer.Option("--ticket-external-reference", help="Ticket external reference")
    ] = None,
    subscription_key: Annotated[
        str | None, typer.Option("--subscription-key", "-k", envvar="QONDOR_SUBSCRIPTION_KEY")
    ] = None,
    env: Annotated[str | None, typer.Option("--env", "-e", envvar="QONDOR_ENV")] = None,
    raw: Annotated[bool, typer.Option("--raw", help="Compact JSON")] = False,
) -> None:
    """Attach a ticket to a transport product."""
    req = AttachTicketToTransportProduct(
        transport_product_id=transport_product_id,
        transport_product_external_reference=transport_product_external_reference,
        ticket_id=ticket_id,
        ticket_external_reference=ticket_external_reference,
    )
    run_async(
        lambda c: c.product.attach_ticket_to_transport_product(req), subscription_key=subscription_key, env=env, raw=raw
    )


@app.command("detach-ticket")
def detach_ticket(
    transport_product_id: Annotated[
        int | None, typer.Option("--transport-product-id", help="Transport product ID")
    ] = None,
    transport_product_external_reference: Annotated[
        str | None, typer.Option("--transport-product-external-reference", help="Transport product external reference")
    ] = None,
    ticket_id: Annotated[int | None, typer.Option("--ticket-id", help="Ticket ID to detach")] = None,
    ticket_external_reference: Annotated[
        str | None, typer.Option("--ticket-external-reference", help="Ticket external reference")
    ] = None,
    subscription_key: Annotated[
        str | None, typer.Option("--subscription-key", "-k", envvar="QONDOR_SUBSCRIPTION_KEY")
    ] = None,
    env: Annotated[str | None, typer.Option("--env", "-e", envvar="QONDOR_ENV")] = None,
    raw: Annotated[bool, typer.Option("--raw", help="Compact JSON")] = False,
) -> None:
    """Detach a ticket from a transport product."""
    run_async(
        lambda c: c.product.delete_detach_ticket_from_transport_product(
            transport_product_id=transport_product_id,
            transport_product_external_reference=transport_product_external_reference,
            ticket_id=ticket_id,
            ticket_external_reference=ticket_external_reference,
        ),
        subscription_key=subscription_key,
        env=env,
        raw=raw,
    )


@app.command("get-tickets")
def get_tickets(
    transport_product_id: Annotated[int, typer.Option("--transport-product-id", help="Transport product ID")],
    subscription_key: Annotated[
        str | None, typer.Option("--subscription-key", "-k", envvar="QONDOR_SUBSCRIPTION_KEY")
    ] = None,
    env: Annotated[str | None, typer.Option("--env", "-e", envvar="QONDOR_ENV")] = None,
    raw: Annotated[bool, typer.Option("--raw", help="Compact JSON")] = False,
) -> None:
    """Get tickets for a transport product."""
    run_async(
        lambda c: c.product.get_tickets_for_transport_product(transport_product_id=transport_product_id),
        subscription_key=subscription_key,
        env=env,
        raw=raw,
    )


@app.command("get-tickets-by-ref")
def get_tickets_by_ref(
    transport_product_external_reference: Annotated[
        str, typer.Option("--transport-product-external-reference", help="Transport product external reference")
    ],
    subscription_key: Annotated[
        str | None, typer.Option("--subscription-key", "-k", envvar="QONDOR_SUBSCRIPTION_KEY")
    ] = None,
    env: Annotated[str | None, typer.Option("--env", "-e", envvar="QONDOR_ENV")] = None,
    raw: Annotated[bool, typer.Option("--raw", help="Compact JSON")] = False,
) -> None:
    """Get tickets for a transport product by external reference."""
    run_async(
        lambda c: c.product.get_tickets_for_transport_product_by_external_reference(
            transport_product_external_reference=transport_product_external_reference
        ),
        subscription_key=subscription_key,
        env=env,
        raw=raw,
    )
