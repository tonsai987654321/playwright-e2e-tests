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
        self.page.locator(self.PROCEED_TO_CHECKOUT).first.click()

    def place_order(self):
        self.page.locator(self.PLACE_ORDER).click()

    def fill_card_details(self, name: str, number: str, cvc: str, month: str, year: str):
        self.page.locator(self.CARD_NAME).fill(name)
        self.page.locator(self.CARD_NUMBER).fill(number)
        self.page.locator(self.CARD_CVC).fill(cvc)
        self.page.locator(self.CARD_MONTH).fill(month)
        self.page.locator(self.CARD_YEAR).fill(year)

    def confirm_payment(self):
        self.page.locator(self.PAY_BUTTON).click()

    def is_order_placed(self) -> bool:
        return self.page.locator(self.ORDER_CONFIRMATION).is_visible()

    def login_prompt_visible(self) -> bool:
        return self.page.locator(self.LOGIN_PROMPT).is_visible()
