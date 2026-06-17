from pages.home_page import HomePage


def test_search_returns_results(page):
    home = HomePage(page)
    home.navigate()
    home.search("dress")
    names = home.get_product_names()
    assert len(names) > 0
    assert any("dress" in name.lower() for name in names)


def test_search_no_results(page):
    home = HomePage(page)
    home.navigate()
    home.search("xyznotaproduct999")
    names = home.get_product_names()
    assert len(names) == 0
