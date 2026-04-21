"""qondor product-group — Product group commands."""

from __future__ import annotations

from typing import Annotated

import typer
from qondor_api_sdk.models.product_group import CreateProductGroup, UpdateProductGroup

from .._run import run_async

app = typer.Typer(no_args_is_help=True)


@app.command()
def get(
    id: Annotated[int, typer.Argument(help="Product group ID")],
    subscription_key: Annotated[
        str | None, typer.Option("--subscription-key", "-k", envvar="QONDOR_SUBSCRIPTION_KEY")
    ] = None,
    env: Annotated[str | None, typer.Option("--env", "-e", envvar="QONDOR_ENV")] = None,
    raw: Annotated[bool, typer.Option("--raw", help="Compact JSON")] = False,
) -> None:
    """Get a product group by ID."""
    run_async(lambda c: c.product_group.get(id), subscription_key=subscription_key, env=env, raw=raw)


@app.command("list")
def list_groups(
    offer_id: Annotated[int, typer.Option("--offer-id", help="Offer to list groups for")],
    subscription_key: Annotated[
        str | None, typer.Option("--subscription-key", "-k", envvar="QONDOR_SUBSCRIPTION_KEY")
    ] = None,
    env: Annotated[str | None, typer.Option("--env", "-e", envvar="QONDOR_ENV")] = None,
    raw: Annotated[bool, typer.Option("--raw", help="Compact JSON")] = False,
) -> None:
    """List product groups for an offer."""
    run_async(
        lambda c: c.product_group.get_all_for_offer(offer_id=offer_id),
        subscription_key=subscription_key,
        env=env,
        raw=raw,
    )


@app.command()
def create(
    offer_id: Annotated[int, typer.Option("--offer-id", help="Offer the group belongs to")],
    name: Annotated[str, typer.Option("--name", help="Group name/heading")],
    position: Annotated[int | None, typer.Option("--position", help="Position in the offer")] = None,
    introduction: Annotated[
        str | None, typer.Option("--introduction", help="Introduction text (HTML sanitised)")
    ] = None,
    description: Annotated[str | None, typer.Option("--description", help="Description text (HTML sanitised)")] = None,
    external_reference: Annotated[
        str | None, typer.Option("--external-reference", help="Your unique external reference")
    ] = None,
    offer_external_reference: Annotated[
        str | None, typer.Option("--offer-external-reference", help="External reference of the offer")
    ] = None,
    offer_design_template: Annotated[
        int | None,
        typer.Option(
            "--offer-design-template", help="1=Img left, 2=Img top, 6=Img right, 7=Three imgs top, 8=Img slider"
        ),
    ] = None,
    hide_all_products: Annotated[
        bool | None, typer.Option("--hide-all-products/--no-hide-all-products", help="Hide all products on the offer")
    ] = None,
    must_select_all_products: Annotated[
        bool | None,
        typer.Option(
            "--must-select-all-products/--no-must-select-all-products", help="All products must be selected if any are"
        ),
    ] = None,
    hide_product_prices: Annotated[
        bool | None,
        typer.Option(
            "--hide-product-prices/--no-hide-product-prices", help="Hide individual product prices on the offer"
        ),
    ] = None,
    show_total_price_for_group: Annotated[
        bool | None,
        typer.Option(
            "--show-total-price-for-group/--no-show-total-price-for-group", help="Display total price for the group"
        ),
    ] = None,
    show_total_price_per_person: Annotated[
        bool | None,
        typer.Option(
            "--show-total-price-per-person/--no-show-total-price-per-person", help="Display total price per person"
        ),
    ] = None,
    number_of_persons_in_total_price: Annotated[
        int | None,
        typer.Option("--number-of-persons-in-total-price", help="Persons used for per-person price calculation"),
    ] = None,
    hide_price_table: Annotated[
        bool | None,
        typer.Option(
            "--hide-price-table/--no-hide-price-table", help="Hide prices; disables accept/decline on products"
        ),
    ] = None,
    custom_total_row_text: Annotated[
        str | None, typer.Option("--custom-total-row-text", help="Override text for the total price row")
    ] = None,
    name_on_invoice: Annotated[
        str | None, typer.Option("--name-on-invoice", help="Text displayed on invoices for this group")
    ] = None,
    hide_feedback_on_offer: Annotated[
        bool | None,
        typer.Option(
            "--hide-feedback-on-offer/--no-hide-feedback-on-offer", help="Hide feedback when displaying the group"
        ),
    ] = None,
    subscription_key: Annotated[
        str | None, typer.Option("--subscription-key", "-k", envvar="QONDOR_SUBSCRIPTION_KEY")
    ] = None,
    env: Annotated[str | None, typer.Option("--env", "-e", envvar="QONDOR_ENV")] = None,
    raw: Annotated[bool, typer.Option("--raw", help="Compact JSON")] = False,
) -> None:
    """Create a product group."""
    req = CreateProductGroup(
        offer_id=offer_id,
        name=name,
        position=position,
        introduction=introduction,
        description=description,
        external_reference=external_reference,
        offer_external_reference=offer_external_reference,
        offer_design_template=offer_design_template,
        hide_all_products=hide_all_products,
        must_select_all_products=must_select_all_products,
        hide_product_prices=hide_product_prices,
        show_total_price_for_group=show_total_price_for_group,
        show_total_price_per_person=show_total_price_per_person,
        number_of_persons_in_total_price=number_of_persons_in_total_price,
        hide_price_table=hide_price_table,
        custom_total_row_text=custom_total_row_text,
        name_on_invoice=name_on_invoice,
        hide_feedback_on_offer=hide_feedback_on_offer,
    )
    run_async(lambda c: c.product_group.create(req), subscription_key=subscription_key, env=env, raw=raw)


@app.command()
def update(
    id: Annotated[int, typer.Option("--id", help="Product group ID")],
    name: Annotated[str | None, typer.Option("--name", help="Group name/heading")] = None,
    position: Annotated[int | None, typer.Option("--position", help="Position in the offer")] = None,
    external_reference: Annotated[
        str | None, typer.Option("--external-reference", help="Your unique external reference")
    ] = None,
    introduction: Annotated[
        str | None, typer.Option("--introduction", help="Introduction text (HTML sanitised)")
    ] = None,
    description: Annotated[str | None, typer.Option("--description", help="Description text (HTML sanitised)")] = None,
    offer_design_template: Annotated[
        int | None,
        typer.Option(
            "--offer-design-template", help="1=Img left, 2=Img top, 6=Img right, 7=Three imgs top, 8=Img slider"
        ),
    ] = None,
    hide_all_products: Annotated[
        bool | None, typer.Option("--hide-all-products/--no-hide-all-products", help="Hide all products on the offer")
    ] = None,
    must_select_all_products: Annotated[
        bool | None,
        typer.Option(
            "--must-select-all-products/--no-must-select-all-products", help="All products must be selected if any are"
        ),
    ] = None,
    hide_product_prices: Annotated[
        bool | None,
        typer.Option(
            "--hide-product-prices/--no-hide-product-prices", help="Hide individual product prices on the offer"
        ),
    ] = None,
    show_total_price_for_group: Annotated[
        bool | None,
        typer.Option(
            "--show-total-price-for-group/--no-show-total-price-for-group", help="Display total price for the group"
        ),
    ] = None,
    show_total_price_per_person: Annotated[
        bool | None,
        typer.Option(
            "--show-total-price-per-person/--no-show-total-price-per-person", help="Display total price per person"
        ),
    ] = None,
    number_of_persons_in_total_price: Annotated[
        int | None,
        typer.Option("--number-of-persons-in-total-price", help="Persons used for per-person price calculation"),
    ] = None,
    hide_price_table: Annotated[
        bool | None,
        typer.Option(
            "--hide-price-table/--no-hide-price-table", help="Hide prices; disables accept/decline on products"
        ),
    ] = None,
    custom_total_row_text: Annotated[
        str | None, typer.Option("--custom-total-row-text", help="Override text for the total price row")
    ] = None,
    name_on_invoice: Annotated[
        str | None, typer.Option("--name-on-invoice", help="Text displayed on invoices for this group")
    ] = None,
    hide_feedback_on_offer: Annotated[
        bool | None,
        typer.Option(
            "--hide-feedback-on-offer/--no-hide-feedback-on-offer", help="Hide feedback when displaying the group"
        ),
    ] = None,
    subscription_key: Annotated[
        str | None, typer.Option("--subscription-key", "-k", envvar="QONDOR_SUBSCRIPTION_KEY")
    ] = None,
    env: Annotated[str | None, typer.Option("--env", "-e", envvar="QONDOR_ENV")] = None,
    raw: Annotated[bool, typer.Option("--raw", help="Compact JSON")] = False,
) -> None:
    """Update a product group."""
    req = UpdateProductGroup(
        id=id,
        name=name,
        position=position,
        external_reference=external_reference,
        introduction=introduction,
        description=description,
        offer_design_template=offer_design_template,
        hide_all_products=hide_all_products,
        must_select_all_products=must_select_all_products,
        hide_product_prices=hide_product_prices,
        show_total_price_for_group=show_total_price_for_group,
        show_total_price_per_person=show_total_price_per_person,
        number_of_persons_in_total_price=number_of_persons_in_total_price,
        hide_price_table=hide_price_table,
        custom_total_row_text=custom_total_row_text,
        name_on_invoice=name_on_invoice,
        hide_feedback_on_offer=hide_feedback_on_offer,
    )
    run_async(lambda c: c.product_group.update(req), subscription_key=subscription_key, env=env, raw=raw)


@app.command()
def delete(
    id: Annotated[int, typer.Argument(help="Product group ID")],
    subscription_key: Annotated[
        str | None, typer.Option("--subscription-key", "-k", envvar="QONDOR_SUBSCRIPTION_KEY")
    ] = None,
    env: Annotated[str | None, typer.Option("--env", "-e", envvar="QONDOR_ENV")] = None,
    raw: Annotated[bool, typer.Option("--raw", help="Compact JSON")] = False,
) -> None:
    """Delete a product group by ID."""
    run_async(lambda c: c.product_group.delete(id), subscription_key=subscription_key, env=env, raw=raw)


@app.command("get-by-ref")
def get_by_ref(
    external_reference: Annotated[str, typer.Option("--external-reference", help="External reference")],
    subscription_key: Annotated[
        str | None, typer.Option("--subscription-key", "-k", envvar="QONDOR_SUBSCRIPTION_KEY")
    ] = None,
    env: Annotated[str | None, typer.Option("--env", "-e", envvar="QONDOR_ENV")] = None,
    raw: Annotated[bool, typer.Option("--raw", help="Compact JSON")] = False,
) -> None:
    """Get a product group by external reference."""
    run_async(
        lambda c: c.product_group.get_by_external_reference(external_reference=external_reference),
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
    """Delete a product group by external reference."""
    run_async(
        lambda c: c.product_group.delete_by_external_reference(external_reference=external_reference),
        subscription_key=subscription_key,
        env=env,
        raw=raw,
    )
