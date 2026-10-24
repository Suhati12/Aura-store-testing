"""
Locustfile for Aura Luxe Store Load Testing
Simulates realistic concurrent virtual users browsing catalog, filtering,
validating carts, applying coupons, and placing orders.
"""

import random
from locust import HttpUser, task, between

SAMPLE_FIRST_NAMES = ["Sophia", "Elena", "Lucas", "Alexander", "Camille", "Liam", "Olivia"]
SAMPLE_LAST_NAMES = ["Vance", "Wright", "Montgomery", "Laurent", "Chen", "Dubois"]


class AuraLuxeShopper(HttpUser):
    wait_time = between(0.5, 1.5)

    @task(5)
    def browse_homepage(self):
        """Simulate loading the main storefront."""
        self.client.get("/", name="[Page] Homepage")

    @task(4)
    def fetch_products_catalog(self):
        """Simulate loading all products catalog."""
        self.client.get("/api/products", name="[API] Get All Products")

    @task(3)
    def filter_by_category(self):
        """Simulate filtering products by category."""
        category = random.choice(["Clothing", "Shoes", "Bags", "Beauty", "Accessories"])
        self.client.get(f"/api/products?category={category}", name="[API] Filter by Category")

    @task(3)
    def search_products(self):
        """Simulate user searching for products."""
        keyword = random.choice(["silk", "leather", "trench", "dress", "rose"])
        self.client.get(f"/api/products?search={keyword}", name="[API] Search Products")

    @task(3)
    def view_product_detail(self):
        """Simulate viewing single product quick-view modal."""
        product_id = random.randint(1, 14)
        self.client.get(f"/api/products/{product_id}", name="[API] Get Product Details")

    @task(2)
    def validate_cart_and_coupon(self):
        """Simulate calculating cart subtotal and discounts."""
        pid = random.randint(1, 14)
        payload = {
            "items": [
                {"productId": pid, "quantity": random.randint(1, 2), "color": "Default", "size": "M"}
            ],
            "coupon": "AURA10"
        }
        self.client.post("/api/cart/validate", json=payload, name="[API] Validate Cart")

    @task(1)
    def verify_coupon_code(self):
        """Simulate applying promo coupon."""
        self.client.post("/api/coupons/verify", json={"code": "AURA10"}, name="[API] Verify Coupon")

    @task(1)
    def place_order(self):
        """Simulate customer checkout."""
        first_name = random.choice(SAMPLE_FIRST_NAMES)
        last_name = random.choice(SAMPLE_LAST_NAMES)
        pid = random.randint(1, 14)

        order_data = {
            "firstName": first_name,
            "lastName": last_name,
            "email": f"{first_name.lower()}.{last_name.lower()}@testload.com",
            "phone": "+1 (555) 019-9988",
            "address": "450 Luxury Boulevard, Suite 100",
            "city": "New York",
            "state": "NY",
            "zip": "10001",
            "country": "United States",
            "paymentMethod": random.choice(["card", "cod", "paypal"]),
            "items": [
                {"productId": pid, "quantity": 1, "color": "Default", "size": "M"}
            ],
            "coupon": "AURA10"
        }
        self.client.post("/api/orders", json=order_data, name="[API] Place Order")
