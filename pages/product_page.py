from pages.base_page import BasePage


class ProductPage(BasePage):
    PRODUCT_NAME = ".product-information h2"
    ADD_TO_CART = "button:has-text('Add to cart')"
    CONTINUE_SHOPPING = "button:has-text('Continue Shopping')"

    def __init__(self, page):
        super().__init__(page)

    def get_name(self) -> str:
        return self.page.locator(self.PRODUCT_NAME).text_content()

    def add_to_cart(self):
        self.page.locator(self.ADD_TO_CART).first.click()

    def continue_shopping(self):
        self.page.locator(self.CONTINUE_SHOPPING).click()
