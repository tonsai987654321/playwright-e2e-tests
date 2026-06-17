# playwright-e2e-tests Design

**Date:** 2026-06-17  
**Status:** Approved

## Overview

Web UI automation framework targeting [automationexercise.com](https://www.automationexercise.com) — a public e-commerce demo site. Covers core happy paths and negative cases using Python + Playwright + Page Object Model. CI runs on push via GitHub Actions and publishes Allure HTML reports to GitHub Pages.

---

## Scope

### Flows covered

| File | Happy path | Negative case |
|---|---|---|
| `tests/test_login.py` | Valid credentials → logged in | Invalid credentials → error message |
| `tests/test_browse.py` | Search product → view detail | Search returns no results |
| `tests/test_cart.py` | Add item → appears in cart | View empty cart |
| `tests/test_checkout.py` | Full checkout flow → order placed | Bad form inputs → validation errors |

~20–25 test cases total.

---

## Architecture: Flat Page Object Model

One class per page. No inheritance. Selectors live only in page classes — tests never reference raw selectors.

### Project structure

```
playwright-e2e-tests/
├── pages/
│   ├── login_page.py
│   ├── home_page.py
│   ├── product_page.py
│   ├── cart_page.py
│   └── checkout_page.py
├── tests/
│   ├── test_login.py
│   ├── test_browse.py
│   ├── test_cart.py
│   └── test_checkout.py
├── conftest.py
├── requirements.txt
├── .github/
│   └── workflows/
│       └── ci.yml
└── docs/
    └── superpowers/specs/
```

### Page class pattern

Each page class holds:
- `URL` — page URL constant
- Selector constants (class-level)
- `navigate()` method
- Action methods that wrap Playwright calls

```python
class LoginPage:
    URL = "https://www.automationexercise.com/login"
    EMAIL_INPUT = "#form input[name='email']"
    PASSWORD_INPUT = "#form input[name='password']"
    LOGIN_BUTTON = "button[data-qa='login-button']"
    ERROR_MSG = "p:has-text('Your email or password is incorrect')"

    def __init__(self, page):
        self.page = page

    def navigate(self):
        self.page.goto(self.URL)

    def login(self, email, password):
        self.page.fill(self.EMAIL_INPUT, email)
        self.page.fill(self.PASSWORD_INPUT, password)
        self.page.click(self.LOGIN_BUTTON)

    def get_error_message(self):
        return self.page.locator(self.ERROR_MSG).text_content()
```

---

## Fixtures (conftest.py)

- `browser` — session-scoped, launches headless Chromium
- `page` — function-scoped, new context per test for isolation
- `TEST_USER` — shared dict with test account credentials

---

## CI / Allure Reporting

- Trigger: push or PR to `master`
- Runner: `ubuntu-latest`
- Steps: checkout → install deps → `playwright install chromium` → `pytest --alluredir=allure-results` → generate Allure report → deploy to `gh-pages` branch
- Live report URL: `https://tonsai987654321.github.io/playwright-e2e-tests/`
- History preserved across runs via `gh-pages` checkout before generation

---

## Dependencies (requirements.txt)

```
pytest
playwright
pytest-playwright
allure-pytest
```

---

## Conventions

- Selectors in page classes only — never in tests
- Relative imports only — repo is portable
- One test file per flow; happy path and negative case as separate functions within the same file
- Headless Chromium in CI; can run headed locally
