import allure
from pages.helpers import dismiss_ads
from pages.base_page import BasePage


class HomePage(BasePage):
    URL = "https://www.automationexercise.com/"
    PRODUCTS_URL = "https://www.automationexercise.com/products"
    SEARCH_INPUT = "#search_product"
    SEARCH_BUTTON = "#submit_search"
    PRODUCT_NAMES = ".productinfo > p"
    FIRST_PRODUCT_LINK = "a[href*='/product_details/']"

    def __init__(self, page):
        super().__init__(page)

    @allure.step("Navigate to home page")
    def navigate(self):
        self.page.goto(self.URL)
        self.page.wait_for_load_state("domcontentloaded")
        dismiss_ads(self.page)
        self.screenshot("after-navigate")

    @allure.step("Search: query={query}")
    def search(self, query: str):
        self.page.goto(self.PRODUCTS_URL)
        self.page.wait_for_load_state("domcontentloaded")
        dismiss_ads(self.page)
        self.page.locator(self.SEARCH_INPUT).fill(query)
        self.page.locator(self.SEARCH_BUTTON).click()
        self.screenshot("after-search")

    @allure.step("Get product names")
    def get_product_names(self) -> list:
        return self.page.locator(self.PRODUCT_NAMES).all_text_contents()

    @allure.step("Click first product")
    def click_first_product(self):
        self.page.locator(self.FIRST_PRODUCT_LINK).first.click()
        self.screenshot("after-click-first-product")
