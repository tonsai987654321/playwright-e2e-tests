# playwright-e2e-tests — Agent Context

## Purpose
Web UI automation framework for a public e-commerce demo site.

## Status
In Progress.

## Tech Stack
Playwright · Python · Page Object Model (POM) · GitHub Actions · Allure.

## Architecture Intent
Page Object Model: one class per page encapsulating selectors and actions; tests call
page objects, never raw selectors. CI runs the suite on push via GitHub Actions. Results
published as Allure HTML reports.

## Planned Layout (not yet created)
- `pages/` — page object classes (one per page)
- `tests/` — test specs
- `reports/` — generated Allure output
- `.github/workflows/` — CI pipeline
- `requirements.txt` — deps (playwright, pytest, allure-pytest)
- `conftest.py` — fixtures (browser, context, page)

## Conventions
- Relative paths only — repo is portable.
- Selectors live in page objects, not tests.
