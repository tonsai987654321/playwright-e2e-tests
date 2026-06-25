import os
import pytest
from playwright.sync_api import sync_playwright
import allure
from pytest import hookimpl

# Load .env if present (local dev); in CI these come from repository secrets
try:
    from dotenv import load_dotenv
    load_dotenv()
except ImportError:
    pass

TEST_USER = {
    "email": os.environ["TEST_EMAIL"],
    "password": os.environ["TEST_PASSWORD"],
    "name": os.environ.get("TEST_NAME", "Test User"),
}

@hookimpl(hookwrapper=True)
def pytest_runtest_makereport(item, call):
    outcome = yield
    rep = outcome.get_result()
    setattr(item, f"rep_{rep.when}", rep)

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
    page.set_default_timeout(60000)
    yield page
    context.close()

@pytest.fixture(scope="function", autouse=True)
def attach_screenshot_on_failure(request, page):
    yield
    if hasattr(request.node, "rep_call") and request.node.rep_call.failed:
        allure.attach(
            page.screenshot(),
            name="failure-screenshot",
            attachment_type=allure.attachment_type.PNG,
        )
