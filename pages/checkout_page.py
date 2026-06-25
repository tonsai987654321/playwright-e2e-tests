import allure
from pages.base_page import BasePage
from pages.helpers import dismiss_ads


class CheckoutPage(BasePage):
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
        super().__init__(page)

    @allure.step("Proceed to checkout")
    def proceed_to_checkout(self):
        dismiss_ads(self.page)
        self.page.locator(self.PROCEED_TO_CHECKOUT).first.click()
        self.screenshot("after-proceed-to-checkout")

    @allure.step("Place order")
    def place_order(self):
        self.page.locator(self.PLACE_ORDER).click()
        self.screenshot("after-place-order")

    @allure.step("Fill card details: name={name}, number={number}, cvc={cvc}, month={month}, year={year}")
    def fill_card_details(self, name: str, number: str, cvc: str, month: str, year: str):
        self.page.locator(self.CARD_NAME).fill(name)
        self.page.locator(self.CARD_NUMBER).fill(number)
        self.page.locator(self.CARD_CVC).fill(cvc)
        self.page.locator(self.CARD_MONTH).fill(month)
        self.page.locator(self.CARD_YEAR).fill(year)
        self.screenshot("after-fill-card-details")

    @allure.step("Confirm payment")
    def confirm_payment(self):
        self.page.locator(self.PAY_BUTTON).click()
        self.screenshot("after-confirm-payment")

    @allure.step("Check if order is placed")
    def is_order_placed(self) -> bool:
        return self.page.locator(self.ORDER_CONFIRMATION).is_visible()

    @allure.step("Check if login prompt is visible")
    def login_prompt_visible(self) -> bool:
        return self.page.locator(self.LOGIN_PROMPT).is_visible()
