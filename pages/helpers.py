def dismiss_ads(page) -> None:
    """Close any ad overlay that may block element interaction on automationexercise.com."""
    try:
        page.locator("div#ad_position_box").wait_for(state="visible", timeout=3000)
        page.locator("#ad_closeButton").click(timeout=3000)
    except Exception:
        pass
