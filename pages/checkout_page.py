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
