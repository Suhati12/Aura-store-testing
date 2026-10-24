"""
Responsive Testing Suite
Validates layout across Mobile (375x667, 390x844), Tablet (768x1024),
Laptop (1366x768), and Desktop (1920x1080).
Asserts:
- No horizontal scrolling (scrollWidth <= innerWidth).
- Mobile hamburger menu toggle works properly.
- Shop filter drawer/sidebar adapts correctly.
- Captures full-page responsive screenshots.
"""

import pytest
from playwright.sync_api import sync_playwright, expect

VIEWPORTS = [
    {"name": "Mobile_Small", "width": 375, "height": 667, "is_mobile": True},
    {"name": "Mobile_Standard", "width": 390, "height": 844, "is_mobile": True},
    {"name": "Tablet", "width": 768, "height": 1024, "is_mobile": True},
    {"name": "Laptop", "width": 1366, "height": 768, "is_mobile": False},
    {"name": "Desktop_FullHD", "width": 1920, "height": 1080, "is_mobile": False},
]


@pytest.mark.parametrize("vp", VIEWPORTS)
def test_viewport_no_horizontal_overflow(live_server, screenshots_dir, vp):
    """Ensure no horizontal scrolling on any supported screen size."""
    with sync_playwright() as p:
        browser = p.chromium.launch(headless=True)
        context = browser.new_context(viewport={"width": vp["width"], "height": vp["height"]})
        page = context.new_page()
        page.goto(live_server, wait_until="domcontentloaded")
        page.wait_for_selector('[data-testid="header-logo"]')

        # Check horizontal overflow
        overflow_check = page.evaluate("""
            () => {
                const scrollWidth = document.documentElement.scrollWidth;
                const innerWidth = window.innerWidth;
                return {
                    hasOverflow: scrollWidth > innerWidth,
                    scrollWidth: scrollWidth,
                    innerWidth: innerWidth
                };
            }
        """)

        assert not overflow_check["hasOverflow"], (
            f"Horizontal overflow detected on {vp['name']} ({vp['width']}x{vp['height']}): "
            f"scrollWidth={overflow_check['scrollWidth']} > innerWidth={overflow_check['innerWidth']}"
        )

        # Capture screenshot for visual inspection
        screenshot_path = f"{screenshots_dir}/responsive_{vp['name'].lower()}_{vp['width']}.png"
        page.screenshot(path=screenshot_path, full_page=True)

        browser.close()


def test_mobile_hamburger_menu_toggle(live_server, screenshots_dir):
    """Verify hamburger menu expands and collapses on mobile viewports."""
    with sync_playwright() as p:
        browser = p.chromium.launch(headless=True)
        context = browser.new_context(viewport={"width": 390, "height": 844})
        page = context.new_page()
        page.goto(live_server, wait_until="domcontentloaded")

        menu_btn = page.locator('[data-testid="mobile-menu-btn"]')
        nav_menu = page.locator('[data-testid="nav-menu"]')

        expect(menu_btn).to_be_visible()

        # Click hamburger menu to open
        menu_btn.click()
        expect(nav_menu).to_have_class("nav-menu active")

        # Capture menu open screenshot
        page.screenshot(path=f"{screenshots_dir}/responsive_mobile_menu_open.png")

        # Click menu button again to collapse
        menu_btn.click()
        expect(nav_menu).not_to_have_class("nav-menu active")

        browser.close()


def test_shop_mobile_filter_toggle(live_server):
    """Verify shop sidebar filter toggle on tablet/mobile screens."""
    with sync_playwright() as p:
        browser = p.chromium.launch(headless=True)
        context = browser.new_context(viewport={"width": 768, "height": 1024})
        page = context.new_page()
        page.goto(live_server, wait_until="domcontentloaded")

        page.locator('[data-testid="mobile-menu-btn"]').click()
        page.locator('[data-testid="nav-shop"]').click()

        filter_btn = page.locator('[data-testid="mobile-filter-btn"]')
        expect(filter_btn).to_be_visible()

        # Toggle filter sidebar
        filter_btn.click()
        sidebar = page.locator('[data-testid="shop-sidebar"]')
        expect(sidebar).to_have_class("shop-sidebar active-mobile")

        browser.close()
