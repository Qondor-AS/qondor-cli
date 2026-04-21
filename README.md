# qondor-cli

A command-line interface for the [Qondor API](https://qondor.com), built on
[Typer](https://typer.tiangolo.com/) and the
[`qondor-api-sdk`](https://pypi.org/project/qondor-api-sdk/).

## Install

```bash
pip install qondor-cli
```

Requires Python 3.12+.

## Configuration

The CLI reads credentials from environment variables (or equivalent flags):

| Variable                   | Required | Default | Description                                     |
| -------------------------- | -------- | ------- | ----------------------------------------------- |
| `QONDOR_SUBSCRIPTION_KEY`  | yes      | —       | Azure APIM subscription key for the Qondor API. |
| `QONDOR_ENV`               | no       | `prod`  | One of `prod`, `test`, `dev`.                   |

Every command also accepts `--subscription-key/-k` and `--env/-e` flags if you
prefer to pass them explicitly.

```bash
export QONDOR_SUBSCRIPTION_KEY="..."
export QONDOR_ENV="prod"
```

## Quick start

```bash
# List all top-level command groups.
qondor --help

# Fetch a single offer by ID (human-readable output).
qondor offer get 12345

# Same call, compact JSON suitable for piping into jq.
qondor offer get 12345 --raw | jq '.title'

# List offers for a project.
qondor offer list --project-id 678
```

## Command groups

- `qondor offer`          — offers and offer currencies
- `qondor project`        — projects
- `qondor customer`       — customers
- `qondor product`        — products
- `qondor product-group`  — product groups
- `qondor supplier`       — suppliers
- `qondor contact-person` — contact persons
- `qondor office`         — office queries
- `qondor statistics`     — statistics queries

Run `qondor <group> --help` for the sub-commands in each group.

## License

MIT. See [LICENSE](LICENSE).
