from conftest import TEST_USER
from pages.login_page import LoginPage
from pages.home_page import HomePage
from pages.product_page import ProductPage
from pages.cart_page import CartPage
from pages.checkout_page import CheckoutPage


def test_checkout_complete(page):
    login = LoginPage(page)
    login.navigate()
    login.login(TEST_USER["email"], TEST_USER["password"])
    assert login.is_logged_in()

    home = HomePage(page)
    home.navigate()
    home.search("dress")
    home.click_first_product()

    product = ProductPage(page)
    product.add_to_cart()
    product.continue_shopping()

    cart = CartPage(page)
    cart.navigate()

    checkout = CheckoutPage(page)
    checkout.proceed_to_checkout()
    checkout.place_order()
    checkout.fill_card_details(
        name="Test User",
        number="4111111111111111",
        cvc="123",
        month="01",
        year="2027",
    )
    checkout.confirm_payment()
    assert checkout.is_order_placed()


def test_checkout_requires_login(page):
    # Add item to cart first — "Proceed to Checkout" only appears when cart has items
    home = HomePage(page)
    home.navigate()
    home.search("dress")
    home.click_first_product()
    product = ProductPage(page)
    product.add_to_cart()
    product.continue_shopping()
    cart = CartPage(page)
    cart.navigate()
    checkout = CheckoutPage(page)
    checkout.proceed_to_checkout()
    # Unauthenticated users see a modal with a Register / Login link
    assert checkout.login_prompt_visible()
