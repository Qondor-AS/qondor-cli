"""qondor offer — Offer commands."""

from __future__ import annotations

from typing import Annotated

import typer
from qondor_api_sdk.models.offer import AddCurrencyToOffer, CreateOffer, UpdateOffer, UpdateOfferCurrency

from .._run import run_async

app = typer.Typer(no_args_is_help=True)


@app.command()
def get(
    id: Annotated[int, typer.Argument(help="Offer ID")],
    subscription_key: Annotated[
        str | None, typer.Option("--subscription-key", "-k", envvar="QONDOR_SUBSCRIPTION_KEY")
    ] = None,
    env: Annotated[str | None, typer.Option("--env", "-e", envvar="QONDOR_ENV")] = None,
    raw: Annotated[bool, typer.Option("--raw", help="Compact JSON")] = False,
) -> None:
    """Get an offer by ID."""
    run_async(lambda c: c.offer.get(id), subscription_key=subscription_key, env=env, raw=raw)


@app.command("list")
def list_offers(
    project_id: Annotated[int, typer.Option("--project-id", help="Project to list offers for")],
    subscription_key: Annotated[
        str | None, typer.Option("--subscription-key", "-k", envvar="QONDOR_SUBSCRIPTION_KEY")
    ] = None,
    env: Annotated[str | None, typer.Option("--env", "-e", envvar="QONDOR_ENV")] = None,
    raw: Annotated[bool, typer.Option("--raw", help="Compact JSON")] = False,
) -> None:
    """List offers for a project."""
    run_async(
        lambda c: c.offer.get_all_for_project(project_id=project_id),
        subscription_key=subscription_key,
        env=env,
        raw=raw,
    )


@app.command()
def create(
    project_id: Annotated[int, typer.Option("--project-id", help="Project to create the offer in")],
    heading: Annotated[str | None, typer.Option("--heading", help="Offer heading")] = None,
    default_margin: Annotated[
        float | None, typer.Option("--default-margin", help="Default margin for the offer")
    ] = None,
    description: Annotated[str | None, typer.Option("--description", help="Offer description (HTML sanitised)")] = None,
    external_reference: Annotated[
        str | None, typer.Option("--external-reference", help="Your unique external reference")
    ] = None,
    project_no: Annotated[
        str | None, typer.Option("--project-no", help="Project number (alternative to project-id)")
    ] = None,
    is_main_offer: Annotated[
        bool | None, typer.Option("--is-main-offer/--no-is-main-offer", help="Set as main offer (one per project)")
    ] = None,
    disable_unsure_answer_on_products_and_groups: Annotated[
        bool | None,
        typer.Option(
            "--disable-unsure-answer-on-products-and-groups/--no-disable-unsure-answer-on-products-and-groups",
            help="Disable 'Unsure' answer on products/groups",
        ),
    ] = None,
    display_total_offer_price: Annotated[
        bool | None,
        typer.Option("--display-total-offer-price/--no-display-total-offer-price", help="Display total offer price"),
    ] = None,
    accommodation_offer_price_type: Annotated[
        int | None,
        typer.Option(
            "--accommodation-offer-price-type", help="1=Per person/night, 2=Per room/night, 3=Per room (entire stay)"
        ),
    ] = None,
    confirmation_page_content: Annotated[
        str | None, typer.Option("--confirmation-page-content", help="Confirmation page content (HTML sanitised)")
    ] = None,
    include_office_terms_and_conditions: Annotated[
        bool | None,
        typer.Option(
            "--include-office-terms-and-conditions/--no-include-office-terms-and-conditions",
            help="Include office T&C in the offer",
        ),
    ] = None,
    confirmation_page_header: Annotated[
        str | None, typer.Option("--confirmation-page-header", help="Confirmation page heading")
    ] = None,
    terms_and_conditions_text: Annotated[
        str | None, typer.Option("--terms-and-conditions-text", help="T&C text for the offer (HTML sanitised)")
    ] = None,
    status: Annotated[int | None, typer.Option("--status", help="1=Not sent, 2=Sent, 3=Confirmed, 4=Declined")] = None,
    email_confirmation_template_body: Annotated[
        str | None, typer.Option("--email-confirmation-template-body", help="Confirmation email body (HTML sanitised)")
    ] = None,
    email_confirmation_template_subject: Annotated[
        str | None, typer.Option("--email-confirmation-template-subject", help="Confirmation email subject")
    ] = None,
    use_office_settings: Annotated[
        bool | None, typer.Option("--use-office-settings/--no-use-office-settings", help="Use default office settings")
    ] = None,
    display_prices_excl_vat: Annotated[
        bool | None,
        typer.Option("--display-prices-excl-vat/--no-display-prices-excl-vat", help="Display prices excl. VAT"),
    ] = None,
    display_prices_incl_vat: Annotated[
        bool | None,
        typer.Option("--display-prices-incl-vat/--no-display-prices-incl-vat", help="Display prices incl. VAT"),
    ] = None,
    display_vat_amount: Annotated[
        bool | None, typer.Option("--display-vat-amount/--no-display-vat-amount", help="Display VAT amount")
    ] = None,
    hide_vat_text_from_prices: Annotated[
        bool | None,
        typer.Option(
            "--hide-vat-text-from-prices/--no-hide-vat-text-from-prices", help="Hide incl./excl. VAT label from prices"
        ),
    ] = None,
    display_total_price_column: Annotated[
        bool | None,
        typer.Option(
            "--display-total-price-column/--no-display-total-price-column",
            help="Display total price column in price tables",
        ),
    ] = None,
    display_total_price_incl_vat: Annotated[
        bool | None,
        typer.Option(
            "--display-total-price-incl-vat/--no-display-total-price-incl-vat", help="Display total price incl. VAT"
        ),
    ] = None,
    offer_valid_until_utc: Annotated[
        str | None, typer.Option("--offer-valid-until-utc", help="Offer valid-until date (UTC)")
    ] = None,
    location_code: Annotated[str | None, typer.Option("--location-code", help="Two-letter ISO location code")] = None,
    location_display_text: Annotated[
        str | None, typer.Option("--location-display-text", help="Display text for the offer location")
    ] = None,
    subscription_key: Annotated[
        str | None, typer.Option("--subscription-key", "-k", envvar="QONDOR_SUBSCRIPTION_KEY")
    ] = None,
    env: Annotated[str | None, typer.Option("--env", "-e", envvar="QONDOR_ENV")] = None,
    raw: Annotated[bool, typer.Option("--raw", help="Compact JSON")] = False,
) -> None:
    """Create an offer."""
    req = CreateOffer(
        project_id=project_id,
        project_no=project_no,
        heading=heading,
        default_margin=default_margin,
        description=description,
        external_reference=external_reference,
        is_main_offer=is_main_offer,
        disable_unsure_answer_on_products_and_groups=disable_unsure_answer_on_products_and_groups,
        display_total_offer_price=display_total_offer_price,
        accommodation_offer_price_type=accommodation_offer_price_type,
        confirmation_page_content=confirmation_page_content,
        include_office_terms_and_conditions=include_office_terms_and_conditions,
        confirmation_page_header=confirmation_page_header,
        terms_and_conditions_text=terms_and_conditions_text,
        status=status,
        email_confirmation_template_body=email_confirmation_template_body,
        email_confirmation_template_subject=email_confirmation_template_subject,
        use_office_settings=use_office_settings,
        display_prices_excl_vat=display_prices_excl_vat,
        display_prices_incl_vat=display_prices_incl_vat,
        display_vat_amount=display_vat_amount,
        hide_vat_text_from_prices=hide_vat_text_from_prices,
        display_total_price_column=display_total_price_column,
        display_total_price_incl_vat=display_total_price_incl_vat,
        offer_valid_until_utc=offer_valid_until_utc,
        location_code=location_code,
        location_display_text=location_display_text,
    )
    run_async(lambda c: c.offer.create(req), subscription_key=subscription_key, env=env, raw=raw)


@app.command()
def update(
    id: Annotated[int, typer.Option("--id", help="Offer ID (required if no external-reference)")],
    heading: Annotated[str | None, typer.Option("--heading", help="Offer heading")] = None,
    default_margin: Annotated[
        float | None, typer.Option("--default-margin", help="Default margin for the offer")
    ] = None,
    description: Annotated[str | None, typer.Option("--description", help="Offer description (HTML sanitised)")] = None,
    external_reference: Annotated[
        str | None, typer.Option("--external-reference", help="Your unique external reference")
    ] = None,
    is_main_offer: Annotated[
        bool | None, typer.Option("--is-main-offer/--no-is-main-offer", help="Set as main offer (one per project)")
    ] = None,
    disable_unsure_answer_on_products_and_groups: Annotated[
        bool | None,
        typer.Option(
            "--disable-unsure-answer-on-products-and-groups/--no-disable-unsure-answer-on-products-and-groups",
            help="Disable 'Unsure' answer on products/groups",
        ),
    ] = None,
    display_total_offer_price: Annotated[
        bool | None,
        typer.Option("--display-total-offer-price/--no-display-total-offer-price", help="Display total offer price"),
    ] = None,
    accommodation_offer_price_type: Annotated[
        int | None,
        typer.Option(
            "--accommodation-offer-price-type", help="1=Per person/night, 2=Per room/night, 3=Per room (entire stay)"
        ),
    ] = None,
    confirmation_page_content: Annotated[
        str | None, typer.Option("--confirmation-page-content", help="Confirmation page content (HTML sanitised)")
    ] = None,
    include_office_terms_and_conditions: Annotated[
        bool | None,
        typer.Option(
            "--include-office-terms-and-conditions/--no-include-office-terms-and-conditions",
            help="Include office T&C in the offer",
        ),
    ] = None,
    confirmation_page_header: Annotated[
        str | None, typer.Option("--confirmation-page-header", help="Confirmation page heading")
    ] = None,
    terms_and_conditions_text: Annotated[
        str | None, typer.Option("--terms-and-conditions-text", help="T&C text for the offer (HTML sanitised)")
    ] = None,
    status: Annotated[int | None, typer.Option("--status", help="1=Not sent, 2=Sent, 3=Confirmed, 4=Declined")] = None,
    email_confirmation_template_body: Annotated[
        str | None, typer.Option("--email-confirmation-template-body", help="Confirmation email body (HTML sanitised)")
    ] = None,
    email_confirmation_template_subject: Annotated[
        str | None, typer.Option("--email-confirmation-template-subject", help="Confirmation email subject")
    ] = None,
    use_office_settings: Annotated[
        bool | None, typer.Option("--use-office-settings/--no-use-office-settings", help="Use default office settings")
    ] = None,
    display_prices_excl_vat: Annotated[
        bool | None,
        typer.Option("--display-prices-excl-vat/--no-display-prices-excl-vat", help="Display prices excl. VAT"),
    ] = None,
    display_prices_incl_vat: Annotated[
        bool | None,
        typer.Option("--display-prices-incl-vat/--no-display-prices-incl-vat", help="Display prices incl. VAT"),
    ] = None,
    display_vat_amount: Annotated[
        bool | None, typer.Option("--display-vat-amount/--no-display-vat-amount", help="Display VAT amount")
    ] = None,
    hide_vat_text_from_prices: Annotated[
        bool | None,
        typer.Option(
            "--hide-vat-text-from-prices/--no-hide-vat-text-from-prices", help="Hide incl./excl. VAT label from prices"
        ),
    ] = None,
    display_total_price_column: Annotated[
        bool | None,
        typer.Option(
            "--display-total-price-column/--no-display-total-price-column",
            help="Display total price column in price tables",
        ),
    ] = None,
    display_total_price_incl_vat: Annotated[
        bool | None,
        typer.Option(
            "--display-total-price-incl-vat/--no-display-total-price-incl-vat", help="Display total price incl. VAT"
        ),
    ] = None,
    offer_valid_until_utc: Annotated[
        str | None, typer.Option("--offer-valid-until-utc", help="Offer valid-until date (UTC)")
    ] = None,
    location_code: Annotated[str | None, typer.Option("--location-code", help="Two-letter ISO location code")] = None,
    location_display_text: Annotated[
        str | None, typer.Option("--location-display-text", help="Display text for the offer location")
    ] = None,
    subscription_key: Annotated[
        str | None, typer.Option("--subscription-key", "-k", envvar="QONDOR_SUBSCRIPTION_KEY")
    ] = None,
    env: Annotated[str | None, typer.Option("--env", "-e", envvar="QONDOR_ENV")] = None,
    raw: Annotated[bool, typer.Option("--raw", help="Compact JSON")] = False,
) -> None:
    """Update an offer."""
    req = UpdateOffer(
        id=id,
        heading=heading,
        default_margin=default_margin,
        description=description,
        external_reference=external_reference,
        is_main_offer=is_main_offer,
        disable_unsure_answer_on_products_and_groups=disable_unsure_answer_on_products_and_groups,
        display_total_offer_price=display_total_offer_price,
        accommodation_offer_price_type=accommodation_offer_price_type,
        confirmation_page_content=confirmation_page_content,
        include_office_terms_and_conditions=include_office_terms_and_conditions,
        confirmation_page_header=confirmation_page_header,
        terms_and_conditions_text=terms_and_conditions_text,
        status=status,
        email_confirmation_template_body=email_confirmation_template_body,
        email_confirmation_template_subject=email_confirmation_template_subject,
        use_office_settings=use_office_settings,
        display_prices_excl_vat=display_prices_excl_vat,
        display_prices_incl_vat=display_prices_incl_vat,
        display_vat_amount=display_vat_amount,
        hide_vat_text_from_prices=hide_vat_text_from_prices,
        display_total_price_column=display_total_price_column,
        display_total_price_incl_vat=display_total_price_incl_vat,
        offer_valid_until_utc=offer_valid_until_utc,
        location_code=location_code,
        location_display_text=location_display_text,
    )
    run_async(lambda c: c.offer.update(req), subscription_key=subscription_key, env=env, raw=raw)


@app.command()
def delete(
    id: Annotated[int, typer.Argument(help="Offer ID")],
    subscription_key: Annotated[
        str | None, typer.Option("--subscription-key", "-k", envvar="QONDOR_SUBSCRIPTION_KEY")
    ] = None,
    env: Annotated[str | None, typer.Option("--env", "-e", envvar="QONDOR_ENV")] = None,
    raw: Annotated[bool, typer.Option("--raw", help="Compact JSON")] = False,
) -> None:
    """Delete an offer by ID."""
    run_async(lambda c: c.offer.delete(id), subscription_key=subscription_key, env=env, raw=raw)


@app.command("get-by-ref")
def get_by_ref(
    external_reference: Annotated[str, typer.Option("--external-reference", help="External reference")],
    subscription_key: Annotated[
        str | None, typer.Option("--subscription-key", "-k", envvar="QONDOR_SUBSCRIPTION_KEY")
    ] = None,
    env: Annotated[str | None, typer.Option("--env", "-e", envvar="QONDOR_ENV")] = None,
    raw: Annotated[bool, typer.Option("--raw", help="Compact JSON")] = False,
) -> None:
    """Get an offer by external reference."""
    run_async(
        lambda c: c.offer.get_by_external_reference(external_reference=external_reference),
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
    """Delete an offer by external reference."""
    run_async(
        lambda c: c.offer.delete_by_external_reference(external_reference=external_reference),
        subscription_key=subscription_key,
        env=env,
        raw=raw,
    )


@app.command("add-currency")
def add_currency(
    offer_id: Annotated[int, typer.Option("--offer-id", help="Offer ID")],
    currency_code: Annotated[
        str, typer.Option("--currency-code", help="Numeric ISO 4217 code (e.g. 978=EUR, 840=USD)")
    ],
    exchange_rate: Annotated[float, typer.Option("--exchange-rate", help="Exchange rate for the currency")],
    offer_external_reference: Annotated[
        str | None, typer.Option("--offer-external-reference", help="External reference of the offer")
    ] = None,
    external_reference: Annotated[
        str | None, typer.Option("--external-reference", help="Your reference for this currency")
    ] = None,
    date: Annotated[str | None, typer.Option("--date", help="Date for the exchange rate")] = None,
    subscription_key: Annotated[
        str | None, typer.Option("--subscription-key", "-k", envvar="QONDOR_SUBSCRIPTION_KEY")
    ] = None,
    env: Annotated[str | None, typer.Option("--env", "-e", envvar="QONDOR_ENV")] = None,
    raw: Annotated[bool, typer.Option("--raw", help="Compact JSON")] = False,
) -> None:
    """Add a currency to an offer."""
    req = AddCurrencyToOffer(
        offer_id=offer_id,
        currency_code=currency_code,
        exchange_rate=exchange_rate,
        offer_external_reference=offer_external_reference,
        external_reference=external_reference,
        date=date,
    )
    run_async(lambda c: c.offer.add_currency_to_offer(req), subscription_key=subscription_key, env=env, raw=raw)


@app.command("update-currency")
def update_currency(
    id: Annotated[int, typer.Option("--id", help="Currency ID")],
    offer_id: Annotated[int | None, typer.Option("--offer-id", help="Offer ID")] = None,
    exchange_rate: Annotated[
        float | None, typer.Option("--exchange-rate", help="Exchange rate for the currency")
    ] = None,
    external_reference: Annotated[
        str | None, typer.Option("--external-reference", help="Your reference for this currency")
    ] = None,
    offer_external_reference: Annotated[
        str | None, typer.Option("--offer-external-reference", help="External reference of the offer")
    ] = None,
    date: Annotated[str | None, typer.Option("--date", help="Date for the exchange rate")] = None,
    recalculate_out_prices: Annotated[
        bool | None,
        typer.Option(
            "--recalculate-out-prices/--no-recalculate-out-prices",
            help="Recalculate out prices for all products using this currency",
        ),
    ] = None,
    subscription_key: Annotated[
        str | None, typer.Option("--subscription-key", "-k", envvar="QONDOR_SUBSCRIPTION_KEY")
    ] = None,
    env: Annotated[str | None, typer.Option("--env", "-e", envvar="QONDOR_ENV")] = None,
    raw: Annotated[bool, typer.Option("--raw", help="Compact JSON")] = False,
) -> None:
    """Update a currency on an offer."""
    req = UpdateOfferCurrency(
        id=id,
        offer_id=offer_id,
        exchange_rate=exchange_rate,
        external_reference=external_reference,
        offer_external_reference=offer_external_reference,
        date_utc=date,
        recalculate_out_prices=recalculate_out_prices,
    )
    run_async(lambda c: c.offer.update_offer_currency(req), subscription_key=subscription_key, env=env, raw=raw)


@app.command("delete-currency")
def delete_currency(
    offer_id: Annotated[int, typer.Option("--offer-id", help="Offer the currency belongs to")],
    offer_currency_id: Annotated[int, typer.Option("--offer-currency-id", help="Currency to delete")],
    subscription_key: Annotated[
        str | None, typer.Option("--subscription-key", "-k", envvar="QONDOR_SUBSCRIPTION_KEY")
    ] = None,
    env: Annotated[str | None, typer.Option("--env", "-e", envvar="QONDOR_ENV")] = None,
    raw: Annotated[bool, typer.Option("--raw", help="Compact JSON")] = False,
) -> None:
    """Delete a currency from an offer."""
    run_async(
        lambda c: c.offer.delete_offer_currency(offer_id=offer_id, offer_currency_id=offer_currency_id),
        subscription_key=subscription_key,
        env=env,
        raw=raw,
    )
