"""
UI Testing: Forms, Quick View Modal & Order Placement
Verifies product quick view modal, coupon validation, checkout submission,
contact inquiries, and newsletter subscription.
"""

import pytest
from playwright.sync_api import sync_playwright, expect


def test_product_modal_interaction(live_server, screenshots_dir):
    with sync_playwright() as p:
        browser = p.chromium.launch(headless=True)
        page = browser.new_page()
        page.goto(live_server, wait_until="domcontentloaded")

        # Click Product 1 name to open quick view modal
        page.locator('[data-testid="product-name-1"]').click()
        modal = page.locator('[data-testid="product-modal"]')
        expect(modal).to_be_visible()

        # Check modal title & price
        expect(page.locator('[data-testid="modal-product-title"]')).to_contain_text("Silk Cashmere Trench Coat")
        expect(page.locator('[data-testid="modal-product-price"]')).to_contain_text("$199.00")

        # Increment quantity
        page.locator('[data-testid="modal-qty-plus"]').click()
        expect(page.locator('[data-testid="modal-qty-input"]')).to_have_value("2")

        # Add to bag
        page.locator('[data-testid="modal-add-to-bag-btn"]').click()
        expect(modal).not_to_be_visible()

        # Verify toast
        expect(page.locator('[data-testid="toast-success"]')).to_be_visible()

        page.screenshot(path=f"{screenshots_dir}/ui_product_modal_added.png")
        browser.close()


def test_coupon_application_valid_and_invalid(live_server):
    with sync_playwright() as p:
        browser = p.chromium.launch(headless=True)
        page = browser.new_page()
        page.goto(live_server, wait_until="domcontentloaded")

        # Put an item in cart
        page.evaluate("""() => {
            cart = [{ productId: 1, color: 'Camel', size: 'M', quantity: 1 }];
            saveStateToLocalStorage();
            renderCartPage();
        }""")

        page.locator('[data-testid="nav-shop"]').click()
        page.locator('[data-testid="footer-link-cart"]').click()

        coupon_input = page.locator('[data-testid="coupon-code-input"]')
        apply_btn = page.locator('[data-testid="apply-coupon-btn"]')

        # 1. Invalid coupon test
        coupon_input.fill("WRONGCODE99")
        apply_btn.click()
        expect(page.locator('[data-testid="toast-error"]')).to_be_visible()

        # 2. Valid coupon test (AURA10 - 10% OFF)
        coupon_input.fill("AURA10")
        apply_btn.click()
        expect(page.locator('[data-testid="toast-success"]')).to_be_visible()
        expect(page.locator('[data-testid="coupon-discount-row"]')).to_be_visible()
        expect(page.locator('[data-testid="cart-discount-val"]')).to_contain_text("-$19.90")

        browser.close()


def test_complete_checkout_order_flow(live_server, screenshots_dir):
    with sync_playwright() as p:
        browser = p.chromium.launch(headless=True)
        page = browser.new_page()
        page.goto(live_server, wait_until="domcontentloaded")

        # Setup 1 cart item
        page.evaluate("""() => {
            cart = [{ productId: 1, color: 'Camel', size: 'M', quantity: 1 }];
            saveStateToLocalStorage();
        }""")

        # Navigate to Checkout
        page.locator('[data-testid="footer-link-cart"]').click()
        page.locator('[data-testid="proceed-to-checkout-btn"]').click()
        expect(page.locator('[data-testid="page-checkout"]')).to_be_visible()

        # Fill shipping details
        page.locator('[data-testid="chk-first-name"]').fill("Sophia")
        page.locator('[data-testid="chk-last-name"]').fill("Vance")
        page.locator('[data-testid="chk-email"]').fill("sophia.vance@example.com")
        page.locator('[data-testid="chk-phone"]').fill("+1 (555) 234-5678")
        page.locator('[data-testid="chk-address"]').fill("742 Evergreen Terrace")
        page.locator('[data-testid="chk-city"]').fill("New York")
        page.locator('[data-testid="chk-state"]').fill("NY")
        page.locator('[data-testid="chk-zip"]').fill("10021")

        # Select COD payment method
        page.locator('[data-testid="opt-cod"]').click()

        # Submit order
        page.locator('[data-testid="place-order-btn"]').click()

        # Confirmation modal should appear
        success_modal = page.locator('[data-testid="order-success-modal"]')
        expect(success_modal).to_be_visible(timeout=8000)

        order_id_el = page.locator('[data-testid="success-order-id"]')
        expect(order_id_el).to_contain_text("#AUR-")

        page.screenshot(path=f"{screenshots_dir}/ui_order_success.png")

        # Click Continue Shopping
        page.locator('[data-testid="continue-shopping-btn"]').click()
        expect(success_modal).not_to_be_visible()
        expect(page.locator('[data-testid="page-home"]')).to_be_visible()

        browser.close()


def test_contact_and_newsletter_forms(live_server, screenshots_dir):
    with sync_playwright() as p:
        browser = p.chromium.launch(headless=True)
        page = browser.new_page()
        page.goto(live_server, wait_until="domcontentloaded")

        # 1. Contact Form
        page.locator('[data-testid="contact-name"]').fill("Lucas Gray")
        page.locator('[data-testid="contact-email"]').fill("lucas.gray@example.com")
        page.locator('[data-testid="contact-subject"]').fill("Custom Suit Inquiry")
        page.locator('[data-testid="contact-message"]').fill("I would like to inquire about silk cashmere tailoring options.")
        page.locator('[data-testid="contact-submit-btn"]').click()

        expect(page.locator('[data-testid="contact-status-msg"]')).to_contain_text("sent successfully", timeout=5000)

        # 2. Newsletter Form
        page.locator('[data-testid="newsletter-email"]').fill("lucas.vip@example.com")
        page.locator('[data-testid="newsletter-submit-btn"]').click()
        expect(page.locator('[data-testid="newsletter-status-msg"]')).to_contain_text("Successfully subscribed", timeout=5000)

        page.screenshot(path=f"{screenshots_dir}/ui_forms_submitted.png")
        browser.close()
