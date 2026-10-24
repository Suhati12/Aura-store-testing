"""
Network Testing Suite
Validates application resilience under realistic network constraints:
1. Slow Internet / 3G Latency Throttling
2. Offline Mode
3. Server Fault (HTTP 500 Internal Server Error)
4. Request Abort / Timeout Simulation
5. Network Reconnection & Recovery
"""

import time
import pytest
from playwright.sync_api import sync_playwright, expect


def test_slow_network_simulation(live_server, screenshots_dir):
    """Test site behavior and rendering under slow internet (simulated 3G latency)."""
    with sync_playwright() as p:
        browser = p.chromium.launch(headless=True)
        context = browser.new_context()
        page = context.new_page()

        # Intercept and add 300ms simulated network latency to all requests
        def delayed_route(route):
            time.sleep(0.3)
            route.continue_()

        page.route("**/*", delayed_route)

        page.goto(live_server)
        expect(page.locator('[data-testid="header-logo"]')).to_be_visible(timeout=10000)
        expect(page.locator('[data-testid="home-products-grid"]')).to_be_visible()

        page.screenshot(path=f"{screenshots_dir}/network_slow_3g_loaded.png")
        browser.close()


def test_offline_mode_detection(live_server, screenshots_dir):
    """Verify application gracefully detects offline mode and displays offline banner."""
    with sync_playwright() as p:
        browser = p.chromium.launch(headless=True)
        context = browser.new_context()
        page = context.new_page()
        page.goto(live_server)

        # Trigger browser offline state
        context.set_offline(True)
        page.evaluate("() => window.dispatchEvent(new Event('offline'))")

        # Verify offline banner is displayed
        offline_banner = page.locator('[data-testid="network-status-banner"]')
        expect(offline_banner).to_be_visible()
        expect(offline_banner).to_contain_text("Offline Mode")

        page.screenshot(path=f"{screenshots_dir}/network_offline_banner.png")
        browser.close()


def test_network_recovery_reconnection(live_server, screenshots_dir):
    """Verify application detects network restoration when returning online."""
    with sync_playwright() as p:
        browser = p.chromium.launch(headless=True)
        context = browser.new_context()
        page = context.new_page()
        page.goto(live_server)

        # Go offline
        context.set_offline(True)
        page.evaluate("() => window.dispatchEvent(new Event('offline'))")
        banner = page.locator('[data-testid="network-status-banner"]')
        expect(banner).to_contain_text("Offline Mode")

        # Restore online connection
        context.set_offline(False)
        page.evaluate("() => window.dispatchEvent(new Event('online'))")

        # Verify recovery notification
        expect(banner).to_contain_text("restored")
        page.screenshot(path=f"{screenshots_dir}/network_reconnected.png")

        browser.close()


def test_server_500_error_graceful_handling(live_server, screenshots_dir):
    """Verify UI handles 500 server errors gracefully with an error toast instead of crashing."""
    with sync_playwright() as p:
        browser = p.chromium.launch(headless=True)
        context = browser.new_context()
        page = context.new_page()
        page.goto(live_server)

        # Intercept /api/orders and return HTTP 500 error
        page.route("**/api/orders", lambda route: route.fulfill(
            status=500,
            content_type="application/json",
            body='{"error": "Internal Payment Gateway Crash (HTTP 500)"}'
        ))

        # Setup cart item
        page.evaluate("""() => {
            cart = [{ productId: 1, color: 'Camel', size: 'M', quantity: 1 }];
            saveStateToLocalStorage();
        }""")

        # Go to checkout and attempt to submit order
        page.locator('[data-testid="footer-link-cart"]').click()
        page.locator('[data-testid="proceed-to-checkout-btn"]').click()

        page.locator('[data-testid="chk-first-name"]').fill("Test")
        page.locator('[data-testid="chk-last-name"]').fill("User")
        page.locator('[data-testid="chk-email"]').fill("test.error@example.com")
        page.locator('[data-testid="chk-phone"]').fill("1234567890")
        page.locator('[data-testid="chk-address"]').fill("123 Error St")
        page.locator('[data-testid="chk-city"]').fill("New York")
        page.locator('[data-testid="chk-state"]').fill("NY")
        page.locator('[data-testid="chk-zip"]').fill("10001")
        page.locator('[data-testid="opt-cod"]').click()

        # Click Place Order
        page.locator('[data-testid="place-order-btn"]').click()

        # UI should catch the 500 response and display error toast
        error_toast = page.locator('[data-testid="toast-error"]')
        expect(error_toast).to_be_visible()
        expect(error_toast).to_contain_text("Order failed")

        page.screenshot(path=f"{screenshots_dir}/network_500_handled.png")
        browser.close()


def test_request_abort_simulation(live_server):
    """Verify application handles network request connection drop/abort."""
    with sync_playwright() as p:
        browser = p.chromium.launch(headless=True)
        context = browser.new_context()
        page = context.new_page()
        page.goto(live_server)

        # Abort newsletter requests to simulate network drop
        page.route("**/api/newsletter", lambda route: route.abort("failed"))

        page.locator('[data-testid="newsletter-email"]').fill("test.abort@example.com")
        page.locator('[data-testid="newsletter-submit-btn"]').click()

        # Fallback handling should engage safely without crashing the page
        expect(page.locator('[data-testid="header-logo"]')).to_be_visible()

        browser.close()
