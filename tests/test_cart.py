from pages.home_page import HomePage
from pages.product_page import ProductPage
from pages.cart_page import CartPage


def test_add_item_to_cart(page):
    home = HomePage(page)
    home.navigate()
    home.search("dress")
    home.click_first_product()
    product = ProductPage(page)
    product.add_to_cart()
    product.continue_shopping()
    cart = CartPage(page)
    cart.navigate()
    assert cart.get_item_count() > 0


def test_remove_item_from_cart(page):
    home = HomePage(page)
    home.navigate()
    home.search("dress")
    home.click_first_product()
    product = ProductPage(page)
    product.add_to_cart()
    product.continue_shopping()
    cart = CartPage(page)
    cart.navigate()
    cart.remove_first_item()
    assert cart.is_empty()
