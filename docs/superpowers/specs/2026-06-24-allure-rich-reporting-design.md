# Allure Rich Reporting Design

**Date:** 2026-06-24
**Status:** Approved

## Goal

Add detailed reporting to existing Playwright/pytest/Allure suite so each test shows:
- What inputs were sent (form values, URLs, search terms, card details)
- What the web responded (XHR/API HTTP status + body)
- Screenshots at key steps and on failure

## Architecture

```
conftest.py          → failure screenshot fixture + pytest_runtest_makereport hook
pages/base_page.py   → new BasePage: XHR listener + screenshot helper
pages/*.py           → inherit BasePage, add @allure.step + self.screenshot() calls
tests/*.py           → unchanged
```

## Components

### `pages/base_page.py` (new)

`BasePage.__init__(page)`:
- Stores `self.page = page`
- Registers `page.on("response", self._capture_network)` to intercept all responses
- `_capture_network` filters out static assets (images, fonts, JS, CSS, woff) by checking `content-type` header and URL extension
- Qualifying responses get attached to Allure: `"{METHOD} {URL} → {status}"` as name, body as text/JSON attachment

`BasePage.screenshot(name)`:
- Calls `allure.attach(self.page.screenshot(), name=name, attachment_type=allure.attachment_type.PNG)`

### Page objects (`login_page.py`, `home_page.py`, `product_page.py`, `cart_page.py`, `checkout_page.py`)

- Inherit `BasePage`
- Public methods decorated with `@allure.step(...)` showing actual param values
- `login()` masks password: step shows `email={email}, password=****`
- `self.screenshot("after {action}")` called at end of each significant method

### `conftest.py`

- Add `pytest_runtest_makereport` hook to track pass/fail state per test
- Add autouse function-scoped fixture `attach_screenshot_on_failure` that checks `request.node.rep_call.failed` and attaches a failure screenshot

## What Appears in Allure Report

**Steps:**
- `Navigate to https://www.automationexercise.com/login`
- `Login: email=user@test.com, password=****`
- `Search: query=dress`
- `Fill card: name=Test User, number=4111...1111, cvc=123, month=01, year=2027`

**Attachments per step:**
- PNG screenshot after each key action
- Extra PNG on failure

**Network (XHR/API only):**
- `POST /api/login → 200` with response body
- Failed requests flagged separately

## Files Changed

| File | Change |
|------|--------|
| `pages/base_page.py` | New — BasePage class |
| `pages/login_page.py` | Inherit BasePage, add steps + screenshots |
| `pages/home_page.py` | Inherit BasePage, add steps + screenshots |
| `pages/product_page.py` | Inherit BasePage, add steps + screenshots |
| `pages/cart_page.py` | Inherit BasePage, add steps + screenshots |
| `pages/checkout_page.py` | Inherit BasePage, add steps + screenshots |
| `conftest.py` | Add failure screenshot fixture + hook |

## Out of Scope

- Changes to test files
- Static asset network capture
- Video recording
- Allure TestOps / live dashboard
