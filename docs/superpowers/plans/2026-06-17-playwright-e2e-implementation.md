# playwright-e2e-tests Implementation Plan

> **For agentic workers:** REQUIRED SUB-SKILL: Use superpowers:subagent-driven-development (recommended) or superpowers:executing-plans to implement this plan task-by-task. Steps use checkbox (`- [ ]`) syntax for tracking.

**Goal:** Build a Playwright + Python E2E test suite for automationexercise.com covering login, browsing, cart, and checkout flows with Allure reporting published to GitHub Pages.

**Architecture:** Flat Page Object Model — one class per page holding selectors and action methods; tests call page objects only, never raw selectors. pytest fixtures in conftest.py provide browser and page isolation per test function.

**Tech Stack:** Python 3.12, Playwright, pytest, allure-pytest, GitHub Actions, GitHub Pages

## Global Constraints

- Python 3.12
- Selectors live only in page classes — never in test files
- Relative paths only — repo must be portable
- One test file per flow; happy and negative cases as separate functions in the same file
- Headless Chromium in CI; can run headed locally by passing `--headed` to pytest
- A test account must be pre-registered at automationexercise.com before running login/checkout tests — replace the placeholder credentials in `conftest.py`

---

## File Map

| File | Responsibility |
|---|---|
| `requirements.txt` | Pinned deps: pytest, playwright, pytest-playwright, allure-pytest |
| `pytest.ini` | Default addopts: `--alluredir=allure-results -v` |
| `conftest.py` | Session-scoped `browser` fixture, function-scoped `page` fixture, `TEST_USER` dict |
| `pages/__init__.py` | Empty — makes `pages` a package |
| `tests/__init__.py` | Empty — makes `tests` a package |
| `pages/login_page.py` | `LoginPage` — navigate, login, get_error_message, is_logged_in |
| `pages/home_page.py` | `HomePage` — navigate, search (internally navigates to /products), get_product_names, click_first_product |
| `pages/product_page.py` | `ProductPage` — get_name, add_to_cart, continue_shopping |
| `pages/cart_page.py` | `CartPage` — navigate, get_item_count, remove_first_item, is_empty |
| `pages/checkout_page.py` | `CheckoutPage` — proceed_to_checkout, place_order, fill_card_details, confirm_payment, is_order_placed, login_prompt_visible |
| `tests/test_login.py` | Valid login + invalid login |
| `tests/test_browse.py` | Search returns results + search no results |
| `tests/test_cart.py` | Add item to cart + remove item from cart |
| `tests/test_checkout.py` | Full checkout flow + checkout requires login |
| `.github/workflows/ci.yml` | Run tests on push, generate Allure report, deploy to GitHub Pages |

---

### Task 1: Project scaffolding

**Files:**
- Create: `requirements.txt`
- Create: `pytest.ini`
- Create: `conftest.py`
- Create: `pages/__init__.py`
- Create: `tests/__init__.py`

**Interfaces:**
- Produces: `browser` fixture (session-scoped Chromium), `page` fixture (function-scoped new context), `TEST_USER` dict with `email`, `password`, `name` keys

- [ ] **Step 1: Create `requirements.txt`**

```
pytest==8.3.5
playwright==1.49.1
pytest-playwright==0.6.2
allure-pytest==2.13.5
```

- [ ] **Step 2: Create `pytest.ini`**

```ini
[pytest]
addopts = --alluredir=allure-results -v
```

- [ ] **Step 3: Create `conftest.py`**

```python
import pytest
from playwright.sync_api import sync_playwright

TEST_USER = {
    "email": "your_test_email@example.com",  # pre-register this account at automationexercise.com
    "password": "YourPassword123!",
    "name": "Test User",
}

@pytest.fixture(scope="session")
def browser():
    with sync_playwright() as p:
        b = p.chromium.launch(headless=True)
        yield b
        b.close()

@pytest.fixture(scope="function")
def page(browser):
    context = browser.new_context()
    page = context.new_page()
    yield page
    context.close()
```

- [ ] **Step 4: Create empty package init files**

Create `pages/__init__.py` (empty) and `tests/__init__.py` (empty).

- [ ] **Step 5: Install dependencies and Chromium**

```bash
python -m venv .venv && source .venv/bin/activate
pip install -r requirements.txt
playwright install chromium
```

Expected: no errors, Chromium browser downloads successfully.

- [ ] **Step 6: Verify pytest collects zero tests**

```bash
pytest --collect-only
```

Expected: `no tests ran` — 0 items collected, no errors.

- [ ] **Step 7: Commit**

```bash
git add requirements.txt pytest.ini conftest.py pages/__init__.py tests/__init__.py
git commit -m "feat: scaffold project with fixtures and dependencies"
```

---

### Task 2: LoginPage + login tests

**Files:**
- Create: `pages/login_page.py`
- Create: `tests/test_login.py`

**Interfaces:**
- Consumes: `page` fixture and `TEST_USER` from `conftest.py`
- Produces: `LoginPage(page)` — `navigate()`, `login(email: str, password: str)`, `get_error_message() -> str`, `is_logged_in() -> bool`

- [ ] **Step 1: Write the failing tests**

```python
# tests/test_login.py
from conftest import TEST_USER
from pages.login_page import LoginPage


def test_login_valid(page):
    login = LoginPage(page)
    login.navigate()
    login.login(TEST_USER["email"], TEST_USER["password"])
    assert login.is_logged_in()


def test_login_invalid(page):
    login = LoginPage(page)
    login.navigate()
    login.login("wrong@example.com", "wrongpassword")
    assert "incorrect" in login.get_error_message().lower()
```

- [ ] **Step 2: Run to confirm import error**

```bash
pytest tests/test_login.py -v
```

Expected: `ImportError: cannot import name 'LoginPage' from 'pages.login_page'`

- [ ] **Step 3: Implement `LoginPage`**

```python
# pages/login_page.py
class LoginPage:
    URL = "https://www.automationexercise.com/login"
    EMAIL_INPUT = "input[data-qa='login-email']"
    PASSWORD_INPUT = "input[data-qa='login-password']"
    LOGIN_BUTTON = "button[data-qa='login-button']"
    ERROR_MSG = "p:has-text('Your email or password is incorrect!')"
    LOGGED_IN_INDICATOR = "a:has-text('Logout')"

    def __init__(self, page):
        self.page = page

    def navigate(self):
        self.page.goto(self.URL)

    def login(self, email: str, password: str):
        self.page.fill(self.EMAIL_INPUT, email)
        self.page.fill(self.PASSWORD_INPUT, password)
        self.page.click(self.LOGIN_BUTTON)

    def get_error_message(self) -> str:
        return self.page.locator(self.ERROR_MSG).text_content()

    def is_logged_in(self) -> bool:
        return self.page.locator(self.LOGGED_IN_INDICATOR).is_visible()
```

- [ ] **Step 4: Run tests to verify they pass**

```bash
pytest tests/test_login.py -v
```

Expected:
```
PASSED tests/test_login.py::test_login_valid
PASSED tests/test_login.py::test_login_invalid
```

- [ ] **Step 5: Commit**

```bash
git add pages/login_page.py tests/test_login.py
git commit -m "feat: add LoginPage and login tests"
```

---

### Task 3: HomePage + ProductPage + browse tests

**Files:**
- Create: `pages/home_page.py`
- Create: `pages/product_page.py`
- Create: `tests/test_browse.py`

**Interfaces:**
- Consumes: `page` fixture from `conftest.py`
- Produces:
  - `HomePage(page)` — `navigate()`, `search(query: str)`, `get_product_names() -> list[str]`, `click_first_product()`
  - `ProductPage(page)` — `get_name() -> str`, `add_to_cart()`, `continue_shopping()`

Note: `HomePage.search()` internally navigates to `/products` before searching — the search form only exists on the products listing page.

- [ ] **Step 1: Write the failing tests**

```python
# tests/test_browse.py
from pages.home_page import HomePage


def test_search_returns_results(page):
    home = HomePage(page)
    home.navigate()
    home.search("dress")
    names = home.get_product_names()
    assert len(names) > 0
    assert any("dress" in name.lower() for name in names)


def test_search_no_results(page):
    home = HomePage(page)
    home.navigate()
    home.search("xyznotaproduct999")
    names = home.get_product_names()
    assert len(names) == 0
```

- [ ] **Step 2: Run to confirm import error**

```bash
pytest tests/test_browse.py -v
```

Expected: `ImportError: cannot import name 'HomePage' from 'pages.home_page'`

- [ ] **Step 3: Implement `HomePage`**

```python
# pages/home_page.py
class HomePage:
    URL = "https://www.automationexercise.com/"
    PRODUCTS_URL = "https://www.automationexercise.com/products"
    SEARCH_INPUT = "#search_product"
    SEARCH_BUTTON = "#submit_search"
    PRODUCT_NAMES = ".productinfo > p"
    FIRST_PRODUCT_LINK = "a[href*='/product_details/']"

    def __init__(self, page):
        self.page = page

    def navigate(self):
        self.page.goto(self.URL)

    def search(self, query: str):
        self.page.goto(self.PRODUCTS_URL)
        self.page.fill(self.SEARCH_INPUT, query)
        self.page.click(self.SEARCH_BUTTON)

    def get_product_names(self) -> list:
        return self.page.locator(self.PRODUCT_NAMES).all_text_contents()

    def click_first_product(self):
        self.page.locator(self.FIRST_PRODUCT_LINK).first.click()
```

- [ ] **Step 4: Implement `ProductPage`**

```python
# pages/product_page.py
class ProductPage:
    PRODUCT_NAME = ".product-information h2"
    ADD_TO_CART = "button:has-text('Add to cart')"
    CONTINUE_SHOPPING = "button:has-text('Continue Shopping')"

    def __init__(self, page):
        self.page = page

    def get_name(self) -> str:
        return self.page.locator(self.PRODUCT_NAME).text_content()

    def add_to_cart(self):
        self.page.locator(self.ADD_TO_CART).first.click()

    def continue_shopping(self):
        self.page.locator(self.CONTINUE_SHOPPING).click()
```

- [ ] **Step 5: Run tests to verify they pass**

```bash
pytest tests/test_browse.py -v
```

Expected:
```
PASSED tests/test_browse.py::test_search_returns_results
PASSED tests/test_browse.py::test_search_no_results
```

- [ ] **Step 6: Commit**

```bash
git add pages/home_page.py pages/product_page.py tests/test_browse.py
git commit -m "feat: add HomePage, ProductPage, and browse tests"
```

---

### Task 4: CartPage + cart tests

**Files:**
- Create: `pages/cart_page.py`
- Create: `tests/test_cart.py`

**Interfaces:**
- Consumes: `page` fixture, `HomePage(page)` from Task 3, `ProductPage(page)` from Task 3
- Produces: `CartPage(page)` — `navigate()`, `get_item_count() -> int`, `remove_first_item()`, `is_empty() -> bool`

- [ ] **Step 1: Write the failing tests**

```python
# tests/test_cart.py
from pages.home_page import HomePage
from pages.product_page import ProductPage
from pages.cart_page import CartPage


def test_add_item_to_cart(page):
    home = HomePage(page)
    home.navigate()
    home.search("dress")
    home.click_first_product()
    product = ProductPage(page)
    product.add_to_cart()
    product.continue_shopping()
    cart = CartPage(page)
    cart.navigate()
    assert cart.get_item_count() > 0


def test_remove_item_from_cart(page):
    home = HomePage(page)
    home.navigate()
    home.search("dress")
    home.click_first_product()
    product = ProductPage(page)
    product.add_to_cart()
    product.continue_shopping()
    cart = CartPage(page)
    cart.navigate()
    cart.remove_first_item()
    assert cart.is_empty()
```

- [ ] **Step 2: Run to confirm import error**

```bash
pytest tests/test_cart.py -v
```

Expected: `ImportError: cannot import name 'CartPage' from 'pages.cart_page'`

- [ ] **Step 3: Implement `CartPage`**

```python
# pages/cart_page.py
class CartPage:
    URL = "https://www.automationexercise.com/view_cart"
    CART_ROWS = "#cart_info_table tbody tr"
    REMOVE_BUTTON = ".cart_quantity_delete"
    EMPTY_CART_MSG = "b:has-text('Cart is empty!')"

    def __init__(self, page):
        self.page = page

    def navigate(self):
        self.page.goto(self.URL)

    def get_item_count(self) -> int:
        return self.page.locator(self.CART_ROWS).count()

    def remove_first_item(self):
        self.page.locator(self.REMOVE_BUTTON).first.click()
        self.page.wait_for_timeout(500)

    def is_empty(self) -> bool:
        return self.page.locator(self.EMPTY_CART_MSG).is_visible()
```

- [ ] **Step 4: Run tests to verify they pass**

```bash
pytest tests/test_cart.py -v
```

Expected:
```
PASSED tests/test_cart.py::test_add_item_to_cart
PASSED tests/test_cart.py::test_remove_item_from_cart
```

- [ ] **Step 5: Commit**

```bash
git add pages/cart_page.py tests/test_cart.py
git commit -m "feat: add CartPage and cart tests"
```

---

### Task 5: CheckoutPage + checkout tests

**Files:**
- Create: `pages/checkout_page.py`
- Create: `tests/test_checkout.py`

**Interfaces:**
- Consumes: `page` fixture, `TEST_USER` from `conftest.py`, `LoginPage` (Task 2), `HomePage` (Task 3), `ProductPage` (Task 3), `CartPage` (Task 4)
- Produces: `CheckoutPage(page)` — `proceed_to_checkout()`, `place_order()`, `fill_card_details(name: str, number: str, cvc: str, month: str, year: str)`, `confirm_payment()`, `is_order_placed() -> bool`, `login_prompt_visible() -> bool`

- [ ] **Step 1: Write the failing tests**

```python
# tests/test_checkout.py
from conftest import TEST_USER
from pages.login_page import LoginPage
from pages.home_page import HomePage
from pages.product_page import ProductPage
from pages.cart_page import CartPage
from pages.checkout_page import CheckoutPage


def test_checkout_complete(page):
    login = LoginPage(page)
    login.navigate()
    login.login(TEST_USER["email"], TEST_USER["password"])

    home = HomePage(page)
    home.navigate()
    home.search("dress")
    home.click_first_product()

    product = ProductPage(page)
    product.add_to_cart()
    product.continue_shopping()

    cart = CartPage(page)
    cart.navigate()

    checkout = CheckoutPage(page)
    checkout.proceed_to_checkout()
    checkout.place_order()
    checkout.fill_card_details(
        name="Test User",
        number="4111111111111111",
        cvc="123",
        month="01",
        year="2027",
    )
    checkout.confirm_payment()
    assert checkout.is_order_placed()


def test_checkout_requires_login(page):
    # Add item to cart first — "Proceed to Checkout" only appears when cart has items
    home = HomePage(page)
    home.navigate()
    home.search("dress")
    home.click_first_product()
    product = ProductPage(page)
    product.add_to_cart()
    product.continue_shopping()
    cart = CartPage(page)
    cart.navigate()
    checkout = CheckoutPage(page)
    checkout.proceed_to_checkout()
    # Unauthenticated users see a modal with a Register / Login link
    assert checkout.login_prompt_visible()
```

- [ ] **Step 2: Run to confirm import error**

```bash
pytest tests/test_checkout.py -v
```

Expected: `ImportError: cannot import name 'CheckoutPage' from 'pages.checkout_page'`

- [ ] **Step 3: Implement `CheckoutPage`**

```python
# pages/checkout_page.py
class CheckoutPage:
    PROCEED_TO_CHECKOUT = "a:has-text('Proceed To Checkout')"
    PLACE_ORDER = "a:has-text('Place Order')"
    CARD_NAME = "input[data-qa='name-on-card']"
    CARD_NUMBER = "input[data-qa='card-number']"
    CARD_CVC = "input[data-qa='cvc']"
    CARD_MONTH = "input[data-qa='expiry-month']"
    CARD_YEAR = "input[data-qa='expiry-year']"
    PAY_BUTTON = "button[data-qa='pay-button']"
    ORDER_CONFIRMATION = "h2[data-qa='order-placed']"
    LOGIN_PROMPT = "a:has-text('Register / Login')"

    def __init__(self, page):
        self.page = page

    def proceed_to_checkout(self):
        self.page.locator(self.PROCEED_TO_CHECKOUT).click()

    def place_order(self):
        self.page.locator(self.PLACE_ORDER).click()

    def fill_card_details(self, name: str, number: str, cvc: str, month: str, year: str):
        self.page.fill(self.CARD_NAME, name)
        self.page.fill(self.CARD_NUMBER, number)
        self.page.fill(self.CARD_CVC, cvc)
        self.page.fill(self.CARD_MONTH, month)
        self.page.fill(self.CARD_YEAR, year)

    def confirm_payment(self):
        self.page.click(self.PAY_BUTTON)

    def is_order_placed(self) -> bool:
        return self.page.locator(self.ORDER_CONFIRMATION).is_visible()

    def login_prompt_visible(self) -> bool:
        return self.page.locator(self.LOGIN_PROMPT).is_visible()
```

- [ ] **Step 4: Run tests to verify they pass**

```bash
pytest tests/test_checkout.py -v
```

Expected:
```
PASSED tests/test_checkout.py::test_checkout_complete
PASSED tests/test_checkout.py::test_checkout_requires_login
```

- [ ] **Step 5: Run full suite**

```bash
pytest tests/ -v
```

Expected: all 10 tests PASSED.

- [ ] **Step 6: Commit**

```bash
git add pages/checkout_page.py tests/test_checkout.py
git commit -m "feat: add CheckoutPage and checkout tests"
```

---

### Task 6: GitHub Actions CI + Allure GitHub Pages

**Files:**
- Create: `.github/workflows/ci.yml`

**Interfaces:**
- Consumes: `allure-results/` directory produced by `pytest --alluredir=allure-results`
- Produces: live Allure report at `https://tonsai987654321.github.io/playwright-e2e-tests/`

- [ ] **Step 1: Create `.github/workflows/ci.yml`**

```yaml
name: E2E Tests

on:
  push:
    branches: [master]
  pull_request:
    branches: [master]

jobs:
  test:
    runs-on: ubuntu-latest

    steps:
      - uses: actions/checkout@v4

      - uses: actions/setup-python@v5
        with:
          python-version: "3.12"

      - name: Install dependencies
        run: |
          pip install -r requirements.txt
          playwright install chromium

      - name: Run tests
        run: pytest tests/ --alluredir=allure-results
        continue-on-error: true

      - name: Load previous Allure history
        uses: actions/checkout@v4
        with:
          ref: gh-pages
          path: gh-pages
        continue-on-error: true

      - name: Generate Allure report
        uses: simple-agi/allure-report-action@v1
        with:
          allure-results: allure-results
          allure-report: allure-report
          gh-pages: gh-pages

      - name: Deploy to GitHub Pages
        uses: peaceiris/actions-gh-pages@v4
        with:
          github_token: ${{ secrets.GITHUB_TOKEN }}
          publish_dir: allure-report
```

- [ ] **Step 2: Enable GitHub Pages in repo settings**

Go to `https://github.com/tonsai987654321/playwright-e2e-tests/settings/pages`:
- Source: **Deploy from a branch**
- Branch: `gh-pages` / `/ (root)`
- Click **Save**

- [ ] **Step 3: Commit and push**

```bash
git add .github/
git commit -m "ci: add GitHub Actions workflow with Allure GitHub Pages"
git push
```

- [ ] **Step 4: Verify CI run**

Go to `https://github.com/tonsai987654321/playwright-e2e-tests/actions`

Expected: workflow triggers, all steps complete, Allure report live at `https://tonsai987654321.github.io/playwright-e2e-tests/`
