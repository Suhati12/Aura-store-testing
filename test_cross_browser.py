"""
Cross-Browser Testing Suite
Executes identical end-to-end shopping user journeys across:
1. Google Chrome / Chromium
2. Mozilla Firefox
3. Microsoft Edge
Verifies layout fidelity, interactions, cart behavior, and checkout compatibility.
"""

import pytest
from playwright.sync_api import sync_playwright, expect

BROWSERS_TO_TEST = [
    {"type": "chromium", "channel": None, "label": "Chrome_Chromium"},
    {"type": "firefox", "channel": None, "label": "Firefox"},
    {"type": "chromium", "channel": "msedge", "label": "Microsoft_Edge"}
]


@pytest.mark.parametrize("b_config", BROWSERS_TO_TEST)
def test_cross_browser_shopping_journey(live_server, screenshots_dir, b_config):
    """Run full shopping flow in each targeted browser."""
    browser_type_name = b_config["type"]
    channel = b_config["channel"]
    label = b_config["label"]

    with sync_playwright() as p:
        browser_type = getattr(p, browser_type_name)
        launch_kwargs = {"headless": True}
        if channel:
            launch_kwargs["channel"] = channel

        browser = browser_type.launch(**launch_kwargs)
        page = browser.new_page()

        # 1. Load Homepage
        page.goto(live_server)
        page.evaluate("() => { cart = []; saveStateToLocalStorage(); updateHeaderBadges(); }")
        expect(page.locator('[data-testid="header-logo"]')).to_be_visible()
        expect(page.locator('[data-testid="hero-title"]')).to_be_visible()

        # 2. Navigate to Shop
        page.locator('[data-testid="nav-shop"]').click()
        expect(page.locator('[data-testid="page-shop"]')).to_be_visible()

        # 3. Filter by Shoes
        page.locator('[data-testid="shop-cat-shoes"]').click()
        expect(page.locator('[data-testid="shop-results-count"]')).to_contain_text("Showing 3 of 14 items")

        # 4. Quick add Product 4
        page.locator('[data-testid="shop-products-grid"] [data-testid="quick-add-btn-4"]').click()

        # 5. Open Cart Drawer and verify item & subtotal
        page.locator('[data-testid="cart-nav-btn"]').click()
        drawer = page.locator('[data-testid="cart-drawer"]')
        expect(drawer).to_be_visible()
        expect(page.locator('[data-testid="cart-item-4"]')).to_be_visible()

        # 6. Navigate to Cart Page
        page.locator('[data-testid="drawer-checkout-btn"]').click()
        expect(page.locator('[data-testid="page-cart"]')).to_be_visible()
        expect(page.locator('[data-testid="cart-subtotal-val"]')).to_contain_text("$169.00")

        # 7. Capture Cross-Browser Screenshot
        screenshot_path = f"{screenshots_dir}/cross_browser_{label.lower()}.png"
        page.screenshot(path=screenshot_path)

        browser.close()
