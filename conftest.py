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
