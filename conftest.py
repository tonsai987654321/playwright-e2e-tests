import os
import pytest
from playwright.sync_api import sync_playwright

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
