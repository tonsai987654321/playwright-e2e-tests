from pages.helpers import dismiss_ads


class HomePage:
    URL = "https://www.automationexercise.com/"
    PRODUCTS_URL = "https://www.automationexercise.com/products"
    SEARCH_INPUT = "#search_product"
    SEARCH_BUTTON = "#submit_search"
    PRODUCT_NAMES = ".productinfo > p"
    FIRST_PRODUCT_LINK = "a[href*='/product_details/']"

    def __init__(self, page):
        self.page = page

    def navigate(self):
        self.page.goto(self.URL)
        self.page.wait_for_load_state("domcontentloaded")
        dismiss_ads(self.page)

    def search(self, query: str):
        self.page.goto(self.PRODUCTS_URL)
        self.page.wait_for_load_state("domcontentloaded")
        dismiss_ads(self.page)
        self.page.locator(self.SEARCH_INPUT).fill(query)
        self.page.locator(self.SEARCH_BUTTON).click()

    def get_product_names(self) -> list:
        return self.page.locator(self.PRODUCT_NAMES).all_text_contents()

    def click_first_product(self):
        self.page.locator(self.FIRST_PRODUCT_LINK).first.click()
