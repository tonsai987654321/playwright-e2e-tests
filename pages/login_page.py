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
