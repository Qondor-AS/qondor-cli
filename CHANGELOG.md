# Changelog

All notable changes to `qondor-cli` are documented in this file. The format is
based on [Keep a Changelog](https://keepachangelog.com/en/1.1.0/), and this
project adheres to [Semantic Versioning](https://semver.org/spec/v2.0.0.html).

## [0.1.0] - Unreleased

Initial public release.

### Added

- Typer-based CLI (`qondor`) wrapping `qondor-api-sdk`.
- Command groups: `offer`, `project`, `customer`, `product`, `product-group`,
  `supplier`, `contact-person`, `office`, `statistics`.
- Configuration via `QONDOR_SUBSCRIPTION_KEY` and `QONDOR_ENV` environment
  variables, or `--subscription-key/-k` and `--env/-e` flags.
- Rich-rendered table output with an opt-in `--raw` flag for compact JSON.
