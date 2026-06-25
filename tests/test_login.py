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


def test_login_wrong_title(page):
    login = LoginPage(page)
    login.navigate()
    assert "Dashboard" in page.title(), f"Expected 'Dashboard' in title but got: {page.title()}"
