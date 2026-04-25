// Mobile Navbar Toggle
const navToggle = document.getElementById('nav-toggle');
const navLinks = document.getElementById('nav-links');
if (navToggle && navLinks) {
    navToggle.addEventListener('click', () => {
        navLinks.classList.toggle('show');
    });
}

// User Dropdown Toggle
const userMenuBtn = document.getElementById('user-menu-btn');
const userDropdown = document.getElementById('user-dropdown');
if (userMenuBtn && userDropdown) {
    userMenuBtn.addEventListener('click', (e) => {
        e.stopPropagation();
        userDropdown.classList.toggle('show');
    });

    document.addEventListener('click', (e) => {
        if (!userDropdown.contains(e.target)) {
            userDropdown.classList.remove('show');
        }
    });
}

// Password Toggle
function togglePassword(inputId) {
    const input = document.getElementById(inputId);
    const icon = input.nextElementSibling.querySelector('i');
    if (input.type === 'password') {
        input.type = 'text';
        icon.classList.remove('fa-eye');
        icon.classList.add('fa-eye-slash');
    } else {
        input.type = 'password';
        icon.classList.remove('fa-eye-slash');
        icon.classList.add('fa-eye');
    }
}

// Auto-hide Flash Messages
setTimeout(() => {
    const flashMessages = document.querySelectorAll('.flash-message');
    flashMessages.forEach(msg => {
        msg.style.opacity = '0';
        msg.style.transform = 'translateY(-10px)';
        setTimeout(() => msg.remove(), 300);
    });
}, 5000);

// Add to Cart Function
function addToCart(itemId, quantity = 1) {
    fetch('/cart/add', {
        method: 'POST',
        headers: {
            'Content-Type': 'application/json'
        },
        body: JSON.stringify({ item_id: itemId, quantity: quantity })
    })
    .then(response => {
        if (response.redirected) {
            window.location.href = response.url;
            return;
        }
        return response.json();
    })
    .then(data => {
        if (data && data.success) {
            // Update cart badge
            const badge = document.getElementById('cart-badge');
            if (badge) {
                badge.textContent = data.cart_count;
                // Animate badge
                badge.style.transform = 'scale(1.5)';
                setTimeout(() => badge.style.transform = 'scale(1)', 200);
            }
            
            // Show toast notification (simplified flash)
            showToast(data.message, 'success');
        } else if (data && data.conflict) {
            if (confirm(data.message)) {
                // Clear cart and then add
                fetch('/cart/clear', { method: 'POST', headers: {'Content-Type': 'application/json'} })
                .then(() => addToCart(itemId, quantity));
            }
        } else if (data) {
            showToast(data.message, 'error');
        }
    })
    .catch(error => console.error('Error:', error));
}

// Update Cart Item Function
function updateCartItem(cartItemId, newQuantity) {
    if (newQuantity <= 0) {
        removeCartItem(cartItemId);
        return;
    }
    
    fetch('/cart/update', {
        method: 'POST',
        headers: {
            'Content-Type': 'application/json'
        },
        body: JSON.stringify({ cart_item_id: cartItemId, quantity: newQuantity })
    })
    .then(response => response.json())
    .then(data => {
        if (data.success) {
            // Update UI elements
            document.getElementById(`qty-${cartItemId}`).textContent = newQuantity;
            document.getElementById(`total-${cartItemId}`).textContent = '₹' + data.item_total.toFixed(0);
            document.getElementById('cart-subtotal').textContent = '₹' + data.subtotal.toFixed(0);
            document.getElementById('cart-total').textContent = '₹' + data.subtotal.toFixed(0);
            
            const badge = document.getElementById('cart-badge');
            if (badge) badge.textContent = data.cart_count;
            
            // Reset discount if any (require re-applying coupon)
            const discountRow = document.getElementById('discount-row');
            if (discountRow) discountRow.style.display = 'none';
        }
    })
    .catch(error => console.error('Error:', error));
}

// Remove Cart Item Function
function removeCartItem(cartItemId) {
    if (!confirm('Remove this item from your cart?')) return;
    
    fetch('/cart/remove', {
        method: 'POST',
        headers: {
            'Content-Type': 'application/json'
        },
        body: JSON.stringify({ cart_item_id: cartItemId })
    })
    .then(response => response.json())
    .then(data => {
        if (data.success) {
            const itemElement = document.getElementById(`cart-item-${cartItemId}`);
            itemElement.style.opacity = '0';
            setTimeout(() => {
                itemElement.remove();
                if (data.cart_count === 0) {
                    location.reload(); // Reload to show empty state
                } else {
                    document.getElementById('cart-subtotal').textContent = '₹' + data.subtotal.toFixed(0);
                    document.getElementById('cart-total').textContent = '₹' + data.subtotal.toFixed(0);
                    const badge = document.getElementById('cart-badge');
                    if (badge) badge.textContent = data.cart_count;
                    
                    // Reset discount
                    const discountRow = document.getElementById('discount-row');
                    if (discountRow) discountRow.style.display = 'none';
                }
            }, 300);
        }
    })
    .catch(error => console.error('Error:', error));
}

// Apply Coupon Function (Cart Page)
function applyCoupon() {
    const codeInput = document.getElementById('coupon-code');
    const msgElement = document.getElementById('coupon-msg');
    
    if (!codeInput || !codeInput.value.trim()) {
        msgElement.textContent = 'Please enter a code';
        msgElement.className = 'coupon-msg coupon-error';
        return;
    }
    
    fetch('/cart/apply-coupon', {
        method: 'POST',
        headers: {
            'Content-Type': 'application/json'
        },
        body: JSON.stringify({ code: codeInput.value })
    })
    .then(response => response.json())
    .then(data => {
        if (data.success) {
            msgElement.textContent = data.message;
            msgElement.className = 'coupon-msg coupon-success';
            
            const subtotalText = document.getElementById('cart-subtotal').textContent;
            const subtotal = parseFloat(subtotalText.replace('₹', ''));
            const newTotal = subtotal - data.discount;
            
            const discountRow = document.getElementById('discount-row');
            if (discountRow) {
                discountRow.style.display = 'flex';
                document.getElementById('discount-amount').textContent = '-₹' + data.discount.toFixed(0);
            }
            
            document.getElementById('cart-total').textContent = '₹' + newTotal.toFixed(0);
        } else {
            msgElement.textContent = data.message;
            msgElement.className = 'coupon-msg coupon-error';
            
            const discountRow = document.getElementById('discount-row');
            if (discountRow) discountRow.style.display = 'none';
            
            const subtotalText = document.getElementById('cart-subtotal').textContent;
            document.getElementById('cart-total').textContent = subtotalText;
        }
    })
    .catch(error => console.error('Error:', error));
}

// Simple Toast Notification
function showToast(message, type = 'success') {
    let container = document.getElementById('flash-container');
    if (!container) {
        container = document.createElement('div');
        container.id = 'flash-container';
        container.className = 'flash-container';
        document.body.appendChild(container);
    }
    
    const toast = document.createElement('div');
    toast.className = `flash-message flash-${type}`;
    
    const iconClass = type === 'success' ? 'fa-check-circle' : 'fa-exclamation-circle';
    
    toast.innerHTML = `
        <i class="fas ${iconClass}"></i>
        <span>${message}</span>
        <button class="flash-close" onclick="this.parentElement.remove()"><i class="fas fa-times"></i></button>
    `;
    
    container.appendChild(toast);
    
    setTimeout(() => {
        toast.style.opacity = '0';
        toast.style.transform = 'translateY(-10px)';
        setTimeout(() => toast.remove(), 300);
    }, 4000);
}
