"""Qondor CLI — entry point."""

from __future__ import annotations

import typer

from .commands import (
    contact_person,
    customer,
    offer,
    office,
    product,
    product_group,
    project,
    statistics,
    supplier,
)

app = typer.Typer(name="qondor", help="CLI for calling the Qondor API.", no_args_is_help=True)

app.add_typer(offer.app, name="offer", help="Manage offers.")
app.add_typer(project.app, name="project", help="Manage projects.")
app.add_typer(customer.app, name="customer", help="Manage customers.")
app.add_typer(product.app, name="product", help="Manage products.")
app.add_typer(product_group.app, name="product-group", help="Manage product groups.")
app.add_typer(supplier.app, name="supplier", help="Manage suppliers.")
app.add_typer(contact_person.app, name="contact-person", help="Manage contact persons.")
app.add_typer(office.app, name="office", help="Office queries.")
app.add_typer(statistics.app, name="statistics", help="Statistics queries.")
