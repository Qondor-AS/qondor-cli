"""Tests for CLI commands: verify correct arg mapping to SDK methods."""

from __future__ import annotations

import json
from unittest.mock import AsyncMock, MagicMock, patch

import pytest
from qondor_api_sdk.errors import QondorApiError, QondorRateLimitError, QondorServerError, QondorValidationError
from qondor_api_sdk.models.contact_person import CustomerContactPersonsDetails
from qondor_api_sdk.models.customer import CustomerDetails
from qondor_api_sdk.models.offer import OfferCurrencyDetails, OfferDetails
from qondor_api_sdk.models.office import OfficeSummary
from qondor_api_sdk.models.product import ProductDetails, ProductPriceOut, ProductTicketDetails
from qondor_api_sdk.models.product_group import ProductGroupDetails
from qondor_api_sdk.models.project import ProjectDetails
from qondor_api_sdk.models.supplier import SupplierDetails
from typer.testing import CliRunner

from qondor_cli.main import app

runner = CliRunner()


def _mock_client() -> MagicMock:
    """Build a mock QondorClient with async module methods."""
    client = MagicMock()
    # Offer module
    client.offer.get = AsyncMock(return_value=OfferDetails(id=789, heading="Test"))
    client.offer.get_all_for_project = AsyncMock(return_value=[])
    client.offer.create = AsyncMock(return_value=OfferDetails(id=100, heading="New"))
    client.offer.update = AsyncMock(return_value=None)
    client.offer.delete = AsyncMock(return_value=None)
    client.offer.get_by_external_reference = AsyncMock(return_value=OfferDetails(id=1))
    client.offer.delete_by_external_reference = AsyncMock(return_value=None)
    client.offer.add_currency_to_offer = AsyncMock(return_value=OfferCurrencyDetails(id=1))
    client.offer.update_offer_currency = AsyncMock(return_value=None)
    client.offer.delete_offer_currency = AsyncMock(return_value=None)
    # Project module
    client.project.get = AsyncMock(return_value=ProjectDetails(id=42, name="Test"))
    client.project.get_all = AsyncMock(return_value=[])
    client.project.create = AsyncMock(return_value=ProjectDetails(id=42, name="New"))
    client.project.get_by_project_no = AsyncMock(return_value=ProjectDetails(id=42))
    client.project.set_as_finished = AsyncMock(return_value=None)
    # Customer module
    client.customer.get = AsyncMock(return_value=CustomerDetails(id=123, name="Test"))
    client.customer.get_all = AsyncMock(return_value=[])
    client.customer.create = AsyncMock(return_value=CustomerDetails(id=123))
    client.customer.update = AsyncMock(return_value=None)
    client.customer.get_by_external_reference = AsyncMock(return_value=CustomerDetails(id=1))
    client.customer.get_all_by_customer_number = AsyncMock(return_value=[])
    # Product module
    client.product.get = AsyncMock(return_value=ProductDetails(id=50, name="Room"))
    client.product.get_all_for_project = AsyncMock(return_value=[])
    client.product.create = AsyncMock(return_value=ProductDetails(id=50))
    client.product.update = AsyncMock(return_value=None)
    client.product.delete = AsyncMock(return_value=None)
    client.product.get_by_external_reference = AsyncMock(return_value=ProductDetails(id=50))
    client.product.delete_by_external_reference = AsyncMock(return_value=None)
    client.product.add_price = AsyncMock(return_value=ProductPriceOut(id=100))
    client.product.update_price = AsyncMock(return_value=None)
    client.product.delete_price = AsyncMock(return_value=None)
    client.product.confirm_product = AsyncMock(return_value=None)
    client.product.attach_ticket_to_transport_product = AsyncMock(return_value=ProductTicketDetails(id=1))
    client.product.delete_detach_ticket_from_transport_product = AsyncMock(return_value=None)
    client.product.get_tickets_for_transport_product = AsyncMock(return_value=[])
    client.product.get_tickets_for_transport_product_by_external_reference = AsyncMock(return_value=[])
    # Product group module
    client.product_group.get = AsyncMock(return_value=ProductGroupDetails(id=20))
    client.product_group.get_all_for_offer = AsyncMock(return_value=[])
    client.product_group.create = AsyncMock(return_value=ProductGroupDetails(id=20, heading="Accom"))
    client.product_group.update = AsyncMock(return_value=None)
    client.product_group.delete = AsyncMock(return_value=None)
    client.product_group.get_by_external_reference = AsyncMock(return_value=ProductGroupDetails(id=20))
    client.product_group.delete_by_external_reference = AsyncMock(return_value=None)
    # Supplier module
    client.supplier.get = AsyncMock(return_value=SupplierDetails(id=101, name="Grand"))
    client.supplier.get_all = AsyncMock(return_value=[])
    client.supplier.create = AsyncMock(return_value=SupplierDetails(id=101))
    client.supplier.update = AsyncMock(return_value=None)
    client.supplier.delete = AsyncMock(return_value=None)
    client.supplier.get_by_external_reference = AsyncMock(return_value=SupplierDetails(id=101))
    client.supplier.delete_by_external_reference = AsyncMock(return_value=None)
    # Contact person module
    client.contact_person.get = AsyncMock(return_value=None)
    client.contact_person.create = AsyncMock(return_value=CustomerContactPersonsDetails(id=10))
    client.contact_person.update = AsyncMock(return_value=None)
    client.contact_person.delete = AsyncMock(return_value=None)
    client.contact_person.get_by_email = AsyncMock(return_value=None)
    client.contact_person.get_by_external_reference = AsyncMock(return_value=None)
    client.contact_person.delete_by_email = AsyncMock(return_value=None)
    client.contact_person.delete_by_external_reference = AsyncMock(return_value=None)
    client.contact_person.update_customer_relation = AsyncMock(return_value=None)
    client.contact_person.update_supplier_relation = AsyncMock(return_value=None)
    # Office module
    client.office.get_all = AsyncMock(return_value=[OfficeSummary(id=1, name="Oslo")])
    client.office.get_all_customer_categories = AsyncMock(return_value=[])
    # Statistics module
    client.statistics.get_offer_sales = AsyncMock(return_value=[])
    # Close
    client.close = AsyncMock()
    return client


def _run(args: list[str]) -> object:
    """Run CLI with mocked client and key."""
    mock_client = _mock_client()

    class _FakeCtx:
        async def __aenter__(self):
            return mock_client

        async def __aexit__(self, *a):
            await mock_client.close()

    with patch("qondor_cli._run.build_client", return_value=_FakeCtx()):
        result = runner.invoke(app, args, env={"QONDOR_SUBSCRIPTION_KEY": "test-key"})

    return result, mock_client


class TestOfferCommands:
    def test_offer_get(self):
        result, client = _run(["offer", "get", "789"])
        assert result.exit_code == 0
        client.offer.get.assert_awaited_once_with(789)
        parsed = json.loads(result.output)
        assert parsed["id"] == 789

    def test_offer_list(self):
        result, client = _run(["offer", "list", "--project-id", "42"])
        assert result.exit_code == 0
        client.offer.get_all_for_project.assert_awaited_once_with(project_id=42)

    def test_offer_create(self):
        result, client = _run(["offer", "create", "--project-id", "42", "--heading", "Test"])
        assert result.exit_code == 0
        req = client.offer.create.call_args[0][0]
        assert req.project_id == 42
        assert req.heading == "Test"

    def test_offer_delete(self):
        result, client = _run(["offer", "delete", "789"])
        assert result.exit_code == 0
        client.offer.delete.assert_awaited_once_with(789)

    def test_offer_get_by_ref(self):
        result, client = _run(["offer", "get-by-ref", "--external-reference", "ext-1"])
        assert result.exit_code == 0
        client.offer.get_by_external_reference.assert_awaited_once_with(external_reference="ext-1")

    def test_offer_delete_by_ref(self):
        result, client = _run(["offer", "delete-by-ref", "--external-reference", "ext-1"])
        assert result.exit_code == 0
        client.offer.delete_by_external_reference.assert_awaited_once_with(external_reference="ext-1")

    @pytest.mark.parametrize(
        "extra_args,field,expected",
        [
            (["--project-no", "P001"], "project_no", "P001"),
            (["--is-main-offer"], "is_main_offer", True),
            (["--disable-unsure-answer-on-products-and-groups"], "disable_unsure_answer_on_products_and_groups", True),
            (["--display-total-offer-price"], "display_total_offer_price", True),
            (["--accommodation-offer-price-type", "1"], "accommodation_offer_price_type", 1),
            (["--confirmation-page-content", "Thanks"], "confirmation_page_content", "Thanks"),
            (["--include-office-terms-and-conditions"], "include_office_terms_and_conditions", True),
            (["--confirmation-page-header", "Header"], "confirmation_page_header", "Header"),
            (["--terms-and-conditions-text", "Terms"], "terms_and_conditions_text", "Terms"),
            (["--status", "2"], "status", 2),
            (["--email-confirmation-template-body", "Body"], "email_confirmation_template_body", "Body"),
            (["--email-confirmation-template-subject", "Subj"], "email_confirmation_template_subject", "Subj"),
            (["--use-office-settings"], "use_office_settings", True),
            (["--display-prices-excl-vat"], "display_prices_excl_vat", True),
            (["--display-prices-incl-vat"], "display_prices_incl_vat", True),
            (["--display-vat-amount"], "display_vat_amount", True),
            (["--hide-vat-text-from-prices"], "hide_vat_text_from_prices", True),
            (["--display-total-price-column"], "display_total_price_column", True),
            (["--display-total-price-incl-vat"], "display_total_price_incl_vat", True),
            (["--offer-valid-until-utc", "2026-12-31"], "offer_valid_until_utc", "2026-12-31"),
            (["--location-code", "OSL"], "location_code", "OSL"),
            (["--location-display-text", "Oslo"], "location_display_text", "Oslo"),
        ],
    )
    def test_offer_create_options(self, extra_args, field, expected):
        result, client = _run(["offer", "create", "--project-id", "42"] + extra_args)
        assert result.exit_code == 0
        req = client.offer.create.call_args[0][0]
        assert getattr(req, field) == expected

    @pytest.mark.parametrize(
        "extra_args,field,expected",
        [
            (["--is-main-offer"], "is_main_offer", True),
            (["--disable-unsure-answer-on-products-and-groups"], "disable_unsure_answer_on_products_and_groups", True),
            (["--display-total-offer-price"], "display_total_offer_price", True),
            (["--accommodation-offer-price-type", "1"], "accommodation_offer_price_type", 1),
            (["--confirmation-page-content", "Thanks"], "confirmation_page_content", "Thanks"),
            (["--include-office-terms-and-conditions"], "include_office_terms_and_conditions", True),
            (["--confirmation-page-header", "Header"], "confirmation_page_header", "Header"),
            (["--terms-and-conditions-text", "Terms"], "terms_and_conditions_text", "Terms"),
            (["--status", "2"], "status", 2),
            (["--email-confirmation-template-body", "Body"], "email_confirmation_template_body", "Body"),
            (["--email-confirmation-template-subject", "Subj"], "email_confirmation_template_subject", "Subj"),
            (["--use-office-settings"], "use_office_settings", True),
            (["--display-prices-excl-vat"], "display_prices_excl_vat", True),
            (["--display-prices-incl-vat"], "display_prices_incl_vat", True),
            (["--display-vat-amount"], "display_vat_amount", True),
            (["--hide-vat-text-from-prices"], "hide_vat_text_from_prices", True),
            (["--display-total-price-column"], "display_total_price_column", True),
            (["--display-total-price-incl-vat"], "display_total_price_incl_vat", True),
            (["--offer-valid-until-utc", "2026-12-31"], "offer_valid_until_utc", "2026-12-31"),
            (["--location-code", "OSL"], "location_code", "OSL"),
            (["--location-display-text", "Oslo"], "location_display_text", "Oslo"),
        ],
    )
    def test_offer_update_options(self, extra_args, field, expected):
        result, client = _run(["offer", "update", "--id", "1"] + extra_args)
        assert result.exit_code == 0
        req = client.offer.update.call_args[0][0]
        assert getattr(req, field) == expected

    @pytest.mark.parametrize(
        "extra_args,field,expected",
        [
            (["--offer-external-reference", "off-1"], "offer_external_reference", "off-1"),
            (["--external-reference", "cur-1"], "external_reference", "cur-1"),
            (["--date", "2026-01-01"], "date", "2026-01-01"),
        ],
    )
    def test_offer_add_currency_options(self, extra_args, field, expected):
        result, client = _run(
            ["offer", "add-currency", "--offer-id", "1", "--currency-code", "USD", "--exchange-rate", "10.5"]
            + extra_args
        )
        assert result.exit_code == 0
        req = client.offer.add_currency_to_offer.call_args[0][0]
        assert getattr(req, field) == expected

    @pytest.mark.parametrize(
        "extra_args,field,expected",
        [
            (["--external-reference", "cur-1"], "external_reference", "cur-1"),
            (["--offer-external-reference", "off-1"], "offer_external_reference", "off-1"),
            (["--date", "2026-01-01"], "date_utc", "2026-01-01"),
            (["--recalculate-out-prices"], "recalculate_out_prices", True),
        ],
    )
    def test_offer_update_currency_options(self, extra_args, field, expected):
        result, client = _run(["offer", "update-currency", "--id", "1"] + extra_args)
        assert result.exit_code == 0
        req = client.offer.update_offer_currency.call_args[0][0]
        assert getattr(req, field) == expected


class TestProjectCommands:
    def test_project_get(self):
        result, client = _run(["project", "get", "42"])
        assert result.exit_code == 0
        client.project.get.assert_awaited_once_with(42)

    def test_project_list(self):
        result, client = _run(["project", "list"])
        assert result.exit_code == 0
        client.project.get_all.assert_awaited_once()

    def test_project_get_by_project_no(self):
        result, client = _run(["project", "get-by-project-no", "--project-no", "P001", "--office-id", "1"])
        assert result.exit_code == 0
        client.project.get_by_project_no.assert_awaited_once_with(project_no="P001", office_id=1)

    def test_project_create(self):
        result, client = _run(["project", "create", "--name", "Conf 2026", "--office-id", "1"])
        assert result.exit_code == 0
        req = client.project.create.call_args[0][0]
        assert req.name == "Conf 2026"
        assert req.office_id == 1

    @pytest.mark.parametrize(
        "extra_args,field,expected",
        [
            (["--project-no", "P001"], "project_no", "P001"),
            (["--main-project-manager-id", "5"], "main_project_manager_id", 5),
            (["--main-project-manager-user-name", "john"], "main_project_manager_user_name", "john"),
            (["--customer-external-reference", "cust-1"], "customer_external_reference", "cust-1"),
            (["--customer-number", "C001"], "customer_number", "C001"),
            (["--main-contact-person-id", "10"], "main_contact_person_id", 10),
            (["--main-contact-person-email", "a@b.com"], "main_contact_person_email", "a@b.com"),
            (["--main-contact-person-external-reference", "cp-1"], "main_contact_person_external_reference", "cp-1"),
            (["--team-id", "3"], "team_id", 3),
            (["--team-external-reference", "team-1"], "team_external_reference", "team-1"),
            (["--location-code", "OSL"], "location_code", "OSL"),
            (["--budgeted-sales", "50000"], "budgeted_sales", 50000.0),
            (["--budgeted-revenue", "40000"], "budgeted_revenue", 40000.0),
            (["--currency", "NOK"], "currency", "NOK"),
            (["--lead-from", "Web"], "lead_from", "Web"),
            (["--project-category", "Conference"], "project_category", "Conference"),
        ],
    )
    def test_project_create_options(self, extra_args, field, expected):
        result, client = _run(["project", "create", "--name", "Test"] + extra_args)
        assert result.exit_code == 0
        req = client.project.create.call_args[0][0]
        assert getattr(req, field) == expected

    @pytest.mark.parametrize(
        "extra_args,field,expected",
        [
            (["--project-no", "P001"], "project_no", "P001"),
            (["--office-id", "2"], "office_id", 2),
            (["--real-sales", "100000"], "real_sales", 100000.0),
            (["--real-revenue", "80000"], "real_revenue", 80000.0),
        ],
    )
    def test_project_set_as_finished_options(self, extra_args, field, expected):
        result, client = _run(["project", "set-as-finished", "--project-id", "1"] + extra_args)
        assert result.exit_code == 0
        req = client.project.set_as_finished.call_args[0][0]
        assert getattr(req, field) == expected


class TestCustomerCommands:
    def test_customer_get(self):
        result, client = _run(["customer", "get", "123"])
        assert result.exit_code == 0
        client.customer.get.assert_awaited_once_with(123)

    def test_customer_list(self):
        result, client = _run(["customer", "list", "--office-id", "1"])
        assert result.exit_code == 0
        client.customer.get_all.assert_awaited_once_with(office_id=1)

    def test_customer_search(self):
        result, client = _run(["customer", "search", "--customer-number", "C001"])
        assert result.exit_code == 0
        client.customer.get_all_by_customer_number.assert_awaited_once_with(customer_number="C001", office_id=None)

    @pytest.mark.parametrize(
        "extra_args,field,expected",
        [
            (["--legal-name", "ACME Corp"], "legal_name", "ACME Corp"),
            (["--address", "Main St 1"], "address", "Main St 1"),
            (["--address2", "Suite 5"], "address2", "Suite 5"),
            (["--zip-code", "0150"], "zip_code", "0150"),
            (["--vat-number", "NO123456789"], "vat_number", "NO123456789"),
            (["--phone-number", "+4712345678"], "phone_number", "+4712345678"),
            (["--fax-number", "+4787654321"], "fax_number", "+4787654321"),
            (["--is-invoiceable"], "is_invoiceable", True),
            (["--invoice-currency", "NOK"], "invoice_currency", "NOK"),
            (["--invoice-currency-code", "578"], "invoice_currency_code", 578),
            (["--invoice-address-enabled"], "invoice_address_enabled", True),
            (["--invoice-address", "Invoice St 1"], "invoice_address", "Invoice St 1"),
            (["--invoice-address2", "Box 99"], "invoice_address2", "Box 99"),
            (["--invoice-zip-code", "0160"], "invoice_zip_code", "0160"),
            (["--invoice-city", "Oslo"], "invoice_city", "Oslo"),
            (["--invoice-country-code", "NO"], "invoice_country_code", "NO"),
            (["--invoice-additional-information", "Attn: Finance"], "invoice_additional_information", "Attn: Finance"),
            (["--customer-category-id", "3"], "customer_category_id", 3),
            (["--is-active"], "is_active", True),
            (["--invoice-email", "inv@acme.com"], "invoice_email", "inv@acme.com"),
            (["--remarks", "VIP customer"], "remarks", "VIP customer"),
        ],
    )
    def test_customer_create_options(self, extra_args, field, expected):
        result, client = _run(["customer", "create", "--name", "Test"] + extra_args)
        assert result.exit_code == 0
        req = client.customer.create.call_args[0][0]
        assert getattr(req, field) == expected

    @pytest.mark.parametrize(
        "extra_args,field,expected",
        [
            (["--name", "Updated"], "name", "Updated"),
            (["--external-reference", "ext-1"], "external_reference", "ext-1"),
            (["--legal-name", "ACME Corp"], "legal_name", "ACME Corp"),
            (["--address", "Main St 1"], "address", "Main St 1"),
            (["--address2", "Suite 5"], "address2", "Suite 5"),
            (["--zip-code", "0150"], "zip_code", "0150"),
            (["--city", "Oslo"], "city", "Oslo"),
            (["--country-code", "NO"], "country_code", "NO"),
            (["--organisation-number", "123456789"], "organisation_number", "123456789"),
            (["--customer-number", "C001"], "customer_number", "C001"),
            (["--vat-number", "NO123456789"], "vat_number", "NO123456789"),
            (["--phone-number", "+4712345678"], "phone_number", "+4712345678"),
            (["--fax-number", "+4787654321"], "fax_number", "+4787654321"),
            (["--is-invoiceable"], "is_invoiceable", True),
            (["--invoice-currency", "NOK"], "invoice_currency", "NOK"),
            (["--invoice-currency-code", "578"], "invoice_currency_code", 578),
            (["--invoice-address-enabled"], "invoice_address_enabled", True),
            (["--invoice-address", "Invoice St 1"], "invoice_address", "Invoice St 1"),
            (["--invoice-address2", "Box 99"], "invoice_address2", "Box 99"),
            (["--invoice-zip-code", "0160"], "invoice_zip_code", "0160"),
            (["--invoice-city", "Oslo"], "invoice_city", "Oslo"),
            (["--invoice-country-code", "NO"], "invoice_country_code", "NO"),
            (["--invoice-additional-information", "Attn: Finance"], "invoice_additional_information", "Attn: Finance"),
            (["--customer-category-id", "3"], "customer_category_id", 3),
            (["--is-active"], "is_active", True),
            (["--invoice-email", "inv@acme.com"], "invoice_email", "inv@acme.com"),
            (["--remarks", "VIP customer"], "remarks", "VIP customer"),
        ],
    )
    def test_customer_update_options(self, extra_args, field, expected):
        result, client = _run(["customer", "update", "--id", "1"] + extra_args)
        assert result.exit_code == 0
        req = client.customer.update.call_args[0][0]
        assert getattr(req, field) == expected


class TestProductCommands:
    def test_product_get(self):
        result, client = _run(["product", "get", "50"])
        assert result.exit_code == 0
        client.product.get.assert_awaited_once_with(50)

    def test_product_list(self):
        result, client = _run(["product", "list", "--project-id", "42"])
        assert result.exit_code == 0
        client.product.get_all_for_project.assert_awaited_once_with(project_id=42)

    def test_product_add_price(self):
        result, client = _run(["product", "add-price", "--product-id", "50", "--out-price-excl-vat", "1500"])
        assert result.exit_code == 0
        req = client.product.add_price.call_args[0][0]
        assert req.product_id == 50
        assert req.out_price_excl_vat == 1500.0

    @pytest.mark.parametrize(
        "extra_args,field,expected",
        [
            (["--product-type", "1"], "product_type", 1),
            (["--offer-external-reference", "off-1"], "offer_external_reference", "off-1"),
            (["--product-group-external-reference", "pg-1"], "product_group_external_reference", "pg-1"),
            (["--offer-intro-text", "Intro"], "offer_intro_text", "Intro"),
            (["--offer-description", "Desc"], "offer_description", "Desc"),
            (["--offer-terms-and-conditions-text", "Terms"], "offer_terms_and_conditions_text", "Terms"),
            (["--name-on-invoice", "Room"], "name_on_invoice", "Room"),
            (["--name-on-offer", "Deluxe Room"], "name_on_offer", "Deluxe Room"),
            (["--supplier-external-reference", "sup-1"], "supplier_external_reference", "sup-1"),
            (["--supplier-specified"], "supplier_specified", True),
            (["--supplier-invoice-reference", "INV-1"], "supplier_invoice_reference", "INV-1"),
            (["--product-category-id", "5"], "product_category_id", 5),
            (["--product-category-external-reference", "cat-1"], "product_category_external_reference", "cat-1"),
            (["--product-category-specified"], "product_category_specified", True),
            (["--is-published-on-offer"], "is_published_on_offer", True),
            (["--is-mandatory-on-offer"], "is_mandatory_on_offer", True),
            (["--hide-feedback-on-offer"], "hide_feedback_on_offer", True),
            (["--commission-percent", "10.5"], "commission_percent", 10.5),
            (["--billing-model", "2"], "billing_model", 2),
            (["--initial-rate", "500"], "initial_rate", 500.0),
            (["--is-initial-rate-incl-vat"], "is_initial_rate_incl_vat", True),
        ],
    )
    def test_product_create_options(self, extra_args, field, expected):
        result, client = _run(["product", "create", "--name", "Test"] + extra_args)
        assert result.exit_code == 0
        req = client.product.create.call_args[0][0]
        assert getattr(req, field) == expected

    @pytest.mark.parametrize(
        "extra_args,field,expected",
        [
            (["--product-group-id", "3"], "product_group_id", 3),
            (["--product-group-external-reference", "pg-1"], "product_group_external_reference", "pg-1"),
            (["--offer-intro-text", "Intro"], "offer_intro_text", "Intro"),
            (["--offer-description", "Desc"], "offer_description", "Desc"),
            (["--offer-quantity", "10"], "offer_quantity", 10.0),
            (["--offer-terms-and-conditions-text", "Terms"], "offer_terms_and_conditions_text", "Terms"),
            (["--name-on-invoice", "Room"], "name_on_invoice", "Room"),
            (["--name-on-offer", "Deluxe Room"], "name_on_offer", "Deluxe Room"),
            (["--supplier-id", "7"], "supplier_id", 7),
            (["--supplier-external-reference", "sup-1"], "supplier_external_reference", "sup-1"),
            (["--supplier-specified"], "supplier_specified", True),
            (["--supplier-invoice-reference", "INV-1"], "supplier_invoice_reference", "INV-1"),
            (["--product-category-id", "5"], "product_category_id", 5),
            (["--product-category-external-reference", "cat-1"], "product_category_external_reference", "cat-1"),
            (["--product-category-specified"], "product_category_specified", True),
            (["--is-published-on-offer"], "is_published_on_offer", True),
            (["--is-mandatory-on-offer"], "is_mandatory_on_offer", True),
            (["--hide-feedback-on-offer"], "hide_feedback_on_offer", True),
            (["--commission-percent", "10.5"], "commission_percent", 10.5),
            (["--billing-model", "2"], "billing_model", 2),
            (["--initial-rate", "500"], "initial_rate", 500.0),
            (["--is-initial-rate-incl-vat"], "is_initial_rate_incl_vat", True),
        ],
    )
    def test_product_update_options(self, extra_args, field, expected):
        result, client = _run(["product", "update", "--id", "1"] + extra_args)
        assert result.exit_code == 0
        req = client.product.update.call_args[0][0]
        assert getattr(req, field) == expected

    @pytest.mark.parametrize(
        "extra_args,field,expected",
        [
            (["--external-reference", "pr-1"], "external_reference", "pr-1"),
            (["--product-external-reference", "prod-1"], "product_external_reference", "prod-1"),
            (["--art-no", "ART001"], "art_no", "ART001"),
            (["--foreign-in-price", "100.5"], "foreign_in_price", 100.5),
            (["--foreign-in-price-offer-currency-id", "3"], "foreign_in_price_offer_currency_id", 3),
            (
                ["--foreign-in-price-offer-currency-external-reference", "cur-1"],
                "foreign_in_price_offer_currency_external_reference",
                "cur-1",
            ),
        ],
    )
    def test_product_add_price_options(self, extra_args, field, expected):
        result, client = _run(["product", "add-price", "--product-id", "50"] + extra_args)
        assert result.exit_code == 0
        req = client.product.add_price.call_args[0][0]
        assert getattr(req, field) == expected

    @pytest.mark.parametrize(
        "extra_args,field,expected",
        [
            (["--external-reference", "pr-1"], "external_reference", "pr-1"),
            (["--product-external-reference", "prod-1"], "product_external_reference", "prod-1"),
            (["--art-no", "ART001"], "art_no", "ART001"),
            (["--foreign-in-price", "100.5"], "foreign_in_price", 100.5),
            (["--foreign-in-price-offer-currency-id", "3"], "foreign_in_price_offer_currency_id", 3),
            (
                ["--foreign-in-price-offer-currency-external-reference", "cur-1"],
                "foreign_in_price_offer_currency_external_reference",
                "cur-1",
            ),
        ],
    )
    def test_product_update_price_options(self, extra_args, field, expected):
        result, client = _run(["product", "update-price", "--id", "1"] + extra_args)
        assert result.exit_code == 0
        req = client.product.update_price.call_args[0][0]
        assert getattr(req, field) == expected

    def test_product_confirm_options(self):
        result, client = _run(["product", "confirm", "--product-id", "50", "--product-external-reference", "prod-1"])
        assert result.exit_code == 0
        req = client.product.confirm_product.call_args[0][0]
        assert req.product_external_reference == "prod-1"

    def test_product_attach_ticket(self):
        result, client = _run(
            [
                "product",
                "attach-ticket",
                "--transport-product-id",
                "50",
                "--ticket-id",
                "100",
            ]
        )
        assert result.exit_code == 0
        req = client.product.attach_ticket_to_transport_product.call_args[0][0]
        assert req.transport_product_id == 50
        assert req.ticket_id == 100

    def test_product_detach_ticket(self):
        result, client = _run(
            [
                "product",
                "detach-ticket",
                "--transport-product-id",
                "50",
                "--ticket-id",
                "100",
            ]
        )
        assert result.exit_code == 0
        client.product.delete_detach_ticket_from_transport_product.assert_awaited_once_with(
            transport_product_id=50,
            transport_product_external_reference=None,
            ticket_id=100,
            ticket_external_reference=None,
        )

    def test_product_get_tickets(self):
        result, client = _run(["product", "get-tickets", "--transport-product-id", "50"])
        assert result.exit_code == 0
        client.product.get_tickets_for_transport_product.assert_awaited_once_with(transport_product_id=50)

    def test_product_get_tickets_by_ref(self):
        result, client = _run(["product", "get-tickets-by-ref", "--transport-product-external-reference", "tp-1"])
        assert result.exit_code == 0
        client.product.get_tickets_for_transport_product_by_external_reference.assert_awaited_once_with(
            transport_product_external_reference="tp-1",
        )


class TestProductGroupCommands:
    def test_product_group_list(self):
        result, client = _run(["product-group", "list", "--offer-id", "789"])
        assert result.exit_code == 0
        client.product_group.get_all_for_offer.assert_awaited_once_with(offer_id=789)

    def test_product_group_create(self):
        result, client = _run(["product-group", "create", "--offer-id", "789", "--name", "Accommodation"])
        assert result.exit_code == 0
        req = client.product_group.create.call_args[0][0]
        assert req.offer_id == 789
        assert req.name == "Accommodation"

    @pytest.mark.parametrize(
        "extra_args,field,expected",
        [
            (["--offer-external-reference", "off-1"], "offer_external_reference", "off-1"),
            (["--offer-design-template", "1"], "offer_design_template", 1),
            (["--hide-all-products"], "hide_all_products", True),
            (["--must-select-all-products"], "must_select_all_products", True),
            (["--hide-product-prices"], "hide_product_prices", True),
            (["--show-total-price-for-group"], "show_total_price_for_group", True),
            (["--show-total-price-per-person"], "show_total_price_per_person", True),
            (["--number-of-persons-in-total-price", "4"], "number_of_persons_in_total_price", 4),
            (["--hide-price-table"], "hide_price_table", True),
            (["--custom-total-row-text", "Total"], "custom_total_row_text", "Total"),
            (["--name-on-invoice", "Accom"], "name_on_invoice", "Accom"),
            (["--hide-feedback-on-offer"], "hide_feedback_on_offer", True),
        ],
    )
    def test_product_group_create_options(self, extra_args, field, expected):
        result, client = _run(["product-group", "create", "--offer-id", "789", "--name", "Test"] + extra_args)
        assert result.exit_code == 0
        req = client.product_group.create.call_args[0][0]
        assert getattr(req, field) == expected

    @pytest.mark.parametrize(
        "extra_args,field,expected",
        [
            (["--introduction", "Welcome"], "introduction", "Welcome"),
            (["--description", "Details"], "description", "Details"),
            (["--offer-design-template", "1"], "offer_design_template", 1),
            (["--hide-all-products"], "hide_all_products", True),
            (["--must-select-all-products"], "must_select_all_products", True),
            (["--hide-product-prices"], "hide_product_prices", True),
            (["--show-total-price-for-group"], "show_total_price_for_group", True),
            (["--show-total-price-per-person"], "show_total_price_per_person", True),
            (["--number-of-persons-in-total-price", "4"], "number_of_persons_in_total_price", 4),
            (["--hide-price-table"], "hide_price_table", True),
            (["--custom-total-row-text", "Total"], "custom_total_row_text", "Total"),
            (["--name-on-invoice", "Accom"], "name_on_invoice", "Accom"),
            (["--hide-feedback-on-offer"], "hide_feedback_on_offer", True),
        ],
    )
    def test_product_group_update_options(self, extra_args, field, expected):
        result, client = _run(["product-group", "update", "--id", "1"] + extra_args)
        assert result.exit_code == 0
        req = client.product_group.update.call_args[0][0]
        assert getattr(req, field) == expected


class TestSupplierCommands:
    def test_supplier_get(self):
        result, client = _run(["supplier", "get", "101"])
        assert result.exit_code == 0
        client.supplier.get.assert_awaited_once_with(101)

    def test_supplier_list(self):
        result, client = _run(["supplier", "list", "--office-id", "1"])
        assert result.exit_code == 0
        client.supplier.get_all.assert_awaited_once_with(office_id=1)

    @pytest.mark.parametrize(
        "extra_args,field,expected",
        [
            (["--address", "Main St 1"], "address", "Main St 1"),
            (["--address2", "Suite 5"], "address2", "Suite 5"),
            (["--zip-code", "0150"], "zip_code", "0150"),
            (["--organisation-number", "123456789"], "organisation_number", "123456789"),
            (["--vat-number", "NO123456789"], "vat_number", "NO123456789"),
            (["--phone-number", "+4712345678"], "phone_number", "+4712345678"),
            (["--fax-number", "+4787654321"], "fax_number", "+4787654321"),
            (["--status", "1"], "status", 1),
            (["--chain", "Hilton"], "chain", "Hilton"),
            (["--brand", "DoubleTree"], "brand", "DoubleTree"),
            (["--supplier-number", "S001"], "supplier_number", "S001"),
            (["--is-internal-supplier"], "is_internal_supplier", True),
            (["--invoice-address-enabled"], "invoice_address_enabled", True),
            (["--invoice-address", "Invoice St 1"], "invoice_address", "Invoice St 1"),
            (["--invoice-address2", "Box 99"], "invoice_address2", "Box 99"),
            (["--invoice-zip-code", "0160"], "invoice_zip_code", "0160"),
            (["--invoice-city", "Oslo"], "invoice_city", "Oslo"),
            (["--invoice-country-code", "NO"], "invoice_country_code", "NO"),
            (["--invoice-additional-information", "Attn: AP"], "invoice_additional_information", "Attn: AP"),
            (["--supplier-category-id", "5"], "supplier_category_id", 5),
            (["--remarks", "Preferred"], "remarks", "Preferred"),
        ],
    )
    def test_supplier_create_options(self, extra_args, field, expected):
        result, client = _run(["supplier", "create", "--name", "Test"] + extra_args)
        assert result.exit_code == 0
        req = client.supplier.create.call_args[0][0]
        assert getattr(req, field) == expected

    @pytest.mark.parametrize(
        "extra_args,field,expected",
        [
            (["--name", "Updated"], "name", "Updated"),
            (["--external-reference", "ext-1"], "external_reference", "ext-1"),
            (["--email", "a@b.com"], "email", "a@b.com"),
            (["--city", "Oslo"], "city", "Oslo"),
            (["--country-code", "NO"], "country_code", "NO"),
            (["--address", "Main St 1"], "address", "Main St 1"),
            (["--address2", "Suite 5"], "address2", "Suite 5"),
            (["--zip-code", "0150"], "zip_code", "0150"),
            (["--organisation-number", "123456789"], "organisation_number", "123456789"),
            (["--vat-number", "NO123456789"], "vat_number", "NO123456789"),
            (["--phone-number", "+4712345678"], "phone_number", "+4712345678"),
            (["--fax-number", "+4787654321"], "fax_number", "+4787654321"),
            (["--status", "1"], "status", 1),
            (["--chain", "Hilton"], "chain", "Hilton"),
            (["--brand", "DoubleTree"], "brand", "DoubleTree"),
            (["--supplier-number", "S001"], "supplier_number", "S001"),
            (["--is-internal-supplier"], "is_internal_supplier", True),
            (["--invoice-address-enabled"], "invoice_address_enabled", True),
            (["--invoice-address", "Invoice St 1"], "invoice_address", "Invoice St 1"),
            (["--invoice-address2", "Box 99"], "invoice_address2", "Box 99"),
            (["--invoice-zip-code", "0160"], "invoice_zip_code", "0160"),
            (["--invoice-city", "Oslo"], "invoice_city", "Oslo"),
            (["--invoice-country-code", "NO"], "invoice_country_code", "NO"),
            (["--invoice-additional-information", "Attn: AP"], "invoice_additional_information", "Attn: AP"),
            (["--supplier-category-id", "5"], "supplier_category_id", 5),
            (["--remarks", "Preferred"], "remarks", "Preferred"),
        ],
    )
    def test_supplier_update_options(self, extra_args, field, expected):
        result, client = _run(["supplier", "update", "--id", "1"] + extra_args)
        assert result.exit_code == 0
        req = client.supplier.update.call_args[0][0]
        assert getattr(req, field) == expected


class TestContactPersonCommands:
    def test_contact_person_get(self):
        result, client = _run(["contact-person", "get", "10"])
        assert result.exit_code == 0
        client.contact_person.get.assert_awaited_once_with(10)

    def test_contact_person_delete_by_email(self):
        result, client = _run(["contact-person", "delete-by-email", "--email", "x@y.com"])
        assert result.exit_code == 0
        client.contact_person.delete_by_email.assert_awaited_once_with(email="x@y.com")

    @pytest.mark.parametrize(
        "extra_args,field,expected",
        [
            (["--phone-country-code", "+47"], "phone_country_code", "+47"),
            (["--phone-country-code2", "+46"], "phone_country_code2", "+46"),
            (["--phone-number2", "87654321"], "phone_number2", "87654321"),
        ],
    )
    def test_contact_person_create_options(self, extra_args, field, expected):
        result, client = _run(["contact-person", "create", "--first-name", "John"] + extra_args)
        assert result.exit_code == 0
        req = client.contact_person.create.call_args[0][0]
        assert getattr(req, field) == expected

    @pytest.mark.parametrize(
        "extra_args,field,expected",
        [
            (["--phone-country-code", "+47"], "phone_country_code", "+47"),
            (["--phone-country-code2", "+46"], "phone_country_code2", "+46"),
            (["--phone-number2", "87654321"], "phone_number2", "87654321"),
        ],
    )
    def test_contact_person_update_options(self, extra_args, field, expected):
        result, client = _run(["contact-person", "update", "--id", "1"] + extra_args)
        assert result.exit_code == 0
        req = client.contact_person.update.call_args[0][0]
        assert getattr(req, field) == expected

    def test_contact_person_update_customer_relation(self):
        result, client = _run(
            [
                "contact-person",
                "update-customer-relation",
                "--contact-person-id",
                "10",
                "--customer-id",
                "20",
                "--is-active",
            ]
        )
        assert result.exit_code == 0
        req = client.contact_person.update_customer_relation.call_args[0][0]
        assert req.contact_person_id == 10
        assert req.customer_id == 20
        assert req.is_active is True

    def test_contact_person_update_supplier_relation(self):
        result, client = _run(
            [
                "contact-person",
                "update-supplier-relation",
                "--contact-person-id",
                "10",
                "--supplier-id",
                "30",
                "--is-active",
            ]
        )
        assert result.exit_code == 0
        req = client.contact_person.update_supplier_relation.call_args[0][0]
        assert req.contact_person_id == 10
        assert req.supplier_id == 30
        assert req.is_active is True


class TestOfficeCommands:
    def test_office_list(self):
        result, client = _run(["office", "list"])
        assert result.exit_code == 0
        client.office.get_all.assert_awaited_once()
        parsed = json.loads(result.output)
        assert len(parsed) == 1
        assert parsed[0]["name"] == "Oslo"

    def test_office_categories(self):
        result, client = _run(["office", "categories", "--office-id", "1"])
        assert result.exit_code == 0
        client.office.get_all_customer_categories.assert_awaited_once_with(office_id=1)


class TestStatisticsCommands:
    def test_offer_sales(self):
        result, client = _run(["statistics", "offer-sales", "--office-id", "1"])
        assert result.exit_code == 0
        client.statistics.get_offer_sales.assert_awaited_once_with(office_id=1, project_id=None)


class TestRawOutput:
    def test_offer_get_raw(self):
        result, _ = _run(["offer", "get", "789", "--raw"])
        assert result.exit_code == 0
        assert "\n" not in result.output.strip()  # compact JSON


class TestEnvFlag:
    def test_env_test(self):
        mock_client = _mock_client()

        class _FakeCtx:
            async def __aenter__(self):
                return mock_client

            async def __aexit__(self, *a):
                await mock_client.close()

        with (
            patch("qondor_cli._run.build_client", return_value=_FakeCtx()),
            patch("qondor_cli._run.resolve_config") as mock_config,
        ):
            mock_config.return_value = MagicMock(base_url="https://qondor.azure-api.net/Test", subscription_key="k")
            result = runner.invoke(app, ["office", "list", "--env", "test"], env={"QONDOR_SUBSCRIPTION_KEY": "k"})
        assert result.exit_code == 0


class TestErrorHandling:
    def test_sdk_error_exits_with_code_1(self):
        """SDK exceptions are caught, printed to stderr, and exit 1."""
        mock_client = _mock_client()
        mock_client.office.get_all = AsyncMock(side_effect=QondorApiError(404, "Not found"))

        class _FakeCtx:
            async def __aenter__(self):
                return mock_client

            async def __aexit__(self, *a):
                await mock_client.close()

        with patch("qondor_cli._run.build_client", return_value=_FakeCtx()):
            result = runner.invoke(app, ["office", "list"], env={"QONDOR_SUBSCRIPTION_KEY": "test-key"})

        assert result.exit_code == 1
        assert "Error" in result.output

    def test_system_exit_not_swallowed(self):
        """SystemExit (e.g. from missing config) passes through with its exit code."""
        mock_client = _mock_client()
        mock_client.office.get_all = AsyncMock(side_effect=SystemExit(2))

        class _FakeCtx:
            async def __aenter__(self):
                return mock_client

            async def __aexit__(self, *a):
                await mock_client.close()

        with patch("qondor_cli._run.build_client", return_value=_FakeCtx()):
            result = runner.invoke(app, ["office", "list"], env={"QONDOR_SUBSCRIPTION_KEY": "test-key"})

        assert result.exit_code == 2

    def test_validation_error_shows_field_errors(self):
        """QondorValidationError displays field-level error messages."""
        mock_client = _mock_client()
        err = QondorValidationError(400, "Validation failed", raw_response={"errors": {"Name": ["Name is required."]}})
        mock_client.office.get_all = AsyncMock(side_effect=err)

        class _FakeCtx:
            async def __aenter__(self):
                return mock_client

            async def __aexit__(self, *a):
                await mock_client.close()

        with patch("qondor_cli._run.build_client", return_value=_FakeCtx()):
            result = runner.invoke(app, ["office", "list"], env={"QONDOR_SUBSCRIPTION_KEY": "test-key"})

        assert result.exit_code == 1
        assert "Validation failed" in result.output or "400" in result.output

    def test_rate_limit_error_exits_with_code_1(self):
        """QondorRateLimitError is caught and exits 1."""
        mock_client = _mock_client()
        mock_client.office.get_all = AsyncMock(
            side_effect=QondorRateLimitError(429, "Too many requests", retry_after=5.0)
        )

        class _FakeCtx:
            async def __aenter__(self):
                return mock_client

            async def __aexit__(self, *a):
                await mock_client.close()

        with patch("qondor_cli._run.build_client", return_value=_FakeCtx()):
            result = runner.invoke(app, ["office", "list"], env={"QONDOR_SUBSCRIPTION_KEY": "test-key"})

        assert result.exit_code == 1
        assert "429" in result.output or "Too many" in result.output

    def test_server_error_exits_with_code_1(self):
        """QondorServerError is caught and exits 1."""
        mock_client = _mock_client()
        mock_client.office.get_all = AsyncMock(side_effect=QondorServerError(500, "Internal server error"))

        class _FakeCtx:
            async def __aenter__(self):
                return mock_client

            async def __aexit__(self, *a):
                await mock_client.close()

        with patch("qondor_cli._run.build_client", return_value=_FakeCtx()):
            result = runner.invoke(app, ["office", "list"], env={"QONDOR_SUBSCRIPTION_KEY": "test-key"})

        assert result.exit_code == 1
        assert "500" in result.output or "Internal" in result.output

    def test_missing_required_arg_shows_usage(self):
        """Missing required option exits 2 with usage hint."""
        result, _ = _run(["product", "create"])
        assert result.exit_code == 2
        assert "Missing" in result.output or "required" in result.output.lower()
