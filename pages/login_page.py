import allure
from pages.helpers import dismiss_ads
from pages.base_page import BasePage


class LoginPage(BasePage):
    URL = "https://www.automationexercise.com/login"
    EMAIL_INPUT = "input[data-qa='login-email']"
    PASSWORD_INPUT = "input[data-qa='login-password']"
    LOGIN_BUTTON = "button[data-qa='login-button']"
    ERROR_MSG = "p:has-text('Your email or password is incorrect!')"
    LOGGED_IN_INDICATOR = "a:has-text('Logout')"

    def __init__(self, page):
        super().__init__(page)

    @allure.step("Navigate to login page")
    def navigate(self):
        self.page.goto(self.URL)
        self.page.wait_for_load_state("domcontentloaded")
        dismiss_ads(self.page)
        self.screenshot("after-navigate")

    @allure.step("Login: email={email}, password=****")
    def login(self, email: str, password: str):
        self.page.locator(self.EMAIL_INPUT).fill(email)
        self.page.locator(self.PASSWORD_INPUT).fill(password)
        self.page.locator(self.LOGIN_BUTTON).click()
        self.screenshot("after-login")

    @allure.step("Get error message")
    def get_error_message(self) -> str:
        return self.page.locator(self.ERROR_MSG).text_content()

    @allure.step("Check if logged in")
    def is_logged_in(self) -> bool:
        return self.page.locator(self.LOGGED_IN_INDICATOR).is_visible()
