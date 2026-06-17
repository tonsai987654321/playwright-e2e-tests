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

    def search(self, query: str):
        self.page.goto(self.PRODUCTS_URL)
        self.page.fill(self.SEARCH_INPUT, query)
        self.page.click(self.SEARCH_BUTTON)

    def get_product_names(self) -> list:
        return self.page.locator(self.PRODUCT_NAMES).all_text_contents()

    def click_first_product(self):
        self.page.locator(self.FIRST_PRODUCT_LINK).first.click()
