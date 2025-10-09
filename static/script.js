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
    const totalItems = cart.reduce((sum, item) => sum + item.quantity, 0);
    document.getElementById('cartCount').textContent = totalItems;
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
    
    // Render cart items
    cartItemsContainer.innerHTML = cart.map(item => `
        <div class="cart-item">
            <div class="cart-item-image">
                <img src="${item.image}" alt="${item.name}">
            </div>
            <div class="cart-item-details">
                <div class="cart-item-name">${item.name}</div>
                <div class="cart-item-color">Color: <strong>${item.color}</strong></div>
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
        </div>
    `).join('');
    
    // Calculate subtotal
    const subtotal = cart.reduce((sum, item) => sum + (item.price * item.quantity), 0);
    subtotalElement.textContent = `Q${subtotal.toFixed(2)}`;
}

// ==================== CART ACTIONS ====================

// Add item to cart or increase quantity
function addToCart(id, pieceId, name, color, price, image) {
    console.log(`Adding to cart: ID=${id}, PieceID=${pieceId}, Name=${name}, Color=${color}`); // Debug
    const existingItem = cart.find(item => item.id === id);
    
    if (existingItem) {
        existingItem.quantity += 1;
    } else {
        cart.push({
            id: id,
            pieceId: pieceId,
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
    console.log(`Updating quantity: ID=${id}, Change=${change}`); // Debug
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

// Update quantity from product card
function updateCardQuantity(id, change) {
    updateCartItemQuantity(id, change);
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
        message += `- ID: ${item.pieceId}, Nombre: ${item.name}, Cantidad: ${item.quantity}\n`;
    });
    message += `\nSubtotal: Q${subtotal.toFixed(2)}`;

    // Encode message and create WhatsApp URL
    const phoneNumber = '+50252054584';
    const encodedMessage = encodeURIComponent(message);
    const whatsappUrl = `https://wa.me/${phoneNumber}?text=${encodedMessage}`;

    // Open WhatsApp
    window.open(whatsappUrl, '_blank');
}

// ==================== CARD BUTTON UI ====================

// Update a specific card's button
function updateCardButton(id) {
    const button = document.querySelector(`[data-id="${id}"]`);
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
            <button class="quantity-btn" onclick="event.stopPropagation(); updateCardQuantity('${id}', -1)">−</button>
            <input type="number" class="quantity-input" value="${item.quantity}" step="1" onchange="event.stopPropagation(); updateCartItemQuantity('${id}', this.value)" onclick="event.stopPropagation();">
            <button class="quantity-btn" onclick="event.stopPropagation(); updateCardQuantity('${id}', 1)">+</button>
        `;
        button.onclick = null;
    }
}

// Update all card buttons on page load
function updateAllCardButtons() {
    const buttons = document.querySelectorAll('[data-id]');
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
    console.log('Toggling cart'); // Debug
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
                e.target.dataset.name,
                e.target.dataset.color,
                e.target.dataset.price,
                e.target.dataset.image
            );
        }
    });
});