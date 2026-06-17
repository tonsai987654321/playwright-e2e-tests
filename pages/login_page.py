from pages.helpers import dismiss_ads


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
        self.page.wait_for_load_state("domcontentloaded")
        dismiss_ads(self.page)

    def login(self, email: str, password: str):
        self.page.locator(self.EMAIL_INPUT).fill(email)
        self.page.locator(self.PASSWORD_INPUT).fill(password)
        self.page.locator(self.LOGIN_BUTTON).click()

    def get_error_message(self) -> str:
        return self.page.locator(self.ERROR_MSG).text_content()

    def is_logged_in(self) -> bool:
        return self.page.locator(self.LOGGED_IN_INDICATOR).is_visible()
