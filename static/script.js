// ==================== SEARCH AND FILTER FUNCTIONALITY ====================

// Global state for filtering
let currentSearchTerm = '';
let currentCategory = 'all';
let visibleCardsCount = 50; // Initial load count
let allCards = [];
let isLoading = false;

/**
 * Initialize lazy loading on page load
 */
function initializeLazyLoading() {
    allCards = Array.from(document.querySelectorAll('.card'));
    
    // Initially hide all cards except first batch
    allCards.forEach((card, index) => {
        if (index >= visibleCardsCount) {
            card.style.display = 'none';
            card.dataset.lazyLoaded = 'false';
        } else {
            card.dataset.lazyLoaded = 'true';
        }
    });

    // Setup intersection observer for infinite scroll
    setupInfiniteScroll();
}

/**
 * Setup infinite scroll to load more cards as user scrolls
 */
function setupInfiniteScroll() {
    const options = {
        root: null,
        rootMargin: '100px',
        threshold: 0.1
    };

    const observer = new IntersectionObserver((entries) => {
        entries.forEach(entry => {
            if (entry.isIntersecting && !isLoading) {
                loadMoreCards();
            }
        });
    }, options);

    // Create a sentinel element at the bottom
    const sentinel = document.createElement('div');
    sentinel.id = 'scroll-sentinel';
    sentinel.style.height = '1px';
    const cardGrid = document.getElementById('cardGrid');
    if (cardGrid) {
        cardGrid.appendChild(sentinel);
        observer.observe(sentinel);
    }
}

/**
 * Load more cards progressively
 */
function loadMoreCards() {
    if (isLoading) return;
    
    isLoading = true;
    const loadBatchSize = 50;
    
    // Filter cards that match current search/category and aren't loaded yet
    const unloadedCards = allCards.filter(card => {
        const matchesSearch = cardMatchesSearch(card);
        const matchesCategory = cardMatchesCategory(card);
        const isUnloaded = card.dataset.lazyLoaded === 'false';
        return matchesSearch && matchesCategory && isUnloaded;
    });

    // Load next batch
    const cardsToLoad = unloadedCards.slice(0, loadBatchSize);
    cardsToLoad.forEach(card => {
        card.style.display = 'flex';
        card.dataset.lazyLoaded = 'true';
    });

    visibleCardsCount += cardsToLoad.length;
    
    setTimeout(() => {
        isLoading = false;
    }, 100);
}

/**
 * Check if card matches current search term
 */
function cardMatchesSearch(card) {
    if (currentSearchTerm === '') return true;
    
    const cardName = card.getAttribute('data-name') || '';
    const cardColor = card.getAttribute('data-color') || '';
    const cardId = card.getAttribute('data-id') || '';
    
    return cardName.includes(currentSearchTerm) || 
           cardColor.includes(currentSearchTerm) || 
           cardId.includes(currentSearchTerm);
}

/**
 * Check if card matches current category
 */
function cardMatchesCategory(card) {
    if (currentCategory === 'all') return true;
    
    const cardCategory = card.getAttribute('data-category') || '';
    return cardCategory === currentCategory;
}

/**
 * Search products by term - matches name, color, or ID
 * @param {string} searchTerm - Search query to filter products
 */
function searchProducts(searchTerm) {
    currentSearchTerm = searchTerm.toLowerCase();
    // Reset category to 'all' when searching
    currentCategory = 'all';
    const categorySelect = document.getElementById('categoryFilter');
    if (categorySelect) {
        categorySelect.value = 'all';
    }
    // Reset lazy loading
    visibleCardsCount = 50;
    applyFilters();
}

/**
 * Filter products by category
 * @param {string} category - Category name to filter by, or 'all' for no filter
 */
function filterByCategory(category) {
    currentCategory = category;
    visibleCardsCount = 50; // Reset on category change
    applyFilters();
}

/**
 * Apply both search and category filters to product cards
 * Shows/hides cards based on current filter state
 */
function applyFilters() {
    const cards = document.querySelectorAll('.card');
    let visibleCount = 0;
    
    cards.forEach(card => {
        const matchesSearch = cardMatchesSearch(card);
        const matchesCategory = cardMatchesCategory(card);
        
        // Show card only if it matches both criteria and is within visible limit
        if (matchesSearch && matchesCategory) {
            if (visibleCount < visibleCardsCount) {
                card.style.display = 'flex';
                card.dataset.lazyLoaded = 'true';
                visibleCount++;
            } else {
                card.style.display = 'none';
                card.dataset.lazyLoaded = 'false';
            }
        } else {
            card.style.display = 'none';
            card.dataset.lazyLoaded = 'false';
        }
    });
}

// Show/hide clear search button
function toggleClearSearchButton() {
    const searchInput = document.getElementById('searchInput');
    const clearSearchBtn = document.getElementById('clearSearchBtn');
    
    if (searchInput && clearSearchBtn) {
        if (searchInput.value.length > 0) {
            clearSearchBtn.style.display = 'flex';
        } else {
            clearSearchBtn.style.display = 'none';
        }
    }
}

// ==================== CART STATE ====================

// Cart state - stored in localStorage
let cart = [];

// Load cart from localStorage on page load
function loadCart() {
    const savedCart = localStorage.getItem('rekubricksCart');
    if (savedCart) {
        cart = JSON.parse(savedCart);
        updateCartDisplay();
        updateAllCardButtons();
    }
}

// Save cart to localStorage
function saveCart() {
    localStorage.setItem('rekubricksCart', JSON.stringify(cart));
}

// ==================== CART UI UPDATES ====================

// Update cart counter in header
function updateCartCount() {
    const uniqueItems = cart.length;
    document.getElementById('cartCount').textContent = uniqueItems;
}

// Update cart display in panel
function updateCartDisplay() {
    const cartItemsContainer = document.getElementById('cartItems');
    const subtotalElement = document.getElementById('subtotalAmount');
    
    updateCartCount();
    
    if (cart.length === 0) {
        cartItemsContainer.innerHTML = `
            <div class="cart-empty">
                <div class="cart-empty-icon">🛒</div>
                <p>Tu carrito está vacío</p>
            </div>
        `;
        subtotalElement.textContent = 'Q0.00';
        return;
    }
    
    // TODO: allow local images, maybe using gcp realtime database 
    // Render cart items
    cartItemsContainer.innerHTML = cart.map(item => `
        <div class="cart-item">
            <div class="cart-item-top">
                <div class="cart-item-image">
                    <img src="${item.image}" alt="${item.name}">
                </div>
                <div class="cart-item-details">
                    <div class="cart-item-name">${item.name}</div>
                    <div class="cart-item-color">Color: <strong>${item.color}</strong></div>
                </div>
            </div>
            <div class="cart-item-bottom">
                <div class="quantity-controls">
                    <button class="quantity-btn" onclick="updateCartItemQuantity('${item.id}', -1)">−</button>
                    <input type="number" class="quantity-input" value="${item.quantity}" step="1" onchange="updateCartItemQuantity('${item.id}', this.value)">
                    <button class="quantity-btn" onclick="updateCartItemQuantity('${item.id}', 1)">+</button>
                </div>
                <div class="cart-item-price">Q${(item.price * item.quantity).toFixed(2)}</div>
                <button class="delete-item-btn" onclick="deleteCartItem('${item.id}')">
                    <svg width="16" height="16" viewBox="0 0 24 24" fill="none" stroke="white" stroke-width="2">
                        <path d="M3 6h18"></path>
                        <path d="M8 6v-2a2 2 0 0 1 2-2h4a2 2 0 0 1 2 2v2"></path>
                        <path d="M6 6v14a2 2 0 0 0 2 2h8a2 2 0 0 0 2-2V6"></path>
                        <path d="M10 11v6"></path>
                        <path d="M14 11v6"></path>
                    </svg>
                </button>
            </div>
        </div>
    `).join('');
    
    // Calculate subtotal
    const subtotal = cart.reduce((sum, item) => sum + (item.price * item.quantity), 0);
    subtotalElement.textContent = `Q${subtotal.toFixed(2)}`;
}

// ==================== CART ACTIONS ====================

// Add item to cart or increase quantity
function addToCart(id, pieceId, idColor, idMolde, name, color, price, image) {
    const existingItem = cart.find(item => item.id === id);
    
    if (existingItem) {
        existingItem.quantity += 1;
    } else {
        cart.push({
            id: id,
            pieceId: pieceId,
            idColor: idColor,
            idMolde: idMolde,
            name: name,
            color: color,
            price: parseFloat(price),
            image: image,
            quantity: 1
        });
    }
    
    saveCart();
    updateCartDisplay();
    updateCardButton(id);
}

// Update quantity from cart panel
function updateCartItemQuantity(id, change) {
    const item = cart.find(item => item.id === id);
    
    if (item) {
        const newQuantity = typeof change === 'string' ? parseInt(change) : item.quantity + change;
        if (isNaN(newQuantity) || newQuantity < 0) {
            alert('Por favor, ingrese una cantidad válida (0 o mayor).');
            updateCartDisplay(); // Reset input to current quantity
            return;
        }
        item.quantity = newQuantity;
        
        if (item.quantity <= 0) {
            cart = cart.filter(i => i.id !== id);
        }
        
        saveCart();
        updateCartDisplay();
        updateCardButton(id);
    }
}

// Delete item from cart
function deleteCartItem(id) {
    if (confirm('¿Estás seguro de que quieres eliminar este ítem del carrito?')) {
        cart = cart.filter(item => item.id !== id);
        saveCart();
        updateCartDisplay();
        updateCardButton(id);
    }
}

// ==================== WHATSAPP INTEGRATION ====================

// Generate WhatsApp message and open link
function sendOrderToWhatsApp() {
    if (cart.length === 0) {
        alert('El carrito está vacío. Añade productos antes de enviar el pedido.');
        return;
    }

    // Calculate subtotal
    const subtotal = cart.reduce((sum, item) => sum + (item.price * item.quantity), 0);

    // Create message
    let message = 'Hola, quisiera realizar un pedido:\n\n';
    message += 'Detalle:\n';
    cart.forEach(item => {
        let idInfo = '';
        // Clean .0 from numeric IDs and handle 'nan' values
        const cleanIdColor = item.idColor && item.idColor !== '' && item.idColor !== 'nan' ? String(item.idColor).replace('.0', '') : '';
        const cleanIdMolde = item.idMolde && item.idMolde !== 'nan' ? String(item.idMolde).replace('.0', '') : '';
        
        if (cleanIdColor && cleanIdColor !== '') {
            idInfo = `ID Esp: ${cleanIdColor}, Item: ${cleanIdMolde}`;
        } else {
            idInfo = `Item: ${cleanIdMolde}`;
        }
        message += `- ${idInfo}, Color: ${item.color}, Cantidad: ${item.quantity}\n`;
    });
    message += `\nSubtotal: Q${subtotal.toFixed(2)}`;

    // Encode message and create WhatsApp URL
    const phoneNumber = '+50253771641';
    const encodedMessage = encodeURIComponent(message);
    const whatsappUrl = `https://wa.me/${phoneNumber}?text=${encodedMessage}`;

    // Open WhatsApp
    window.open(whatsappUrl, '_blank');
}

// ==================== CARD BUTTON UI ====================

// Update a specific card's button
function updateCardButton(id) {
    // Use more specific selector to target only the button, not the card wrapper
    const button = document.querySelector(`.add-to-cart-btn[data-id="${id}"], .quantity-control-wrapper[data-id="${id}"]`);
    if (!button) return;
    
    const item = cart.find(item => item.id === id);
    
    if (!item || item.quantity === 0) {
        // Show "Add to Cart" button
        button.className = 'add-to-cart-btn';
        button.innerHTML = 'Añadir al Carrito';
        // Set data attributes for event delegation
        button.dataset.id = id;
        button.onclick = null; // Remove any existing onclick handler
    } else {
        // Show quantity controls with input and trash button
        button.className = 'quantity-control-wrapper';
        button.innerHTML = `
            <button class="delete-item-btn" onclick="event.stopPropagation(); deleteCartItem('${id}')">
                <svg width="14" height="14" viewBox="0 0 24 24" fill="none" stroke="white" stroke-width="2">
                    <path d="M3 6h18"></path>
                    <path d="M8 6v-2a2 2 0 0 1 2-2h4a2 2 0 0 1 2 2v2"></path>
                    <path d="M6 6v14a2 2 0 0 0 2 2h8a2 2 0 0 0 2-2V6"></path>
                    <path d="M10 11v6"></path>
                    <path d="M14 11v6"></path>
                </svg>
            </button>
            <button class="quantity-btn" onclick="event.stopPropagation(); updateCartItemQuantity('${id}', -1)">−</button>
            <input type="number" class="quantity-input" value="${item.quantity}" step="1" onchange="event.stopPropagation(); updateCartItemQuantity('${id}', this.value)" onclick="event.stopPropagation();">
            <button class="quantity-btn" onclick="event.stopPropagation(); updateCartItemQuantity('${id}', 1)">+</button>
        `;
        // TODO: data validation, only allow ints
        button.onclick = null;
    }
}

// Update all card buttons on page load
function updateAllCardButtons() {
    // Only select actual buttons, not card wrappers
    const buttons = document.querySelectorAll('.add-to-cart-btn[data-id], .quantity-control-wrapper[data-id]');
    buttons.forEach(button => updateCardButton(button.dataset.id));
}

// ==================== CART PANEL TOGGLE ====================

function clearCart() {
    if (confirm('¿Estás seguro de que quieres vaciar el carrito?')) {
        cart = [];
        saveCart();
        updateCartDisplay();
        updateAllCardButtons();
    }
}

function toggleCart() {
    document.getElementById('cartPanel').classList.toggle('active');
    document.getElementById('cartOverlay').classList.toggle('active');
}

function closeCart() {
    document.getElementById('cartPanel').classList.remove('active');
    document.getElementById('cartOverlay').classList.remove('active');
}

// ==================== INITIALIZATION ====================

document.addEventListener('DOMContentLoaded', function() {
    // Load cart state
    loadCart();

    // Cart button click
    document.getElementById('cartButton').addEventListener('click', toggleCart);

    // Close button click
    document.getElementById('cartClose').addEventListener('click', closeCart);

    // Overlay click
    document.getElementById('cartOverlay').addEventListener('click', closeCart);

    // Clear cart button
    document.getElementById('clearCartBtn').addEventListener('click', clearCart);

    // WhatsApp button click
    document.getElementById('whatsappBtn').addEventListener('click', sendOrderToWhatsApp);

    // Add to cart buttons - using event delegation to avoid duplicate listeners
    document.addEventListener('click', function(e) {
        if (e.target.classList.contains('add-to-cart-btn')) {
            addToCart(
                e.target.dataset.id,
                e.target.dataset.pieceId,
                e.target.dataset.idColor, 
                e.target.dataset.idMolde, 
                e.target.dataset.name,
                e.target.dataset.color,
                e.target.dataset.price,
                e.target.dataset.image
            );
        }
    });

    // Search input
    const searchInput = document.getElementById('searchInput');
    if (searchInput) {
        searchInput.addEventListener('input', function(e) {
            searchProducts(e.target.value);
            toggleClearSearchButton();
        });
    }

    // Category dropdown
    const categoryFilter = document.getElementById('categoryFilter');
    if (categoryFilter) {
        categoryFilter.addEventListener('change', function(e) {
            filterByCategory(e.target.value);
        });
    }

    // Clear search button (X)
    const clearSearchBtn = document.getElementById('clearSearchBtn');
    if (clearSearchBtn) {
        clearSearchBtn.addEventListener('click', function() {
            document.getElementById('searchInput').value = '';
            searchProducts('');
            toggleClearSearchButton();
        });
    }

    // Initialize lazy loading
    initializeLazyLoading();
});