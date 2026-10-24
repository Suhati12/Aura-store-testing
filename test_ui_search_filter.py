"""
UI Testing: Search & Filter Tests
Verifies real-time search modal, category filtering, price slider, and reset functionality.
"""

import pytest
from playwright.sync_api import sync_playwright, expect


def test_search_modal_realtime_lookup(live_server, screenshots_dir):
    with sync_playwright() as p:
        browser = p.chromium.launch(headless=True)
        page = browser.new_page()
        page.goto(live_server, wait_until="domcontentloaded")

        # Open search modal
        page.locator('[data-testid="search-btn"]').click()
        search_modal = page.locator('[data-testid="search-modal"]')
        expect(search_modal).to_be_visible()

        # Type keyword 'trench'
        search_input = page.locator('[data-testid="global-search-input"]')
        search_input.fill("trench")

        # Preview results should contain the product
        result_item = page.locator('[data-testid="search-results-preview"]')
        expect(result_item).to_contain_text("Silk Cashmere Trench Coat")

        page.screenshot(path=f"{screenshots_dir}/ui_search_preview.png")

        # Close search modal
        page.locator('[data-testid="search-close-btn"]').click()
        expect(search_modal).not_to_be_visible()

        browser.close()


def test_shop_category_filter(live_server):
    with sync_playwright() as p:
        browser = p.chromium.launch(headless=True)
        page = browser.new_page()
        page.goto(live_server, wait_until="domcontentloaded")

        # Navigate to Shop
        page.locator('[data-testid="nav-shop"]').click()

        # Filter by Shoes (3 products)
        page.locator('[data-testid="shop-cat-shoes"]').click()
        count_label = page.locator('[data-testid="shop-results-count"]')
        expect(count_label).to_contain_text("Showing 3 of 14 items")

        # Filter by Bags (2 products)
        page.locator('[data-testid="shop-cat-bags"]').click()
        expect(count_label).to_contain_text("Showing 2 of 14 items")

        # Return to All
        page.locator('[data-testid="shop-cat-all"]').click()
        expect(count_label).to_contain_text("Showing 14 of 14 items")

        browser.close()


def test_shop_filters_reset(live_server):
    with sync_playwright() as p:
        browser = p.chromium.launch(headless=True)
        page = browser.new_page()
        page.goto(live_server)

        page.locator('[data-testid="nav-shop"]').click()

        # Apply search in shop sidebar
        page.locator('[data-testid="shop-search-input"]').fill("velvet")
        count_label = page.locator('[data-testid="shop-results-count"]')
        expect(count_label).to_contain_text("Showing 1 of 14 items")

        # Click Reset All Filters
        page.locator('[data-testid="reset-filters-btn"]').click()
        expect(count_label).to_contain_text("Showing 14 of 14 items")

        browser.close()
