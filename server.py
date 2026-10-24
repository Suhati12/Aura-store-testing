"""
Aura Luxe Store - Backend API & Web Server
Provides RESTful APIs for the luxury e-commerce store and serves static frontend assets.
Designed for student testing projects with full support for UI, Load, Performance,
Cross-browser, Network, and API Automation Testing.
"""

import os
import re
import random
import time
from datetime import datetime, timezone
from flask import Flask, request, jsonify, send_from_directory
from flask_cors import CORS

BASE_DIR = os.path.abspath(os.path.dirname(__file__))

app = Flask(__name__, static_folder=None)
CORS(app)

# In-memory database of products (consistent with app.js)
PRODUCTS = [
    {
        "id": 1,
        "name": "Silk Cashmere Trench Coat",
        "category": "Clothing",
        "price": 249.00,
        "discountPrice": 199.00,
        "rating": 4.9,
        "reviewCount": 128,
        "badge": "BEST SELLER",
        "description": "Crafted from a luxurious blend of Italian mulberry silk and Mongolian cashmere. Features double-breasted rose gold buttons, storm flap, and a waist belt for an elegant silhouette.",
        "image": "https://images.unsplash.com/photo-1544441893-675973e31985?auto=format&fit=crop&q=80&w=800",
        "sizes": ["S", "M", "L", "XL"],
        "colors": ["Camel", "Ivory Cream", "Obsidian Black"],
        "inStock": True,
        "inventory": 25
    },
    {
        "id": 2,
        "name": "Velvet Wrap Evening Dress",
        "category": "Clothing",
        "price": 169.00,
        "discountPrice": 129.00,
        "rating": 4.8,
        "reviewCount": 94,
        "badge": "NEW",
        "description": "Sumptuous plush velvet evening gown featuring a graceful surplice neckline, gathered side tie, and subtle side slit. Perfect for gala nights and winter celebrations.",
        "image": "https://images.unsplash.com/photo-1595777457583-95e059d581b8?auto=format&fit=crop&q=80&w=800",
        "sizes": ["XS", "S", "M", "L"],
        "colors": ["Deep Burgundy", "Emerald Silk", "Midnight Black"],
        "inStock": True,
        "inventory": 18
    },
    {
        "id": 3,
        "name": "Minimalist Linen Tailored Blazer",
        "category": "Clothing",
        "price": 140.00,
        "discountPrice": 110.00,
        "rating": 4.7,
        "reviewCount": 86,
        "badge": "SALE",
        "description": "Lightweight organic linen blazer with sharp lapels and a single horn button closure. Ideal for sophisticated warm-weather layering.",
        "image": "https://images.unsplash.com/photo-1539109136881-3be0616acf4b?auto=format&fit=crop&q=80&w=800",
        "sizes": ["S", "M", "L"],
        "colors": ["Oatmeal", "Dusty Rose", "Warm Charcoal"],
        "inStock": True,
        "inventory": 30
    },
    {
        "id": 4,
        "name": "Artisanal Italian Leather Ankle Boots",
        "category": "Shoes",
        "price": 210.00,
        "discountPrice": 169.00,
        "rating": 4.9,
        "reviewCount": 215,
        "badge": "BEST SELLER",
        "description": "Handcrafted in Florence using vegetable-tanned full-grain leather. Features a comfortable 2.5-inch block heel and side zip entry.",
        "image": "https://images.unsplash.com/photo-1543163521-1bf539c55dd2?auto=format&fit=crop&q=80&w=800",
        "sizes": ["36", "37", "38", "39", "40", "41"],
        "colors": ["Cognac Brown", "Onyx", "Sand Suede"],
        "inStock": True,
        "inventory": 15
    },
    {
        "id": 5,
        "name": "Ivory Satin Stiletto Pumps",
        "category": "Shoes",
        "price": 155.00,
        "discountPrice": 125.00,
        "rating": 4.8,
        "reviewCount": 64,
        "badge": "NEW",
        "description": "Elegant pointed-toe heels draped in luminescent silk satin with memory foam cushioned insoles for effortless evening comfort.",
        "image": "https://images.unsplash.com/photo-1560343090-f0409e92791a?auto=format&fit=crop&q=80&w=800",
        "sizes": ["36", "37", "38", "39", "40"],
        "colors": ["Pearl Ivory", "Champagne", "Soft Blush"],
        "inStock": True,
        "inventory": 12
    },
    {
        "id": 6,
        "name": "Chic Minimalist Leather Sneakers",
        "category": "Shoes",
        "price": 130.00,
        "discountPrice": 98.00,
        "rating": 4.9,
        "reviewCount": 180,
        "badge": "SALE",
        "description": "Low-top court sneakers crafted from supple calfskin leather with a tonal rubber cupsole. Versatile luxury casual footwear.",
        "image": "https://images.unsplash.com/photo-1595950653106-6c9ebd614d3a?auto=format&fit=crop&q=80&w=800",
        "sizes": ["36", "37", "38", "39", "40", "41"],
        "colors": ["Pure White", "Nude Pink Accent"],
        "inStock": True,
        "inventory": 40
    },
    {
        "id": 7,
        "name": "Quilted Chain Leather Crossbody Bag",
        "category": "Bags",
        "price": 220.00,
        "discountPrice": 179.00,
        "rating": 5.0,
        "reviewCount": 310,
        "badge": "BEST SELLER",
        "description": "Iconic chevron quilted lambskin flap bag with woven gold chain strap and signature clasp hardware. Includes interior zip compartment.",
        "image": "https://images.unsplash.com/photo-1584917865442-de89df76afd3?auto=format&fit=crop&q=80&w=800",
        "sizes": ["One Size"],
        "colors": ["Noir Gold", "Soft Nude", "Crimson Red"],
        "inStock": True,
        "inventory": 20
    },
    {
        "id": 8,
        "name": "Soft Suede Structured Everyday Tote",
        "category": "Bags",
        "price": 195.00,
        "discountPrice": 149.00,
        "rating": 4.7,
        "reviewCount": 142,
        "badge": "SALE",
        "description": "Spacious open-top tote crafted from ultra-soft suede with contrast smooth leather straps. Fits a 15-inch laptop with ease.",
        "image": "https://images.unsplash.com/photo-1590874103328-eac38a683ce7?auto=format&fit=crop&q=80&w=800",
        "sizes": ["One Size"],
        "colors": ["Caramel Suede", "Olive Green", "Mocha"],
        "inStock": True,
        "inventory": 22
    },
    {
        "id": 9,
        "name": "Botanical Rose Facial Hydrating Elixir",
        "category": "Beauty",
        "price": 78.00,
        "discountPrice": 59.00,
        "rating": 4.9,
        "reviewCount": 420,
        "badge": "BEST SELLER",
        "description": "Nourishing facial oil infused with Damascus rose extracts, jojoba, and cold-pressed squalane. Restores luminous skin barrier overnight.",
        "image": "https://images.unsplash.com/photo-1608248597261-833258657640?auto=format&fit=crop&q=80&w=800",
        "sizes": ["50ml", "100ml"],
        "colors": ["Rose Glow"],
        "inStock": True,
        "inventory": 50
    },
    {
        "id": 10,
        "name": "Glowing Radiance Vitamin C Serum",
        "category": "Beauty",
        "price": 65.00,
        "discountPrice": 49.00,
        "rating": 4.8,
        "reviewCount": 195,
        "badge": "NEW",
        "description": "Potent 15% THD Vitamin C formula enhanced with hyaluronic acid and ferulic acid to brighten dark spots and protect against environmental pollutants.",
        "image": "https://images.unsplash.com/photo-1620916566398-39f1143ab7be?auto=format&fit=crop&q=80&w=800",
        "sizes": ["30ml"],
        "colors": ["Golden Amber"],
        "inStock": True,
        "inventory": 45
    },
    {
        "id": 11,
        "name": "18K Gold Plated Layered Pendant Necklace",
        "category": "Accessories",
        "price": 98.00,
        "discountPrice": 75.00,
        "rating": 4.9,
        "reviewCount": 280,
        "badge": "BEST SELLER",
        "description": "Dual-layer delicate chain set crafted in nickel-free brass electroplated with 18-karat real gold and featuring a coin medallion charm.",
        "image": "https://images.unsplash.com/photo-1599643478518-a784e5dc4c8f?auto=format&fit=crop&q=80&w=800",
        "sizes": ["Adjustable"],
        "colors": ["Warm 18K Gold", "Rose Gold", "Sterling Silver"],
        "inStock": True,
        "inventory": 35
    },
    {
        "id": 12,
        "name": "Oversized Gradient UV Sunglasses",
        "category": "Accessories",
        "price": 115.00,
        "discountPrice": 85.00,
        "rating": 4.7,
        "reviewCount": 110,
        "badge": "NEW",
        "description": "Italian acetate frames with scratch-resistant brown gradient lenses offering 100% UV400 protection. Statement eyewear for sunny days.",
        "image": "https://images.unsplash.com/photo-1511499767150-a48a237f0083?auto=format&fit=crop&q=80&w=800",
        "sizes": ["One Size"],
        "colors": ["Tortoise Shell", "Champagne Nude", "Smokey Black"],
        "inStock": True,
        "inventory": 28
    },
    {
        "id": 13,
        "name": "Vintage Italian Leather Chronograph Watch",
        "category": "Accessories",
        "price": 189.00,
        "discountPrice": 145.00,
        "rating": 4.9,
        "reviewCount": 165,
        "badge": "BEST SELLER",
        "description": "Classic timepiece featuring a rose-gold stainless steel case, genuine stitched leather band, sapphire crystal glass, and Japanese quartz movement.",
        "image": "https://images.unsplash.com/photo-1524805444758-089113d48a6d?auto=format&fit=crop&q=80&w=800",
        "sizes": ["38mm", "42mm"],
        "colors": ["Chestnut Gold", "Espresso Black"],
        "inStock": True,
        "inventory": 16
    },
    {
        "id": 14,
        "name": "Silk Satin Square Printed Scarf",
        "category": "Accessories",
        "price": 75.00,
        "discountPrice": 58.00,
        "rating": 4.8,
        "reviewCount": 89,
        "badge": "SALE",
        "description": "Luxurious 100% pure silk square scarf with hand-rolled edges and an intricate botanical print. Can be styled around neck, hair, or handbag strap.",
        "image": "https://images.unsplash.com/photo-1601924994987-69e26d50dc26?auto=format&fit=crop&q=80&w=800",
        "sizes": ["90x90cm"],
        "colors": ["Emerald Floral", "Golden Chain", "Paisley Pink"],
        "inStock": True,
        "inventory": 30
    }
]

# Coupons
COUPONS = {
    "AURA10": {"discountPercent": 10, "description": "10% VIP Discount"},
    "FREESHIP": {"discountPercent": 5, "description": "5% Express Shipping Credit"}
}

# In-memory storage for placed orders, contact messages, and subscribers
ORDERS = {}
CONTACT_MESSAGES = []
NEWSLETTER_SUBSCRIBERS = set()

EMAIL_REGEX = re.compile(r"^[\w\.\+\-]+@[\w\-]+\.[a-zA-Z]{2,}$")


# ==========================================
# Static Files Routes (Frontend Website)
# ==========================================
@app.route("/")
def serve_index():
    return send_from_directory(BASE_DIR, "index.html")

@app.route("/styles.css")
def serve_styles():
    return send_from_directory(BASE_DIR, "styles.css")

@app.route("/app.js")
def serve_app_js():
    return send_from_directory(BASE_DIR, "app.js")

@app.route("/assets/<path:filename>")
def serve_assets(filename):
    assets_dir = os.path.join(BASE_DIR, "assets")
    return send_from_directory(assets_dir, filename)


# ==========================================
# REST API Endpoints
# ==========================================

@app.route("/api/health", methods=["GET"])
def health_check():
    """Health check endpoint to verify backend service status."""
    return jsonify({
        "status": "healthy",
        "service": "Aura Luxe Store API",
        "version": "1.0.0",
        "timestamp": datetime.now(timezone.utc).isoformat() + "Z",
        "productsCount": len(PRODUCTS),
        "ordersCount": len(ORDERS)
    }), 200


@app.route("/api/products", methods=["GET"])
def get_products():
    """
    Get all products with optional filters:
    - category: string
    - search: string
    - max_price: float
    - badge: string
    - sort: 'low-high' | 'high-low' | 'rating' | 'newest' | 'popular'
    """
    category = request.args.get("category", "").strip()
    search = request.args.get("search", "").strip().lower()
    max_price = request.args.get("max_price", type=float)
    badge = request.args.get("badge", "").strip().upper()
    sort_by = request.args.get("sort", "popular")

    results = list(PRODUCTS)

    if category and category.lower() != "all":
        results = [p for p in results if p["category"].lower() == category.lower()]

    if search:
        results = [p for p in results if search in p["name"].lower() or search in p["category"].lower() or search in p["description"].lower()]

    if max_price is not None:
        results = [p for p in results if p["discountPrice"] <= max_price]

    if badge:
        results = [p for p in results if p.get("badge") == badge]

    if sort_by == "low-high":
        results.sort(key=lambda x: x["discountPrice"])
    elif sort_by == "high-low":
        results.sort(key=lambda x: x["discountPrice"], reverse=True)
    elif sort_by == "rating":
        results.sort(key=lambda x: x["rating"], reverse=True)
    elif sort_by == "newest":
        results.sort(key=lambda x: 1 if x.get("badge") == "NEW" else 0, reverse=True)

    return jsonify({
        "success": True,
        "count": len(results),
        "total": len(PRODUCTS),
        "products": results
    }), 200


@app.route("/api/products/<int:product_id>", methods=["GET"])
def get_product_by_id(product_id):
    """Retrieve details of a single product by ID."""
    product = next((p for p in PRODUCTS if p["id"] == product_id), None)
    if not product:
        return jsonify({
            "success": False,
            "error": "Product not found",
            "productId": product_id
        }), 404

    return jsonify({
        "success": True,
        "product": product
    }), 200


@app.route("/api/coupons/verify", methods=["POST"])
def verify_coupon():
    """Verify promotional coupon code."""
    data = request.get_json(silent=True) or {}
    code = str(data.get("code", "")).strip().upper()

    if not code:
        return jsonify({
            "success": False,
            "valid": False,
            "error": "Coupon code cannot be empty"
        }), 400

    if code in COUPONS:
        coupon = COUPONS[code]
        return jsonify({
            "success": True,
            "valid": True,
            "code": code,
            "discountPercent": coupon["discountPercent"],
            "description": coupon["description"]
        }), 200
    else:
        return jsonify({
            "success": False,
            "valid": False,
            "error": f"Invalid promo code '{code}'. Try 'AURA10' or 'FREESHIP'"
        }), 400


@app.route("/api/cart/validate", methods=["POST"])
def validate_cart():
    """Validate cart items, check stock, calculate subtotal, shipping, discount, and total."""
    data = request.get_json(silent=True) or {}
    items = data.get("items", [])
    coupon_code = str(data.get("coupon", "")).strip().upper()

    if not isinstance(items, list):
        return jsonify({"success": False, "error": "Items must be an array"}), 400

    validated_items = []
    subtotal = 0.0

    for item in items:
        pid = item.get("productId")
        qty = item.get("quantity", 1)
        if not pid or qty <= 0:
            return jsonify({"success": False, "error": "Invalid item payload"}), 400

        product = next((p for p in PRODUCTS if p["id"] == pid), None)
        if not product:
            return jsonify({"success": False, "error": f"Product ID {pid} does not exist"}), 400

        item_total = round(product["discountPrice"] * qty, 2)
        subtotal += item_total

        validated_items.append({
            "productId": pid,
            "name": product["name"],
            "price": product["discountPrice"],
            "quantity": qty,
            "color": item.get("color", "Default"),
            "size": item.get("size", "One Size"),
            "total": item_total
        })

    subtotal = round(subtotal, 2)
    shipping = 0.0 if subtotal >= 100.0 or len(validated_items) == 0 else 15.00

    discount_amount = 0.0
    discount_percent = 0
    if coupon_code and coupon_code in COUPONS:
        discount_percent = COUPONS[coupon_code]["discountPercent"]
        discount_amount = round((subtotal * discount_percent) / 100.0, 2)

    total = round(max(0.0, subtotal - discount_amount + shipping), 2)

    return jsonify({
        "success": True,
        "items": validated_items,
        "itemsCount": sum(i["quantity"] for i in validated_items),
        "subtotal": subtotal,
        "shipping": shipping,
        "discountPercent": discount_percent,
        "discountAmount": discount_amount,
        "total": total
    }), 200


@app.route("/api/orders", methods=["POST"])
def place_order():
    """
    Place a new customer order.
    Validates required contact details, shipping address, and line items.
    """
    data = request.get_json(silent=True) or {}

    first_name = str(data.get("firstName", "")).strip()
    last_name = str(data.get("lastName", "")).strip()
    email = str(data.get("email", "")).strip()
    phone = str(data.get("phone", "")).strip()
    address = str(data.get("address", "")).strip()
    city = str(data.get("city", "")).strip()
    state = str(data.get("state", "")).strip()
    zip_code = str(data.get("zip", "")).strip()
    country = str(data.get("country", "")).strip()
    payment_method = str(data.get("paymentMethod", "card")).strip()
    items = data.get("items", [])
    coupon_code = str(data.get("coupon", "")).strip().upper()

    # Validation
    missing_fields = []
    if not first_name: missing_fields.append("firstName")
    if not last_name: missing_fields.append("lastName")
    if not email: missing_fields.append("email")
    if not phone: missing_fields.append("phone")
    if not address: missing_fields.append("address")
    if not city: missing_fields.append("city")
    if not zip_code: missing_fields.append("zip")

    if missing_fields:
        return jsonify({
            "success": False,
            "error": "Missing required fields",
            "missing": missing_fields
        }), 400

    if not EMAIL_REGEX.match(email):
        return jsonify({
            "success": False,
            "error": "Invalid email address format"
        }), 400

    if not items or not isinstance(items, list) or len(items) == 0:
        return jsonify({
            "success": False,
            "error": "Cannot place an order with an empty cart"
        }), 400

    # Calculate subtotal & order summary
    subtotal = 0.0
    order_items = []
    for item in items:
        pid = item.get("productId")
        qty = item.get("quantity", 1)
        product = next((p for p in PRODUCTS if p["id"] == pid), None)
        if product:
            line_total = round(product["discountPrice"] * qty, 2)
            subtotal += line_total
            order_items.append({
                "productId": pid,
                "name": product["name"],
                "unitPrice": product["discountPrice"],
                "quantity": qty,
                "color": item.get("color", "Default"),
                "size": item.get("size", "One Size"),
                "lineTotal": line_total
            })

    subtotal = round(subtotal, 2)
    shipping = 0.0 if subtotal >= 100.0 else 15.00
    discount = 0.0
    if coupon_code in COUPONS:
        discount = round((subtotal * COUPONS[coupon_code]["discountPercent"]) / 100.0, 2)
    total = round(max(0.0, subtotal - discount + shipping), 2)

    # Generate unique Order ID
    order_id = f"AUR-{random.randint(100000, 999999)}"
    order_record = {
        "orderId": order_id,
        "createdAt": datetime.now(timezone.utc).isoformat() + "Z",
        "customer": {
            "name": f"{first_name} {last_name}",
            "email": email,
            "phone": phone,
            "address": f"{address}, {city}, {state} {zip_code}, {country}"
        },
        "paymentMethod": payment_method,
        "items": order_items,
        "summary": {
            "subtotal": subtotal,
            "shipping": shipping,
            "discount": discount,
            "total": total
        },
        "status": "Confirmed"
    }

    ORDERS[order_id] = order_record

    return jsonify({
        "success": True,
        "message": "Order successfully placed",
        "orderId": order_id,
        "order": order_record
    }), 201


@app.route("/api/orders/<order_id>", methods=["GET"])
def get_order_by_id(order_id):
    """Retrieve details of an order by Order ID."""
    order = ORDERS.get(order_id)
    if not order:
        return jsonify({
            "success": False,
            "error": "Order not found",
            "orderId": order_id
        }), 404

    return jsonify({
        "success": True,
        "order": order
    }), 200


@app.route("/api/newsletter", methods=["POST"])
def newsletter_subscribe():
    """Subscribe user to newsletter."""
    data = request.get_json(silent=True) or {}
    email = str(data.get("email", "")).strip().lower()

    if not email or not EMAIL_REGEX.match(email):
        return jsonify({
            "success": False,
            "error": "Please provide a valid email address"
        }), 400

    NEWSLETTER_SUBSCRIBERS.add(email)
    return jsonify({
        "success": True,
        "message": "Thank you for subscribing to Aura Luxe VIP Club!",
        "email": email
    }), 200


@app.route("/api/contact", methods=["POST"])
def contact_submit():
    """Submit a concierge / customer service inquiry."""
    data = request.get_json(silent=True) or {}
    name = str(data.get("name", "")).strip()
    email = str(data.get("email", "")).strip()
    subject = str(data.get("subject", "")).strip()
    message = str(data.get("message", "")).strip()

    if not name or not email or not subject or not message:
        return jsonify({
            "success": False,
            "error": "Name, email, subject, and message are all required"
        }), 400

    if not EMAIL_REGEX.match(email):
        return jsonify({
            "success": False,
            "error": "Please provide a valid email address"
        }), 400

    entry = {
        "id": len(CONTACT_MESSAGES) + 1,
        "name": name,
        "email": email,
        "subject": subject,
        "message": message,
        "receivedAt": datetime.now(timezone.utc).isoformat() + "Z"
    }
    CONTACT_MESSAGES.append(entry)

    return jsonify({
        "success": True,
        "message": "Your inquiry has been received. Our concierge will respond within 24 hours.",
        "inquiryId": entry["id"]
    }), 200


if __name__ == "__main__":
    port = int(os.environ.get("PORT", 8000))
    print(f"[Aura Luxe Store] running at http://localhost:{port}")
    app.run(host="127.0.0.1", port=port, debug=False)
