"""
UI Testing: Navigation & Header Tests
Verifies page transitions, navbar links, announcements, and footer links.
"""

import pytest
from playwright.sync_api import sync_playwright, expect


def test_navbar_page_switching(live_server, screenshots_dir):
    with sync_playwright() as p:
        browser = p.chromium.launch(headless=True)
        page = browser.new_page()
        page.goto(live_server, wait_until="domcontentloaded")

        # Verify initial page is Home
        expect(page.locator('[data-testid="page-home"]')).to_be_visible()

        # Navigate to Shop
        page.locator('[data-testid="nav-shop"]').click()
        expect(page.locator('[data-testid="page-shop"]')).to_be_visible()
        expect(page.locator('[data-testid="page-home"]')).not_to_be_visible()

        # Navigate to Wishlist
        page.locator('[data-testid="wishlist-nav-btn"]').click()
        expect(page.locator('[data-testid="page-wishlist"]')).to_be_visible()

        # Navigate to Cart
        page.locator('[data-testid="footer-link-cart"]').click()
        expect(page.locator('[data-testid="page-cart"]')).to_be_visible()

        # Return to Home via Logo
        page.locator('[data-testid="header-logo"]').click()
        expect(page.locator('[data-testid="page-home"]')).to_be_visible()

        page.screenshot(path=f"{screenshots_dir}/ui_navigation_home.png")
        browser.close()


def test_announcement_bar_close(live_server):
    with sync_playwright() as p:
        browser = p.chromium.launch(headless=True)
        page = browser.new_page()
        page.goto(live_server, wait_until="domcontentloaded")

        top_bar = page.locator('[data-testid="top-bar"]')
        expect(top_bar).to_be_visible()

        # Click close button
        page.locator('[data-testid="top-bar-close"]').click()
        expect(top_bar).not_to_be_visible()

        browser.close()


def test_footer_explore_links(live_server):
    with sync_playwright() as p:
        browser = p.chromium.launch(headless=True)
        page = browser.new_page()
        page.goto(live_server, wait_until="domcontentloaded")

        # Click footer Shop link
        page.locator('[data-testid="footer-link-shop"]').click()
        expect(page.locator('[data-testid="page-shop"]')).to_be_visible()

        # Click footer Wishlist link
        page.locator('[data-testid="footer-link-wishlist"]').click()
        expect(page.locator('[data-testid="page-wishlist"]')).to_be_visible()

        browser.close()
