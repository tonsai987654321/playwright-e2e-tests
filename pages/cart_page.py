from pages.helpers import dismiss_ads
from pages.base_page import BasePage


class CartPage(BasePage):
    URL = "https://www.automationexercise.com/view_cart"
    CART_ROWS = "#cart_info_table tbody tr"
    REMOVE_BUTTON = ".cart_quantity_delete"
    EMPTY_CART_MSG = "b:has-text('Cart is empty!')"

    def __init__(self, page):
        super().__init__(page)

    def navigate(self):
        self.page.goto(self.URL)
        self.page.wait_for_load_state("domcontentloaded")
        dismiss_ads(self.page)

    def get_item_count(self) -> int:
        return self.page.locator(self.CART_ROWS).count()

    def remove_first_item(self):
        self.page.locator(self.REMOVE_BUTTON).first.click()
        self.page.wait_for_selector(self.EMPTY_CART_MSG)

    def is_empty(self) -> bool:
        return self.page.locator(self.EMPTY_CART_MSG).is_visible()
