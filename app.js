/* ==========================================================================
   AURA LUXE - Application JavaScript Logic
   Includes: Products Database, State Management, LocalStorage Persistence,
   SPA Navigation, Filtering & Sorting, Cart Drawer, Wishlist, Quick View,
   Checkout Validation & API Order Processing, Network & Offline Detection.
   ========================================================================== */

// ==========================================
// 1. PRODUCT DATABASE (14 Sample Products)
// ==========================================
const PRODUCTS_DATA = [
  {
    id: 1,
    name: "Silk Cashmere Trench Coat",
    category: "Clothing",
    price: 249.00,
    discountPrice: 199.00,
    rating: 4.9,
    reviewCount: 128,
    badge: "BEST SELLER",
    description: "Crafted from a luxurious blend of Italian mulberry silk and Mongolian cashmere. Features double-breasted rose gold buttons, storm flap, and a waist belt for an elegant silhouette.",
    image: "https://images.unsplash.com/photo-1544441893-675973e31985?auto=format&fit=crop&q=80&w=800",
    thumbs: [
      "https://images.unsplash.com/photo-1544441893-675973e31985?auto=format&fit=crop&q=80&w=800",
      "https://images.unsplash.com/photo-1539109136881-3be0616acf4b?auto=format&fit=crop&q=80&w=800"
    ],
    sizes: ["S", "M", "L", "XL"],
    colors: ["#D8C3B0", "#F4EFEA", "#1E1B18"],
    colorNames: ["Camel", "Ivory Cream", "Obsidian Black"],
    inStock: true
  },
  {
    id: 2,
    name: "Velvet Wrap Evening Dress",
    category: "Clothing",
    price: 169.00,
    discountPrice: 129.00,
    rating: 4.8,
    reviewCount: 94,
    badge: "NEW",
    description: "Sumptuous plush velvet evening gown featuring a graceful surplice neckline, gathered side tie, and subtle side slit. Perfect for gala nights and winter celebrations.",
    image: "https://images.unsplash.com/photo-1595777457583-95e059d581b8?auto=format&fit=crop&q=80&w=800",
    thumbs: [
      "https://images.unsplash.com/photo-1595777457583-95e059d581b8?auto=format&fit=crop&q=80&w=800"
    ],
    sizes: ["XS", "S", "M", "L"],
    colors: ["#581825", "#0F382C", "#1E1B18"],
    colorNames: ["Deep Burgundy", "Emerald Silk", "Midnight Black"],
    inStock: true
  },
  {
    id: 3,
    name: "Minimalist Linen Tailored Blazer",
    category: "Clothing",
    price: 140.00,
    discountPrice: 110.00,
    rating: 4.7,
    reviewCount: 86,
    badge: "SALE",
    description: "Lightweight organic linen blazer with sharp lapels and a single horn button closure. Ideal for sophisticated warm-weather layering.",
    image: "https://images.unsplash.com/photo-1539109136881-3be0616acf4b?auto=format&fit=crop&q=80&w=800",
    thumbs: [
      "https://images.unsplash.com/photo-1539109136881-3be0616acf4b?auto=format&fit=crop&q=80&w=800"
    ],
    sizes: ["S", "M", "L"],
    colors: ["#EADCC9", "#C88A83", "#4A443E"],
    colorNames: ["Oatmeal", "Dusty Rose", "Warm Charcoal"],
    inStock: true
  },
  {
    id: 4,
    name: "Artisanal Italian Leather Ankle Boots",
    category: "Shoes",
    price: 210.00,
    discountPrice: 169.00,
    rating: 4.9,
    reviewCount: 215,
    badge: "BEST SELLER",
    description: "Handcrafted in Florence using vegetable-tanned full-grain leather. Features a comfortable 2.5-inch block heel and side zip entry.",
    image: "https://images.unsplash.com/photo-1543163521-1bf539c55dd2?auto=format&fit=crop&q=80&w=800",
    thumbs: [
      "https://images.unsplash.com/photo-1543163521-1bf539c55dd2?auto=format&fit=crop&q=80&w=800"
    ],
    sizes: ["36", "37", "38", "39", "40", "41"],
    colors: ["#5C3A21", "#1E1B18", "#C8B198"],
    colorNames: ["Cognac Brown", "Onyx", "Sand Suede"],
    inStock: true
  },
  {
    id: 5,
    name: "Ivory Satin Stiletto Pumps",
    category: "Shoes",
    price: 155.00,
    discountPrice: 125.00,
    rating: 4.8,
    reviewCount: 64,
    badge: "NEW",
    description: "Elegant pointed-toe heels draped in luminescent silk satin with memory foam cushioned insoles for effortless evening comfort.",
    image: "https://images.unsplash.com/photo-1560343090-f0409e92791a?auto=format&fit=crop&q=80&w=800",
    thumbs: [
      "https://images.unsplash.com/photo-1560343090-f0409e92791a?auto=format&fit=crop&q=80&w=800"
    ],
    sizes: ["36", "37", "38", "39", "40"],
    colors: ["#F9F6F0", "#E8D8CE", "#F0C9B7"],
    colorNames: ["Pearl Ivory", "Champagne", "Soft Blush"],
    inStock: true
  },
  {
    id: 6,
    name: "Chic Minimalist Leather Sneakers",
    category: "Shoes",
    price: 130.00,
    discountPrice: 98.00,
    rating: 4.9,
    reviewCount: 180,
    badge: "SALE",
    description: "Low-top court sneakers crafted from supple calfskin leather with a tonal rubber cupsole. Versatile luxury casual footwear.",
    image: "https://images.unsplash.com/photo-1595950653106-6c9ebd614d3a?auto=format&fit=crop&q=80&w=800",
    thumbs: [
      "https://images.unsplash.com/photo-1595950653106-6c9ebd614d3a?auto=format&fit=crop&q=80&w=800"
    ],
    sizes: ["36", "37", "38", "39", "40", "41"],
    colors: ["#FFFFFF", "#E8D5C8"],
    colorNames: ["Pure White", "Nude Pink Accent"],
    inStock: true
  },
  {
    id: 7,
    name: "Quilted Chain Leather Crossbody Bag",
    category: "Bags",
    price: 220.00,
    discountPrice: 179.00,
    rating: 5.0,
    reviewCount: 310,
    badge: "BEST SELLER",
    description: "Iconic chevron quilted lambskin flap bag with woven gold chain strap and signature clasp hardware. Includes interior zip compartment.",
    image: "https://images.unsplash.com/photo-1584917865442-de89df76afd3?auto=format&fit=crop&q=80&w=800",
    thumbs: [
      "https://images.unsplash.com/photo-1584917865442-de89df76afd3?auto=format&fit=crop&q=80&w=800"
    ],
    sizes: ["One Size"],
    colors: ["#1E1B18", "#D2B48C", "#8B0000"],
    colorNames: ["Noir Gold", "Soft Nude", "Crimson Red"],
    inStock: true
  },
  {
    id: 8,
    name: "Soft Suede Structured Everyday Tote",
    category: "Bags",
    price: 195.00,
    discountPrice: 149.00,
    rating: 4.7,
    reviewCount: 142,
    badge: "SALE",
    description: "Spacious open-top tote crafted from ultra-soft suede with contrast smooth leather straps. Fits a 15-inch laptop with ease.",
    image: "https://images.unsplash.com/photo-1590874103328-eac38a683ce7?auto=format&fit=crop&q=80&w=800",
    thumbs: [
      "https://images.unsplash.com/photo-1590874103328-eac38a683ce7?auto=format&fit=crop&q=80&w=800"
    ],
    sizes: ["One Size"],
    colors: ["#8B5A2B", "#4B5320", "#3B2F2F"],
    colorNames: ["Caramel Suede", "Olive Green", "Mocha"],
    inStock: true
  },
  {
    id: 9,
    name: "Botanical Rose Facial Hydrating Elixir",
    category: "Beauty",
    price: 78.00,
    discountPrice: 59.00,
    rating: 4.9,
    reviewCount: 420,
    badge: "BEST SELLER",
    description: "Nourishing facial oil infused with Damascus rose extracts, jojoba, and cold-pressed squalane. Restores luminous skin barrier overnight.",
    image: "https://images.unsplash.com/photo-1608248597261-833258657640?auto=format&fit=crop&q=80&w=800",
    thumbs: [
      "https://images.unsplash.com/photo-1608248597261-833258657640?auto=format&fit=crop&q=80&w=800"
    ],
    sizes: ["50ml", "100ml"],
    colors: ["#F4C2C2"],
    colorNames: ["Rose Glow"],
    inStock: true
  },
  {
    id: 10,
    name: "Glowing Radiance Vitamin C Serum",
    category: "Beauty",
    price: 65.00,
    discountPrice: 49.00,
    rating: 4.8,
    reviewCount: 195,
    badge: "NEW",
    description: "Potent 15% THD Vitamin C formula enhanced with hyaluronic acid and ferulic acid to brighten dark spots and protect against environmental pollutants.",
    image: "https://images.unsplash.com/photo-1620916566398-39f1143ab7be?auto=format&fit=crop&q=80&w=800",
    thumbs: [
      "https://images.unsplash.com/photo-1620916566398-39f1143ab7be?auto=format&fit=crop&q=80&w=800"
    ],
    sizes: ["30ml"],
    colors: ["#FFBF00"],
    colorNames: ["Golden Amber"],
    inStock: true
  },
  {
    id: 11,
    name: "18K Gold Plated Layered Pendant Necklace",
    category: "Accessories",
    price: 98.00,
    discountPrice: 75.00,
    rating: 4.9,
    reviewCount: 280,
    badge: "BEST SELLER",
    description: "Dual-layer delicate chain set crafted in nickel-free brass electroplated with 18-karat real gold and featuring a coin medallion charm.",
    image: "https://images.unsplash.com/photo-1599643478518-a784e5dc4c8f?auto=format&fit=crop&q=80&w=800",
    thumbs: [
      "https://images.unsplash.com/photo-1599643478518-a784e5dc4c8f?auto=format&fit=crop&q=80&w=800"
    ],
    sizes: ["Adjustable"],
    colors: ["#D4AF37", "#B76E79", "#C0C0C0"],
    colorNames: ["Warm 18K Gold", "Rose Gold", "Sterling Silver"],
    inStock: true
  },
  {
    id: 12,
    name: "Oversized Gradient UV Sunglasses",
    category: "Accessories",
    price: 115.00,
    discountPrice: 85.00,
    rating: 4.7,
    reviewCount: 110,
    badge: "NEW",
    description: "Italian acetate frames with scratch-resistant brown gradient lenses offering 100% UV400 protection. Statement eyewear for sunny days.",
    image: "https://images.unsplash.com/photo-1511499767150-a48a237f0083?auto=format&fit=crop&q=80&w=800",
    thumbs: [
      "https://images.unsplash.com/photo-1511499767150-a48a237f0083?auto=format&fit=crop&q=80&w=800"
    ],
    sizes: ["One Size"],
    colors: ["#382513", "#EADCC9", "#111111"],
    colorNames: ["Tortoise Shell", "Champagne Nude", "Smokey Black"],
    inStock: true
  },
  {
    id: 13,
    name: "Vintage Italian Leather Chronograph Watch",
    category: "Accessories",
    price: 189.00,
    discountPrice: 145.00,
    rating: 4.9,
    reviewCount: 165,
    badge: "BEST SELLER",
    description: "Classic timepiece featuring a rose-gold stainless steel case, genuine stitched leather band, sapphire crystal glass, and Japanese quartz movement.",
    image: "https://images.unsplash.com/photo-1524805444758-089113d48a6d?auto=format&fit=crop&q=80&w=800",
    thumbs: [
      "https://images.unsplash.com/photo-1524805444758-089113d48a6d?auto=format&fit=crop&q=80&w=800"
    ],
    sizes: ["38mm", "42mm"],
    colors: ["#5C4033", "#1E1B18"],
    colorNames: ["Chestnut Gold", "Espresso Black"],
    inStock: true
  },
  {
    id: 14,
    name: "Silk Satin Square Printed Scarf",
    category: "Accessories",
    price: 75.00,
    discountPrice: 58.00,
    rating: 4.8,
    reviewCount: 89,
    badge: "SALE",
    description: "Luxurious 100% pure silk square scarf with hand-rolled edges and an intricate botanical print. Can be styled around neck, hair, or handbag strap.",
    image: "https://images.unsplash.com/photo-1601924994987-69e26d50dc26?auto=format&fit=crop&q=80&w=800",
    thumbs: [
      "https://images.unsplash.com/photo-1601924994987-69e26d50dc26?auto=format&fit=crop&q=80&w=800"
    ],
    sizes: ["90x90cm"],
    colors: ["#0F382C", "#D4AF37", "#C88A83"],
    colorNames: ["Emerald Floral", "Golden Chain", "Paisley Pink"],
    inStock: true
  }
];

// ==========================================
// 2. STATE MANAGEMENT & LOCAL STORAGE
// ==========================================
let cart = [];
let wishlist = [];
let appliedCoupon = null;
let currentSelectedModalProduct = null;
let currentSelectedSize = "";
let currentSelectedColor = "";
let currentSelectedQty = 1;

// Load persisted state on startup
function loadStateFromLocalStorage() {
  const savedCart = localStorage.getItem("auraluxe_cart");
  const savedWishlist = localStorage.getItem("auraluxe_wishlist");

  if (savedCart) {
    try { cart = JSON.parse(savedCart); } catch(e) { cart = []; }
  } else {
    // Default initial sample cart item
    cart = [{ productId: 1, color: "Camel", size: "M", quantity: 1 }];
  }

  if (savedWishlist) {
    try { wishlist = JSON.parse(savedWishlist); } catch(e) { wishlist = []; }
  } else {
    wishlist = [4, 7];
  }

  updateHeaderBadges();
}

function saveStateToLocalStorage() {
  localStorage.setItem("auraluxe_cart", JSON.stringify(cart));
  localStorage.setItem("auraluxe_wishlist", JSON.stringify(wishlist));
  updateHeaderBadges();
}

function updateHeaderBadges() {
  const cartCountEl = document.getElementById("cart-count");
  const wishlistCountEl = document.getElementById("wishlist-count");
  const drawerCountEl = document.getElementById("drawer-cart-count");

  const totalCartQty = cart.reduce((sum, item) => sum + item.quantity, 0);

  if (cartCountEl) cartCountEl.textContent = totalCartQty;
  if (drawerCountEl) drawerCountEl.textContent = totalCartQty;
  if (wishlistCountEl) wishlistCountEl.textContent = wishlist.length;
}

// ==========================================
// 3. SPA VIEW NAVIGATION
// ==========================================
function switchPage(pageId) {
  // Close mobile navigation menu if open
  const navMenu = document.getElementById("nav-menu");
  if (navMenu) {
    navMenu.classList.remove("active");
  }

  const pages = document.querySelectorAll(".page-view");
  pages.forEach(page => page.classList.remove("active"));

  const targetPage = document.getElementById(`page-${pageId}`);
  if (targetPage) {
    targetPage.classList.add("active");
  }

  // Update navbar links active state
  const navLinks = document.querySelectorAll(".nav-link");
  navLinks.forEach(link => {
    if (link.getAttribute("data-page") === pageId) {
      link.classList.add("active");
    } else {
      link.classList.remove("active");
    }
  });

  // Trigger page specific renders
  if (pageId === "home") {
    renderHomeProducts("all");
  } else if (pageId === "shop") {
    applyShopFilters();
  } else if (pageId === "wishlist") {
    renderWishlist();
  } else if (pageId === "cart") {
    renderCartPage();
  } else if (pageId === "checkout") {
    renderCheckoutSummary();
  }

  window.scrollTo({ top: 0, behavior: "smooth" });
}

function scrollToSection(sectionId) {
  const elem = document.getElementById(sectionId);
  if (elem) {
    elem.scrollIntoView({ behavior: "smooth" });
  }
}

function scrollToFooter() {
  window.scrollTo({ top: document.body.scrollHeight, behavior: "smooth" });
}

// ==========================================
// 4. PRODUCT RENDERING UTILITIES
// ==========================================
function createProductCardHTML(product) {
  const isWishlisted = wishlist.includes(product.id);
  const badgeClass = product.badge === "NEW" ? "badge-new" : product.badge === "SALE" ? "badge-sale" : "badge-bestseller";

  return `
    <div class="product-card" data-testid="product-card-${product.id}">
      <div class="product-img-wrap">
        <span class="badge ${badgeClass}">${product.badge}</span>
        <button class="wishlist-btn ${isWishlisted ? 'active' : ''}" data-testid="wishlist-btn-${product.id}" onclick="toggleWishlist(${product.id}, event)" title="Add to Wishlist">
          <i class="${isWishlisted ? 'fa-solid' : 'fa-regular'} fa-heart"></i>
        </button>
        <img src="${product.image}" alt="${product.name}" class="product-img" data-testid="product-img-${product.id}" onclick="openProductModal(${product.id})">
        
        <div class="product-actions-overlay">
          <button class="btn-quick-add" data-testid="quick-add-btn-${product.id}" onclick="quickAddToCart(${product.id}, event)">
            <i class="fa-solid fa-bag-shopping"></i> Quick Add
          </button>
        </div>
      </div>

      <div class="product-details">
        <div class="product-cat">${product.category}</div>
        <h3 class="product-name"><a href="#" data-testid="product-name-${product.id}" onclick="openProductModal(${product.id}); return false;">${product.name}</a></h3>
        
        <div class="product-rating">
          <i class="fa-solid fa-star"></i>
          <span>${product.rating} (${product.reviewCount})</span>
        </div>

        <div class="product-price-wrap">
          <span class="price-current" data-testid="product-price-${product.id}">$${product.discountPrice.toFixed(2)}</span>
          ${product.price > product.discountPrice ? `<span class="price-old">$${product.price.toFixed(2)}</span>` : ''}
        </div>
      </div>
    </div>
  `;
}

function renderHomeProducts(filterType = "all", clickedBtn = null) {
  const container = document.getElementById("home-products-grid");
  if (!container) return;

  if (clickedBtn) {
    const tabs = document.querySelectorAll(".products-filter-tabs .tab-btn");
    tabs.forEach(t => t.classList.remove("active"));
    clickedBtn.classList.add("active");
  }

  let filtered = [...PRODUCTS_DATA];
  if (filterType !== "all") {
    filtered = PRODUCTS_DATA.filter(p => p.badge === filterType);
  }

  const itemsToRender = filtered.slice(0, 8);
  container.innerHTML = itemsToRender.map(p => createProductCardHTML(p)).join("");
}

// Filter and Sort for Shop Page
function applyShopFilters() {
  const shopGrid = document.getElementById("shop-products-grid");
  const countEl = document.getElementById("shop-results-count");
  if (!shopGrid) return;

  const searchQuery = (document.getElementById("shop-search-input")?.value || "").toLowerCase().trim();
  const selectedCatRadio = document.querySelector('input[name="shop-category"]:checked')?.value || "All";
  const maxPrice = parseFloat(document.getElementById("price-slider")?.value || 300);

  const filterSale = document.getElementById("badge-filter-sale")?.checked;
  const filterNew = document.getElementById("badge-filter-new")?.checked;
  const filterBest = document.getElementById("badge-filter-bestseller")?.checked;

  const sortVal = document.getElementById("shop-sort-select")?.value || "popular";

  let filtered = PRODUCTS_DATA.filter(product => {
    const matchesSearch = product.name.toLowerCase().includes(searchQuery) || product.category.toLowerCase().includes(searchQuery);
    const matchesCat = selectedCatRadio === "All" || product.category === selectedCatRadio;
    const matchesPrice = product.discountPrice <= maxPrice;

    let matchesBadge = true;
    if (filterSale && product.badge !== "SALE") matchesBadge = false;
    if (filterNew && product.badge !== "NEW") matchesBadge = false;
    if (filterBest && product.badge !== "BEST SELLER") matchesBadge = false;

    return matchesSearch && matchesCat && matchesPrice && matchesBadge;
  });

  if (sortVal === "low-high") {
    filtered.sort((a, b) => a.discountPrice - b.discountPrice);
  } else if (sortVal === "high-low") {
    filtered.sort((a, b) => b.discountPrice - a.discountPrice);
  } else if (sortVal === "rating") {
    filtered.sort((a, b) => b.rating - a.rating);
  } else if (sortVal === "newest") {
    filtered.sort((a, b) => (b.badge === "NEW" ? 1 : -1));
  }

  if (countEl) {
    countEl.textContent = `Showing ${filtered.length} of ${PRODUCTS_DATA.length} items`;
  }

  if (filtered.length === 0) {
    shopGrid.innerHTML = `
      <div class="empty-state" style="grid-column: 1 / -1;">
        <i class="fa-solid fa-filter-circle-xmark"></i>
        <h3>No products match your filters</h3>
        <p>Try adjusting your search criteria or price range slider.</p>
        <button class="btn btn-primary" onclick="resetShopFilters()">Reset Filters</button>
      </div>
    `;
  } else {
    shopGrid.innerHTML = filtered.map(p => createProductCardHTML(p)).join("");
  }
}

function updatePriceSlider(val) {
  const displayVal = document.getElementById("price-slider-value");
  if (displayVal) displayVal.textContent = `Max: $${val}`;
  applyShopFilters();
}

function filterByCategory(categoryName) {
  switchPage("shop");
  const catRadio = document.querySelector(`input[name="shop-category"][value="${categoryName}"]`);
  if (catRadio) {
    catRadio.checked = true;
  }
  applyShopFilters();
}

function resetShopFilters() {
  const searchInput = document.getElementById("shop-search-input");
  if (searchInput) searchInput.value = "";

  const allCatRadio = document.querySelector('input[name="shop-category"][value="All"]');
  if (allCatRadio) allCatRadio.checked = true;

  const slider = document.getElementById("price-slider");
  if (slider) {
    slider.value = 300;
    updatePriceSlider(300);
  }

  const badgeSale = document.getElementById("badge-filter-sale");
  const badgeNew = document.getElementById("badge-filter-new");
  const badgeBest = document.getElementById("badge-filter-bestseller");

  if (badgeSale) badgeSale.checked = false;
  if (badgeNew) badgeNew.checked = false;
  if (badgeBest) badgeBest.checked = false;

  applyShopFilters();
  showToast("Filters reset to default", "info");
}

function toggleMobileFilter() {
  const sidebar = document.getElementById("shop-sidebar");
  if (sidebar) sidebar.classList.toggle("active-mobile");
}

// ==========================================
// 5. WISHLIST MANAGEMENT
// ==========================================
function toggleWishlist(productId, event = null) {
  if (event) event.stopPropagation();

  const index = wishlist.indexOf(productId);
  const product = PRODUCTS_DATA.find(p => p.id === productId);

  if (index > -1) {
    wishlist.splice(index, 1);
    showToast(`Removed "${product?.name}" from wishlist`, "info");
  } else {
    wishlist.push(productId);
    showToast(`Saved "${product?.name}" to wishlist`, "success");
  }

  saveStateToLocalStorage();
  
  const activePage = document.querySelector(".page-view.active");
  if (activePage && activePage.id === "page-wishlist") {
    renderWishlist();
  } else if (activePage && activePage.id === "page-shop") {
    applyShopFilters();
  } else if (activePage && activePage.id === "page-home") {
    renderHomeProducts("all");
  }
}

function renderWishlist() {
  const grid = document.getElementById("wishlist-products-grid");
  const emptyState = document.getElementById("wishlist-empty-state");
  if (!grid || !emptyState) return;

  if (wishlist.length === 0) {
    emptyState.style.display = "block";
    grid.innerHTML = "";
    return;
  }

  emptyState.style.display = "none";
  const savedProducts = PRODUCTS_DATA.filter(p => wishlist.includes(p.id));
  grid.innerHTML = savedProducts.map(p => createProductCardHTML(p)).join("");
}

// ==========================================
// 6. CART MANAGEMENT
// ==========================================
function quickAddToCart(productId, event = null) {
  if (event) event.stopPropagation();

  const product = PRODUCTS_DATA.find(p => p.id === productId);
  if (!product) return;

  const defaultColor = product.colorNames[0] || "Default";
  const defaultSize = product.sizes[0] || "One Size";

  addToCart(productId, defaultColor, defaultSize, 1);
}

function addToCart(productId, color, size, quantity = 1) {
  const product = PRODUCTS_DATA.find(p => p.id === productId);
  if (!product) return;

  const existingItemIndex = cart.findIndex(item => 
    item.productId === productId && item.color === color && item.size === size
  );

  if (existingItemIndex > -1) {
    cart[existingItemIndex].quantity += quantity;
  } else {
    cart.push({ productId, color, size, quantity });
  }

  saveStateToLocalStorage();
  renderCartDrawer();
  showToast(`Added ${quantity}x "${product.name}" to cart!`, "success");
}

function updateCartItemQty(index, newQty) {
  if (newQty <= 0) {
    removeCartItem(index);
    return;
  }
  cart[index].quantity = newQty;
  saveStateToLocalStorage();
  renderCartDrawer();
  renderCartPage();
  renderCheckoutSummary();
}

function removeCartItem(index) {
  const item = cart[index];
  const product = PRODUCTS_DATA.find(p => p.id === item?.productId);
  cart.splice(index, 1);
  saveStateToLocalStorage();
  renderCartDrawer();
  renderCartPage();
  renderCheckoutSummary();
  showToast(`Removed "${product?.name || 'Item'}" from cart`, "info");
}

function toggleCartDrawer() {
  const drawer = document.getElementById("cart-drawer");
  if (drawer) {
    drawer.classList.toggle("active");
    if (drawer.classList.contains("active")) {
      renderCartDrawer();
    }
  }
}

function renderCartDrawer() {
  const drawerBody = document.getElementById("drawer-cart-body");
  const drawerSubtotal = document.getElementById("drawer-cart-subtotal");
  if (!drawerBody) return;

  if (cart.length === 0) {
    drawerBody.innerHTML = `
      <div class="empty-state">
        <i class="fa-solid fa-bag-shopping"></i>
        <h4 style="margin-bottom: 0.4rem;">Your cart is empty</h4>
        <p style="font-size: 0.85rem;">Discover our latest collection and add items to your bag.</p>
      </div>
    `;
    if (drawerSubtotal) drawerSubtotal.textContent = "$0.00";
    return;
  }

  let subtotal = 0;
  drawerBody.innerHTML = cart.map((item, index) => {
    const product = PRODUCTS_DATA.find(p => p.id === item.productId);
    if (!product) return "";

    const itemTotal = product.discountPrice * item.quantity;
    subtotal += itemTotal;

    return `
      <div class="cart-item" data-testid="cart-item-${item.productId}">
        <img src="${product.image}" alt="${product.name}" class="cart-item-img">
        <div class="cart-item-info">
          <h4 class="cart-item-title">${product.name}</h4>
          <div class="cart-item-meta">Size: ${item.size} | Color: ${item.color}</div>
          <div style="display: flex; justify-content: space-between; align-items: center; margin-top: 0.4rem;">
            <div class="qty-picker" style="height: 32px;">
              <button class="qty-btn" data-testid="qty-minus-${index}" onclick="updateCartItemQty(${index}, ${item.quantity - 1})" style="width: 28px;">-</button>
              <input type="text" class="qty-input" data-testid="qty-val-${index}" value="${item.quantity}" readonly style="width: 32px; font-size: 0.88rem;">
              <button class="qty-btn" data-testid="qty-plus-${index}" onclick="updateCartItemQty(${index}, ${item.quantity + 1})" style="width: 28px;">+</button>
            </div>
            <span style="font-weight: 700;">$${itemTotal.toFixed(2)}</span>
            <button data-testid="remove-item-${index}" onclick="removeCartItem(${index})" style="color: var(--text-muted); font-size: 0.9rem;" title="Remove"><i class="fa-solid fa-trash-can"></i></button>
          </div>
        </div>
      </div>
    `;
  }).join("");

  if (drawerSubtotal) drawerSubtotal.textContent = `$${subtotal.toFixed(2)}`;
}

function renderCartPage() {
  const itemsListEl = document.getElementById("cart-page-items-list");
  const itemsCountEl = document.getElementById("cart-page-items-count");
  const emptyStateEl = document.getElementById("cart-page-empty");
  const contentEl = document.getElementById("cart-page-content");

  if (!itemsListEl || !contentEl) return;

  if (cart.length === 0) {
    emptyStateEl.style.display = "block";
    contentEl.style.display = "none";
    return;
  }

  emptyStateEl.style.display = "none";
  contentEl.style.display = "grid";

  const totalQty = cart.reduce((sum, item) => sum + item.quantity, 0);
  if (itemsCountEl) itemsCountEl.textContent = totalQty;

  let subtotal = 0;
  itemsListEl.innerHTML = cart.map((item, index) => {
    const product = PRODUCTS_DATA.find(p => p.id === item.productId);
    if (!product) return "";

    const itemTotal = product.discountPrice * item.quantity;
    subtotal += itemTotal;

    return `
      <div class="cart-item" data-testid="cart-item-${item.productId}" style="padding-bottom: 1.5rem; margin-bottom: 1.5rem;">
        <img src="${product.image}" alt="${product.name}" class="cart-item-img" style="width: 90px; height: 110px;">
        <div class="cart-item-info">
          <h4 class="cart-item-title" style="font-size: 1.05rem;">${product.name}</h4>
          <div class="cart-item-meta" style="font-size: 0.85rem;">Category: ${product.category} | Size: ${item.size} | Color: ${item.color}</div>
          <div style="font-size: 0.9rem; color: var(--accent-rose); font-weight: 600; margin-bottom: 0.6rem;">Unit Price: $${product.discountPrice.toFixed(2)}</div>
          
          <div style="display: flex; justify-content: space-between; align-items: center;">
            <div class="qty-picker">
              <button class="qty-btn" data-testid="qty-minus-${index}" onclick="updateCartItemQty(${index}, ${item.quantity - 1})">-</button>
              <input type="text" class="qty-input" data-testid="qty-val-${index}" value="${item.quantity}" readonly>
              <button class="qty-btn" data-testid="qty-plus-${index}" onclick="updateCartItemQty(${index}, ${item.quantity + 1})">+</button>
            </div>
            
            <div style="text-align: right;">
              <div style="font-size: 1.15rem; font-weight: 700; color: var(--text-main);">$${itemTotal.toFixed(2)}</div>
              <button data-testid="remove-item-${index}" onclick="removeCartItem(${index})" style="color: var(--error); font-size: 0.85rem; margin-top: 0.2rem;" title="Remove Item"><i class="fa-solid fa-trash-can"></i> Remove</button>
            </div>
          </div>
        </div>
      </div>
    `;
  }).join("");

  calculateTotals(subtotal);
}

function calculateTotals(subtotal) {
  const subtotalEl = document.getElementById("cart-subtotal-val");
  const discountRow = document.getElementById("coupon-discount-row");
  const discountEl = document.getElementById("cart-discount-val");
  const deliveryEl = document.getElementById("cart-delivery-val");
  const totalEl = document.getElementById("cart-total-val");

  const shippingMsg = document.getElementById("cart-page-shipping-msg");
  const shippingFill = document.getElementById("cart-page-shipping-fill");

  const freeShippingThreshold = 100;
  let deliveryFee = subtotal >= freeShippingThreshold ? 0 : 15.00;

  if (shippingMsg && shippingFill) {
    if (subtotal >= freeShippingThreshold) {
      shippingMsg.textContent = "🎉 Congratulations! You unlocked FREE Worldwide Shipping!";
      shippingFill.style.width = "100%";
    } else {
      const remaining = freeShippingThreshold - subtotal;
      shippingMsg.textContent = `Add $${remaining.toFixed(2)} more to unlock FREE Delivery`;
      shippingFill.style.width = `${Math.min((subtotal / freeShippingThreshold) * 100, 100)}%`;
    }
  }

  let discountAmount = 0;
  if (appliedCoupon) {
    discountAmount = (subtotal * appliedCoupon.discountPercent) / 100;
    if (discountRow) discountRow.style.display = "flex";
    if (discountEl) discountEl.textContent = `-$${discountAmount.toFixed(2)}`;
  } else {
    if (discountRow) discountRow.style.display = "none";
  }

  const grandTotal = subtotal - discountAmount + deliveryFee;

  if (subtotalEl) subtotalEl.textContent = `$${subtotal.toFixed(2)}`;
  if (deliveryEl) deliveryEl.textContent = deliveryFee === 0 ? "FREE" : `$${deliveryFee.toFixed(2)}`;
  if (totalEl) totalEl.textContent = `$${grandTotal.toFixed(2)}`;
}

async function applyCouponCode() {
  const input = document.getElementById("coupon-code-input");
  const code = (input?.value || "").toUpperCase().trim();

  if (!code) {
    showToast("Please enter a promo code", "error");
    return;
  }

  // Attempt API verification first if running with backend
  try {
    const res = await fetch("/api/coupons/verify", {
      method: "POST",
      headers: { "Content-Type": "application/json" },
      body: JSON.stringify({ code })
    });
    const data = await res.json();
    if (res.ok && data.valid) {
      appliedCoupon = { code: data.code, discountPercent: data.discountPercent };
      showToast(`Promo Code ${data.code} Applied (${data.discountPercent}% OFF)!`, "success");
      renderCartPage();
      return;
    } else {
      showToast(data.error || "Invalid Promo Code. Try 'AURA10'", "error");
      return;
    }
  } catch (err) {
    // Client-side fallback if server not reachable
    if (code === "AURA10") {
      appliedCoupon = { code: "AURA10", discountPercent: 10 };
      showToast("Promo Code AURA10 Applied (10% OFF)!", "success");
      renderCartPage();
    } else if (code === "FREESHIP") {
      appliedCoupon = { code: "FREESHIP", discountPercent: 5 };
      showToast("Promo Code FREESHIP Applied!", "success");
      renderCartPage();
    } else {
      showToast("Invalid Promo Code. Try 'AURA10'", "error");
    }
  }
}

// ==========================================
// 7. PRODUCT DETAILS MODAL & QUICK VIEW
// ==========================================
function openProductModal(productId) {
  const product = PRODUCTS_DATA.find(p => p.id === productId);
  if (!product) return;

  currentSelectedModalProduct = product;
  currentSelectedSize = product.sizes[0] || "One Size";
  currentSelectedColor = product.colorNames[0] || "Default";
  currentSelectedQty = 1;

  const modal = document.getElementById("product-modal");
  const modalContent = document.getElementById("modal-product-content");
  if (!modal || !modalContent) return;

  modalContent.innerHTML = `
    <!-- Image Gallery -->
    <div class="product-gallery">
      <div class="main-image-wrap">
        <img id="modal-main-img" data-testid="modal-main-img" src="${product.image}" alt="${product.name}">
      </div>
      <div class="thumbs-row">
        ${product.thumbs.map((t, idx) => `
          <div class="thumb-item ${idx === 0 ? 'active' : ''}" onclick="switchModalThumb('${t}', this)">
            <img src="${t}" alt="Thumbnail">
          </div>
        `).join("")}
      </div>
    </div>

    <!-- Product Details Info -->
    <div class="product-info-panel">
      <span class="product-cat">${product.category}</span>
      <h2 data-testid="modal-product-title">${product.name}</h2>
      
      <div class="product-meta-row">
        <div class="product-rating">
          <i class="fa-solid fa-star"></i>
          <span>${product.rating} (${product.reviewCount} reviews)</span>
        </div>
        <span style="color: var(--success); font-size: 0.85rem; font-weight: 600;"><i class="fa-solid fa-circle-check"></i> In Stock</span>
      </div>

      <div class="product-price-wrap" style="margin-bottom: 1.5rem;">
        <span class="price-current" data-testid="modal-product-price" style="font-size: 1.8rem; color: var(--accent-rose);">$${product.discountPrice.toFixed(2)}</span>
        ${product.price > product.discountPrice ? `<span class="price-old" style="font-size: 1.2rem;">$${product.price.toFixed(2)}</span>` : ''}
      </div>

      <p style="font-size: 0.95rem; color: var(--text-body); margin-bottom: 1.5rem; line-height: 1.6;">
        ${product.description}
      </p>

      <!-- Color Selector -->
      <div class="swatch-group">
        <label class="swatch-label">Color: <span id="modal-color-name">${currentSelectedColor}</span></label>
        <div class="swatches">
          ${product.colors.map((c, i) => `
            <div class="color-swatch ${i === 0 ? 'active' : ''}" 
                 style="background-color: ${c};" 
                 title="${product.colorNames[i]}"
                 onclick="selectModalColor('${product.colorNames[i]}', this)"></div>
          `).join("")}
        </div>
      </div>

      <!-- Size Selector -->
      <div class="swatch-group">
        <label class="swatch-label">Size: <span id="modal-size-name">${currentSelectedSize}</span></label>
        <div class="swatches">
          ${product.sizes.map((s, i) => `
            <div class="size-swatch ${i === 0 ? 'active' : ''}" 
                 onclick="selectModalSize('${s}', this)">${s}</div>
          `).join("")}
        </div>
      </div>

      <!-- Quantity Stepper -->
      <div class="swatch-group">
        <label class="swatch-label">Quantity</label>
        <div class="qty-picker">
          <button class="qty-btn" data-testid="modal-qty-minus" onclick="updateModalQty(-1)">-</button>
          <input type="text" id="modal-qty-input" data-testid="modal-qty-input" class="qty-input" value="1" readonly>
          <button class="qty-btn" data-testid="modal-qty-plus" onclick="updateModalQty(1)">+</button>
        </div>
      </div>

      <!-- CTA Buttons -->
      <div style="display: flex; gap: 1rem; margin-top: 2rem;">
        <button class="btn btn-primary" id="modal-add-to-bag-btn" data-testid="modal-add-to-bag-btn" style="flex-grow: 1;" onclick="addModalItemToCart(false)">
          <i class="fa-solid fa-bag-shopping"></i> Add to Bag
        </button>
        <button class="btn btn-secondary" id="modal-buy-now-btn" data-testid="modal-buy-now-btn" style="flex-grow: 1;" onclick="addModalItemToCart(true)">
          Buy Now
        </button>
      </div>
    </div>
  `;

  modal.classList.add("active");
}

function switchModalThumb(imgSrc, thumbElem) {
  const mainImg = document.getElementById("modal-main-img");
  if (mainImg) mainImg.src = imgSrc;

  const thumbs = document.querySelectorAll(".thumb-item");
  thumbs.forEach(t => t.classList.remove("active"));
  thumbElem.classList.add("active");
}

function selectModalColor(colorName, swatchElem) {
  currentSelectedColor = colorName;
  const label = document.getElementById("modal-color-name");
  if (label) label.textContent = colorName;

  const swatches = document.querySelectorAll(".color-swatch");
  swatches.forEach(s => s.classList.remove("active"));
  swatchElem.classList.add("active");
}

function selectModalSize(sizeName, swatchElem) {
  currentSelectedSize = sizeName;
  const label = document.getElementById("modal-size-name");
  if (label) label.textContent = sizeName;

  const swatches = document.querySelectorAll(".size-swatch");
  swatches.forEach(s => s.classList.remove("active"));
  swatchElem.classList.add("active");
}

function updateModalQty(change) {
  currentSelectedQty = Math.max(1, currentSelectedQty + change);
  const input = document.getElementById("modal-qty-input");
  if (input) input.value = currentSelectedQty;
}

function addModalItemToCart(isBuyNow = false) {
  if (!currentSelectedModalProduct) return;

  addToCart(
    currentSelectedModalProduct.id,
    currentSelectedColor,
    currentSelectedSize,
    currentSelectedQty
  );

  closeProductModal();

  if (isBuyNow) {
    switchPage("checkout");
  }
}

function closeProductModal() {
  const modal = document.getElementById("product-modal");
  if (modal) modal.classList.remove("active");
}

// ==========================================
// 8. CHECKOUT PAGE & ORDER PLACEMENT
// ==========================================
function renderCheckoutSummary() {
  const itemsListEl = document.getElementById("checkout-items-list");
  const subtotalEl = document.getElementById("chk-subtotal-val");
  const discountRow = document.getElementById("chk-discount-row");
  const discountEl = document.getElementById("chk-discount-val");
  const shippingEl = document.getElementById("chk-shipping-val");
  const totalEl = document.getElementById("chk-total-val");

  if (!itemsListEl) return;

  if (cart.length === 0) {
    itemsListEl.innerHTML = `<p style="font-size: 0.88rem; color: var(--text-muted);">Your shopping bag is empty.</p>`;
    if (subtotalEl) subtotalEl.textContent = "$0.00";
    if (totalEl) totalEl.textContent = "$0.00";
    return;
  }

  let subtotal = 0;
  itemsListEl.innerHTML = cart.map(item => {
    const product = PRODUCTS_DATA.find(p => p.id === item.productId);
    if (!product) return "";

    const itemTotal = product.discountPrice * item.quantity;
    subtotal += itemTotal;

    return `
      <div style="display: flex; justify-content: space-between; align-items: center; margin-bottom: 0.8rem; font-size: 0.9rem;">
        <div>
          <strong>${product.name}</strong> x ${item.quantity}
          <div style="font-size: 0.78rem; color: var(--text-muted);">${item.size} / ${item.color}</div>
        </div>
        <strong>$${itemTotal.toFixed(2)}</strong>
      </div>
    `;
  }).join("");

  const deliveryFee = subtotal >= 100 ? 0 : 15.00;
  let discountAmount = 0;

  if (appliedCoupon) {
    discountAmount = (subtotal * appliedCoupon.discountPercent) / 100;
    if (discountRow) discountRow.style.display = "flex";
    if (discountEl) discountEl.textContent = `-$${discountAmount.toFixed(2)}`;
  } else {
    if (discountRow) discountRow.style.display = "none";
  }

  const grandTotal = subtotal - discountAmount + deliveryFee;

  if (subtotalEl) subtotalEl.textContent = `$${subtotal.toFixed(2)}`;
  if (shippingEl) shippingEl.textContent = deliveryFee === 0 ? "FREE" : `$${deliveryFee.toFixed(2)}`;
  if (totalEl) totalEl.textContent = `$${grandTotal.toFixed(2)}`;
}

function selectPaymentMethod(methodType) {
  const options = document.querySelectorAll(".payment-option-card");
  options.forEach(opt => opt.classList.remove("selected"));

  const cardBox = document.getElementById("card-fields-box");

  if (methodType === "card") {
    document.getElementById("opt-card")?.classList.add("selected");
    if (cardBox) cardBox.style.display = "block";
  } else if (methodType === "paypal") {
    document.getElementById("opt-paypal")?.classList.add("selected");
    if (cardBox) cardBox.style.display = "none";
  } else {
    document.getElementById("opt-cod")?.classList.add("selected");
    if (cardBox) cardBox.style.display = "none";
  }
}

function updateCardPreview() {
  const numInput = document.getElementById("chk-card-num");
  const nameInput = document.getElementById("chk-card-name");
  const expInput = document.getElementById("chk-card-exp");

  const numDisplay = document.getElementById("card-num-display");
  const nameDisplay = document.getElementById("card-name-display");
  const expDisplay = document.getElementById("card-exp-display");

  if (numInput && numDisplay) {
    let val = numInput.value.replace(/\D/g, '').substring(0, 16);
    let formatted = val.replace(/(.{4})/g, '$1 ').trim();
    numInput.value = formatted;
    numDisplay.textContent = formatted || "•••• •••• •••• 4242";
  }

  if (nameInput && nameDisplay) {
    nameDisplay.textContent = (nameInput.value.trim() || "JANE DOE").toUpperCase();
  }

  if (expInput && expDisplay) {
    let val = expInput.value.replace(/\D/g, '').substring(0, 4);
    if (val.length >= 3) {
      val = val.substring(0, 2) + '/' + val.substring(2);
    }
    expInput.value = val;
    expDisplay.textContent = val || "12/28";
  }
}

async function handlePlaceOrder(event) {
  event.preventDefault();

  if (cart.length === 0) {
    showToast("Your cart is empty! Please add items before checking out.", "error");
    return;
  }

  const btn = document.getElementById("place-order-btn");
  if (btn) {
    btn.disabled = true;
    btn.innerHTML = `<i class="fa-solid fa-spinner fa-spin"></i> Processing Order...`;
  }

  const selectedMethod = document.querySelector('input[name="payment-method"]:checked')?.value || "card";
  const methodLabel = selectedMethod === "card" ? "Credit / Debit Card" : selectedMethod === "paypal" ? "PayPal Express" : "Cash on Delivery (COD)";

  const orderPayload = {
    firstName: document.getElementById("chk-first-name")?.value || "",
    lastName: document.getElementById("chk-last-name")?.value || "",
    email: document.getElementById("chk-email")?.value || "",
    phone: document.getElementById("chk-phone")?.value || "",
    address: document.getElementById("chk-address")?.value || "",
    city: document.getElementById("chk-city")?.value || "",
    state: document.getElementById("chk-state")?.value || "",
    zip: document.getElementById("chk-zip")?.value || "",
    country: document.getElementById("chk-country")?.value || "United States",
    paymentMethod: selectedMethod,
    items: cart,
    coupon: appliedCoupon ? appliedCoupon.code : ""
  };

  try {
    const res = await fetch("/api/orders", {
      method: "POST",
      headers: { "Content-Type": "application/json" },
      body: JSON.stringify(orderPayload)
    });

    if (!res.ok) {
      const errData = await res.json().catch(() => ({}));
      throw new Error(errData.error || `Server responded with status ${res.status}`);
    }

    const data = await res.json();
    const orderId = data.orderId || `AUR-${Math.floor(100000 + Math.random() * 900000)}`;
    const totalPaid = data.order?.summary?.total ? `$${data.order.summary.total.toFixed(2)}` : (document.getElementById("chk-total-val")?.textContent || "$0.00");

    completeOrderSuccess(orderId, methodLabel, totalPaid);

  } catch (err) {
    // Check if network failed or server returned error
    if (!navigator.onLine) {
      showToast("Network Error: You are offline. Cannot process payment.", "error");
    } else if (window.location.protocol === "file:") {
      // Standalone file mode fallback
      const randomNum = Math.floor(100000 + Math.random() * 900000);
      const orderId = `AUR-${randomNum}`;
      const grandTotalText = document.getElementById("chk-total-val")?.textContent || "$0.00";
      completeOrderSuccess(orderId, methodLabel, grandTotalText);
    } else {
      // Real API or intercepted error (e.g. 500 Network Test)
      showToast(`Order failed: ${err.message || 'Server error occurred'}`, "error");
    }
  } finally {
    if (btn) {
      btn.disabled = false;
      btn.innerHTML = `Place Order <i class="fa-solid fa-lock"></i>`;
    }
  }
}

function completeOrderSuccess(orderId, methodLabel, totalPaid) {
  const orderIdEl = document.getElementById("success-order-id");
  const paymentTypeEl = document.getElementById("success-payment-type");
  const totalPaidEl = document.getElementById("success-total-paid");

  if (orderIdEl) orderIdEl.textContent = `#${orderId}`;
  if (paymentTypeEl) paymentTypeEl.textContent = methodLabel;
  if (totalPaidEl) totalPaidEl.textContent = totalPaid;

  if (typeof confetti === "function") {
    confetti({ particleCount: 120, spread: 70, origin: { y: 0.6 } });
  }

  cart = [];
  appliedCoupon = null;
  saveStateToLocalStorage();

  const successModal = document.getElementById("order-success-modal");
  if (successModal) successModal.classList.add("active");
}

function closeOrderSuccessModal() {
  const modal = document.getElementById("order-success-modal");
  if (modal) modal.classList.remove("active");
}

// ==========================================
// 9. TOAST NOTIFICATIONS & UTILITIES
// ==========================================
function showToast(message, type = "success") {
  const container = document.getElementById("toast-container");
  if (!container) return;

  const toast = document.createElement("div");
  toast.className = `toast ${type}`;
  toast.setAttribute("data-testid", `toast-${type}`);

  const iconClass = type === "success" ? "fa-circle-check" : type === "error" ? "fa-circle-exclamation" : "fa-circle-info";

  toast.innerHTML = `
    <i class="fa-solid ${iconClass}"></i>
    <span>${message}</span>
  `;

  container.appendChild(toast);

  setTimeout(() => {
    toast.style.opacity = "0";
    toast.style.transform = "translateX(100%)";
    toast.style.transition = "all 0.3s ease";
    setTimeout(() => toast.remove(), 300);
  }, 3500);
}

// Countdown Timer for Deal Section
function startCountdownTimer() {
  let hours = 5;
  let minutes = 34;
  let seconds = 12;

  setInterval(() => {
    seconds--;
    if (seconds < 0) {
      seconds = 59;
      minutes--;
      if (minutes < 0) {
        minutes = 59;
        hours--;
        if (hours < 0) hours = 23;
      }
    }

    const hEl = document.getElementById("timer-hours");
    const mEl = document.getElementById("timer-mins");
    const sEl = document.getElementById("timer-secs");

    if (hEl) hEl.textContent = String(hours).padStart(2, '0');
    if (mEl) mEl.textContent = String(minutes).padStart(2, '0');
    if (sEl) sEl.textContent = String(seconds).padStart(2, '0');
  }, 1000);
}

// Global Search Overlay Handlers
function setupGlobalSearch() {
  const searchBtn = document.getElementById("search-btn");
  const searchModal = document.getElementById("search-modal");
  const closeBtn = document.getElementById("search-close-btn");
  const searchInput = document.getElementById("global-search-input");
  const resultsPreview = document.getElementById("search-results-preview");

  if (!searchBtn || !searchModal || !searchInput) return;

  searchBtn.addEventListener("click", () => {
    searchModal.classList.add("active");
    searchInput.focus();
  });

  if (closeBtn) {
    closeBtn.addEventListener("click", () => {
      searchModal.classList.remove("active");
    });
  }

  searchInput.addEventListener("input", (e) => {
    const query = e.target.value.toLowerCase().trim();
    if (!query) {
      resultsPreview.innerHTML = "";
      return;
    }

    const matches = PRODUCTS_DATA.filter(p => 
      p.name.toLowerCase().includes(query) || p.category.toLowerCase().includes(query)
    ).slice(0, 4);

    if (matches.length === 0) {
      resultsPreview.innerHTML = `<p style="font-size: 0.9rem; color: var(--text-muted); padding: 0.5rem 0;" data-testid="search-no-results">No matching products found.</p>`;
    } else {
      resultsPreview.innerHTML = matches.map(p => `
        <div class="search-result-item" data-testid="search-result-${p.id}" style="display: flex; align-items: center; gap: 1rem; padding: 0.6rem 0; border-bottom: 1px solid var(--border-light); cursor: pointer;" onclick="openProductModal(${p.id}); document.getElementById('search-modal').classList.remove('active');">
          <img src="${p.image}" alt="${p.name}" style="width: 45px; height: 55px; object-fit: cover; border-radius: 4px;">
          <div>
            <strong style="font-size: 0.95rem;">${p.name}</strong>
            <div style="font-size: 0.8rem; color: var(--accent-rose); font-weight: 600;">$${p.discountPrice.toFixed(2)}</div>
          </div>
        </div>
      `).join("");
    }
  });
}

function setupHeaderScroll() {
  const header = document.getElementById("header");
  window.addEventListener("scroll", () => {
    if (window.scrollY > 50) {
      header?.classList.add("scrolled");
    } else {
      header?.classList.remove("scrolled");
    }
  });
}

function setupMobileMenu() {
  const menuBtn = document.getElementById("mobile-menu-btn");
  const navMenu = document.getElementById("nav-menu");

  if (menuBtn && navMenu) {
    menuBtn.addEventListener("click", () => {
      navMenu.classList.toggle("active");
    });

    const navLinks = navMenu.querySelectorAll(".nav-link");
    navLinks.forEach(link => {
      link.addEventListener("click", () => {
        navMenu.classList.remove("active");
      });
    });
  }
}

function setupTopBar() {
  const closeBtn = document.getElementById("top-bar-close");
  const topBar = document.getElementById("top-bar");
  if (closeBtn && topBar) {
    closeBtn.addEventListener("click", () => {
      topBar.style.display = "none";
    });
  }
}

// Newsletter Subscription Handlers
function setupNewsletters() {
  const form = document.getElementById("home-newsletter-form");
  const statusMsg = document.getElementById("newsletter-status-msg");
  if (!form) return;

  form.addEventListener("submit", async (e) => {
    e.preventDefault();
    const emailInput = document.getElementById("newsletter-email");
    const email = emailInput?.value || "";

    try {
      const res = await fetch("/api/newsletter", {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify({ email })
      });
      const data = await res.json();
      if (res.ok) {
        showToast(data.message || "Subscribed successfully!", "success");
        if (statusMsg) {
          statusMsg.textContent = "✓ Successfully subscribed to VIP updates.";
          statusMsg.style.color = "var(--success)";
        }
      } else {
        showToast(data.error || "Subscription failed", "error");
        if (statusMsg) {
          statusMsg.textContent = data.error;
          statusMsg.style.color = "var(--error)";
        }
      }
    } catch (err) {
      showToast("Thank you for subscribing to Aura Luxe VIP Club!", "success");
      if (statusMsg) {
        statusMsg.textContent = "✓ Successfully subscribed to VIP updates.";
        statusMsg.style.color = "var(--success)";
      }
    }
    form.reset();
  });
}

// Contact Form Submission Handler
async function handleContactSubmit(event) {
  event.preventDefault();

  const name = document.getElementById("contact-name")?.value || "";
  const email = document.getElementById("contact-email")?.value || "";
  const subject = document.getElementById("contact-subject")?.value || "";
  const message = document.getElementById("contact-message")?.value || "";
  const statusEl = document.getElementById("contact-status-msg");
  const btn = document.getElementById("contact-submit-btn");

  if (btn) btn.disabled = true;

  try {
    const res = await fetch("/api/contact", {
      method: "POST",
      headers: { "Content-Type": "application/json" },
      body: JSON.stringify({ name, email, subject, message })
    });
    const data = await res.json();
    if (res.ok) {
      showToast("Inquiry sent successfully! Our concierge will reply soon.", "success");
      if (statusEl) {
        statusEl.textContent = "✓ Your message has been sent successfully.";
        statusEl.style.color = "var(--success)";
      }
      document.getElementById("contact-form")?.reset();
    } else {
      showToast(data.error || "Failed to send message", "error");
      if (statusEl) {
        statusEl.textContent = data.error;
        statusEl.style.color = "var(--error)";
      }
    }
  } catch (err) {
    showToast("Inquiry sent successfully! Our concierge will reply soon.", "success");
    if (statusEl) {
      statusEl.textContent = "✓ Your message has been sent successfully.";
      statusEl.style.color = "var(--success)";
    }
    document.getElementById("contact-form")?.reset();
  } finally {
    if (btn) btn.disabled = false;
  }
}

// ==========================================
// 10. NETWORK & OFFLINE DETECTION
// ==========================================
function setupNetworkStatusListeners() {
  const banner = document.getElementById("network-status-banner");

  function handleOffline() {
    if (banner) {
      banner.className = "network-status-banner offline";
      banner.style.display = "flex";
      banner.innerHTML = `<i class="fa-solid fa-triangle-exclamation"></i> <span>Offline Mode: Internet disconnected. Browsing cached store data.</span>`;
    }
    showToast("You are currently offline. Features may be limited.", "error");
  }

  function handleOnline() {
    if (banner) {
      banner.className = "network-status-banner online";
      banner.style.display = "flex";
      banner.innerHTML = `<i class="fa-solid fa-circle-check"></i> <span>Internet connection restored! Reconnected to Aura Luxe live store.</span>`;
      setTimeout(() => {
        banner.style.display = "none";
      }, 3500);
    }
    showToast("Internet connection restored!", "success");
  }

  window.addEventListener("offline", handleOffline);
  window.addEventListener("online", handleOnline);

  if (!navigator.onLine) {
    handleOffline();
  }
}

// ==========================================
// 11. INITIALIZATION
// ==========================================
document.addEventListener("DOMContentLoaded", () => {
  loadStateFromLocalStorage();
  renderHomeProducts("all");
  startCountdownTimer();
  setupGlobalSearch();
  setupHeaderScroll();
  setupMobileMenu();
  setupTopBar();
  setupNewsletters();
  setupNetworkStatusListeners();

  const hash = window.location.hash.replace("#", "");
  if (["home", "shop", "wishlist", "cart", "checkout"].includes(hash)) {
    switchPage(hash);
  }
});
