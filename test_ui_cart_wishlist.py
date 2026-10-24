"""
UI Testing: Cart & Wishlist Interaction Tests
Verifies adding/removing products, side drawer updates, quantity increment/decrement, and subtotal.
"""

import pytest
from playwright.sync_api import sync_playwright, expect


def test_wishlist_toggle(live_server, screenshots_dir):
    with sync_playwright() as p:
        browser = p.chromium.launch(headless=True)
        page = browser.new_page()
        page.goto(live_server, wait_until="domcontentloaded")

        # Clear existing wishlist in local storage and in-memory variable for a clean test
        page.evaluate("() => { wishlist = []; saveStateToLocalStorage(); updateHeaderBadges(); }")

        wishlist_count = page.locator('[data-testid="wishlist-count"]')
        expect(wishlist_count).to_have_text("0")

        # Click wishlist heart on Product 1
        page.locator('[data-testid="wishlist-btn-1"]').click()
        expect(wishlist_count).to_have_text("1")

        # Open Wishlist page
        page.locator('[data-testid="wishlist-nav-btn"]').click()
        wishlist_item = page.locator('[data-testid="wishlist-products-grid"] [data-testid="product-card-1"]')
        expect(wishlist_item).to_be_visible()

        # Remove from Wishlist
        page.locator('[data-testid="wishlist-products-grid"] [data-testid="wishlist-btn-1"]').click()
        expect(page.locator('[data-testid="wishlist-empty-state"]')).to_be_visible()
        expect(wishlist_count).to_have_text("0")

        page.screenshot(path=f"{screenshots_dir}/ui_wishlist_empty.png")
        browser.close()


def test_quick_add_and_cart_drawer(live_server, screenshots_dir):
    with sync_playwright() as p:
        browser = p.chromium.launch(headless=True)
        page = browser.new_page()
        page.goto(live_server, wait_until="domcontentloaded")

        # Reset cart in storage and in-memory
        page.evaluate("() => { cart = []; saveStateToLocalStorage(); updateHeaderBadges(); }")

        # Click Quick Add for Product 1 (Silk Cashmere Trench Coat, $199.00)
        page.locator('[data-testid="quick-add-btn-1"]').click()

        # Open drawer
        page.locator('[data-testid="cart-nav-btn"]').click()
        drawer = page.locator('[data-testid="cart-drawer"]')
        expect(drawer).to_be_visible()

        # Check cart item in drawer and drawer subtotal
        drawer_item = page.locator('[data-testid="drawer-cart-body"] [data-testid="cart-item-1"]')
        expect(drawer_item).to_be_visible()
        expect(page.locator('[data-testid="drawer-cart-subtotal"]')).to_have_text("$199.00")

        # Increment quantity inside drawer
        page.locator('[data-testid="drawer-cart-body"] [data-testid="qty-plus-0"]').click()
        expect(page.locator('[data-testid="drawer-cart-subtotal"]')).to_have_text("$398.00")

        # Close drawer
        page.locator('[data-testid="drawer-close-btn"]').click()
        expect(drawer).not_to_be_visible()

        page.screenshot(path=f"{screenshots_dir}/ui_cart_drawer.png")
        browser.close()
