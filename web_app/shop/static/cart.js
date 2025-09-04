// Server-side Cart Manager for Telegram Web App
const ServerCartManager = {
  cart: { items: [], total_items: 0, total_price: 0, item_count: 0 },

  async loadCart() {
    try {
      const response = await fetch('/api/get-cart/', {
        method: 'GET',
        headers: {
          'Content-Type': 'application/json',
          'X-CSRFToken': this.getCSRFToken()
        },
        credentials: 'same-origin'
      });

      if (response.ok) {
        const data = await response.json();
        if (data.success) {
          this.cart = data.cart;
          this.updateCartUI();
        } else {
          console.error('Error loading cart:', data.error);
          // Fallback to empty cart
          this.cart = { items: [], total_items: 0, total_price: 0, item_count: 0 };
          this.updateCartUI();
        }
      } else if (response.status === 401) {
        // User not authenticated, use empty cart
        this.cart = { items: [], total_items: 0, total_price: 0, item_count: 0 };
        this.updateCartUI();
      } else {
        throw new Error(`HTTP ${response.status}`);
      }
    } catch (error) {
      console.error('Error loading cart:', error);
      // Fallback to empty cart
      this.cart = { items: [], total_items: 0, total_price: 0, item_count: 0 };
      this.updateCartUI();
    }
  },

  async addToCart(product) {
    try {
      // Get customization data if on product page
      const customizationData = this.getCustomizationData();
      const customizationPrice = this.getCustomizationPrice();
      
      const response = await fetch('/api/add-to-cart/', {
        method: 'POST',
        headers: {
          'Content-Type': 'application/json',
          'X-CSRFToken': this.getCSRFToken()
        },
        credentials: 'same-origin',
        body: JSON.stringify({
          product_id: product.id,
          quantity: product.qty || 1,
          customization: customizationData,
          customization_price: customizationPrice
        })
      });

      const data = await response.json();
      
      if (data.success) {
        // Update cart count in UI
        this.cart.total_items = data.cart_item_count;
        this.cart.total_price = data.cart_total;
        this.updateCartUI();
        
        // Show success message
        this.showToast(data.message || 'Added to cart successfully!', 'success');
        
        return true;
      } else {
        this.showToast(data.error || 'Failed to add to cart', 'error');
        return false;
      }
    } catch (error) {
      console.error('Error adding to cart:', error);
      this.showToast('Network error. Please try again.', 'error');
      return false;
    }
  },

  async updateQuantity(itemId, newQuantity) {
    try {
      const response = await fetch('/api/update-cart-item/', {
        method: 'POST',
        headers: {
          'Content-Type': 'application/json',
          'X-CSRFToken': this.getCSRFToken()
        },
        credentials: 'same-origin',
        body: JSON.stringify({
          item_id: itemId,
          quantity: newQuantity
        })
      });

      const data = await response.json();
      
      if (data.success) {
        // Reload cart to get updated data
        await this.loadCart();
        this.showToast('Cart updated successfully!', 'success');
        return true;
      } else {
        this.showToast(data.error || 'Failed to update cart', 'error');
        return false;
      }
    } catch (error) {
      console.error('Error updating cart:', error);
      this.showToast('Network error. Please try again.', 'error');
      return false;
    }
  },

  async removeFromCart(itemId) {
    try {
      const response = await fetch('/api/remove-from-cart/', {
        method: 'POST',
        headers: {
          'Content-Type': 'application/json',
          'X-CSRFToken': this.getCSRFToken()
        },
        credentials: 'same-origin',
        body: JSON.stringify({
          item_id: itemId
        })
      });

      const data = await response.json();
      
      if (data.success) {
        // Reload cart to get updated data
        await this.loadCart();
        this.showToast('Item removed from cart', 'success');
        return true;
      } else {
        this.showToast(data.error || 'Failed to remove item', 'error');
        return false;
      }
    } catch (error) {
      console.error('Error removing from cart:', error);
      this.showToast('Network error. Please try again.', 'error');
      return false;
    }
  },

  async clearCart() {
    try {
      const response = await fetch('/api/clear-cart/', {
        method: 'POST',
        headers: {
          'Content-Type': 'application/json',
          'X-CSRFToken': this.getCSRFToken()
        },
        credentials: 'same-origin'
      });

      const data = await response.json();
      
      if (data.success) {
        this.cart = { items: [], total_items: 0, total_price: 0, item_count: 0 };
        this.updateCartUI();
        this.showToast('Cart cleared successfully!', 'success');
        return true;
      } else {
        this.showToast(data.error || 'Failed to clear cart', 'error');
        return false;
      }
    } catch (error) {
      console.error('Error clearing cart:', error);
      this.showToast('Network error. Please try again.', 'error');
      return false;
    }
  },

  getCustomizationData() {
    const customizationData = {};
    const customizationSelects = document.querySelectorAll('select[data-customization-type]');
    
    customizationSelects.forEach(select => {
      const type = select.getAttribute('data-customization-type');
      const value = select.value;
      if (value && value !== '') {
        customizationData[type] = value;
      }
    });
    
    return Object.keys(customizationData).length > 0 ? customizationData : null;
  },

  getCustomizationPrice() {
    const customizationSelects = document.querySelectorAll('select[data-customization-type]');
    let totalCustomizationPrice = 0;
    
    customizationSelects.forEach(select => {
      const selectedOption = select.options[select.selectedIndex];
      const priceModifier = parseFloat(selectedOption.getAttribute('data-price')) || 0;
      totalCustomizationPrice += priceModifier;
    });
    
    return totalCustomizationPrice.toFixed(2);
  },

  updateCartUI() {
    // Update cart item count in navigation
    const cartCountElements = document.querySelectorAll('.cart-item-count');
    cartCountElements.forEach(element => {
      element.textContent = this.cart.total_items || 0;
      // Only show the badge if there are items, and ensure it's visible after loading
      if (this.cart.total_items > 0) {
        element.style.display = 'flex';
        element.style.visibility = 'visible';
      } else {
        element.style.display = 'none';
        element.style.visibility = 'visible';
      }
    });

    // Update cart page if we're on it
    if (window.location.pathname.includes('/cart/')) {
      this.renderCartPage();
    }
  },

  renderCartPage() {
    const cartContainer = document.querySelector('.cart-items-container, #cart-items');
    const cartSummary = document.querySelector('.cart-summary, #cart-summary');
    
    if (!cartContainer) return;

    if (this.cart.items.length === 0) {
      cartContainer.innerHTML = `
        <div class="text-center py-12">
          <svg class="lucide lucide-shopping-bag mx-auto text-luxury-gray mb-4" fill="none" height="64" stroke="currentColor" stroke-linecap="round" stroke-linejoin="round" stroke-width="2" viewBox="0 0 24 24" width="64" xmlns="http://www.w3.org/2000/svg">
            <path d="M6 2 3 6v14a2 2 0 0 0 2 2h14a2 2 0 0 0 2-2V6l-3-4Z"></path>
            <path d="M3 6h18"></path>
            <path d="M16 10a4 4 0 0 1-8 0"></path>
          </svg>
          <h3 class="text-xl font-semibold text-luxury-black mb-2">Your cart is empty</h3>
          <p class="text-luxury-gray-dark mb-6">Discover our luxury timepieces and add them to your cart</p>
          <a href="/catalog/" class="inline-flex items-center justify-center px-6 py-3 bg-luxury-gold hover:bg-luxury-gold-dark text-luxury-black font-semibold rounded-lg transition-colors">
            Browse Products
          </a>
        </div>
      `;
      if (cartSummary) cartSummary.style.display = 'none';
      return;
    }

    // Render cart items
    const cartHTML = this.cart.items.map(item => `
      <div class="flex items-center gap-4 p-4 border border-luxury-gray rounded-lg mb-4" data-item-id="${item.id}">
        <div class="w-20 h-20 bg-luxury-gray rounded-lg overflow-hidden">
          <img src="${item.product.image || '/static/hero-watch-D40AmJ87.jpg'}" alt="${item.product.name}" class="w-full h-full object-cover">
        </div>
        <div class="flex-1">
          <h3 class="font-semibold text-luxury-black">${item.product.name}</h3>
          <p class="text-sm text-luxury-gray-dark">${item.product.brand}</p>
          <p class="text-lg font-bold text-luxury-gold">$${item.total_price.toFixed(2)}</p>
        </div>
        <div class="flex items-center gap-2">
          <button class="quantity-btn minus-btn w-8 h-8 rounded-full border border-luxury-gray flex items-center justify-center text-luxury-gray-dark hover:text-luxury-black hover:border-luxury-gold transition-colors" data-item-id="${item.id}" data-action="decrease">-</button>
          <span class="quantity-display w-8 text-center font-medium">${item.quantity}</span>
          <button class="quantity-btn plus-btn w-8 h-8 rounded-full border border-luxury-gray flex items-center justify-center text-luxury-gray-dark hover:text-luxury-black hover:border-luxury-gold transition-colors" data-item-id="${item.id}" data-action="increase">+</button>
        </div>
        <button class="remove-btn text-red-500 hover:text-red-700 p-2 transition-colors" data-item-id="${item.id}">
          <svg xmlns="http://www.w3.org/2000/svg" width="20" height="20" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2">
            <path d="M3 6h18"></path>
            <path d="M19 6v14c0 1-1 2-2 2H7c-1 0-2-1-2-2V6"></path>
            <path d="M8 6V4c0-1 1-2 2-2h4c1 0 2 1 2 2v2"></path>
          </svg>
        </button>
      </div>
    `).join('');

    cartContainer.innerHTML = cartHTML;

    // Update cart summary
    if (cartSummary) {
      cartSummary.style.display = 'block';
      cartSummary.innerHTML = `
        <div class="bg-luxury-white p-6 rounded-lg border border-luxury-gray sticky top-4">
          <h3 class="text-xl font-semibold text-luxury-black mb-4">Order Summary</h3>
          <div class="space-y-2 mb-4">
            <div class="flex justify-between">
              <span class="text-luxury-gray-dark">Items (${this.cart.total_items})</span>
              <span class="font-semibold">$${this.cart.total_price.toFixed(2)}</span>
            </div>
            <div class="flex justify-between">
              <span class="text-luxury-gray-dark">Shipping</span>
              <span class="font-semibold text-green-600">Free</span>
            </div>
            <div class="flex justify-between">
              <span class="text-luxury-gray-dark">Tax</span>
              <span class="font-semibold">Included</span>
            </div>
            <hr class="border-luxury-gray">
            <div class="flex justify-between text-xl font-bold text-luxury-black">
              <span>Total</span>
              <span class="text-luxury-gold">$${this.cart.total_price.toFixed(2)}</span>
            </div>
          </div>
          <button class="w-full bg-luxury-gold hover:bg-luxury-gold-dark text-luxury-black font-semibold py-3 rounded-lg transition-colors mb-3 place-order-btn">
            Place Order
          </button>
          <button class="w-full border border-luxury-gray text-luxury-gray-dark hover:text-luxury-black py-3 rounded-lg transition-colors clear-cart-btn">
            Clear Cart
          </button>
        </div>
      `;
    }

    // Attach event listeners
    this.attachCartListeners();
  },

  attachCartListeners() {
    // Quantity change buttons
    document.querySelectorAll('.quantity-btn').forEach(btn => {
      btn.addEventListener('click', async (e) => {
        e.preventDefault();
        const itemId = btn.getAttribute('data-item-id');
        const action = btn.getAttribute('data-action');
        const currentQuantity = parseInt(btn.parentElement.querySelector('.quantity-display').textContent);
        
        let newQuantity = currentQuantity;
        if (action === 'increase') {
          newQuantity = currentQuantity + 1;
        } else if (action === 'decrease' && currentQuantity > 1) {
          newQuantity = currentQuantity - 1;
        }
        
        if (newQuantity !== currentQuantity) {
          // Show loading
          btn.disabled = true;
          const originalText = btn.textContent;
          btn.textContent = '...';
          
          const success = await this.updateQuantity(itemId, newQuantity);
          
          // Reset button
          btn.disabled = false;
          btn.textContent = originalText;
        }
      });
    });

    // Remove buttons
    document.querySelectorAll('.remove-btn').forEach(btn => {
      btn.addEventListener('click', async (e) => {
        e.preventDefault();
        const itemId = btn.getAttribute('data-item-id');
        
        // Show loading
        btn.disabled = true;
        btn.style.opacity = '0.5';
        
        const success = await this.removeFromCart(itemId);
        
        // Reset button (in case of error)
        btn.disabled = false;
        btn.style.opacity = '1';
      });
    });

    // Clear cart button
    const clearCartBtn = document.querySelector('.clear-cart-btn');
    if (clearCartBtn) {
      clearCartBtn.addEventListener('click', async (e) => {
        e.preventDefault();
        if (confirm('Are you sure you want to clear your cart?')) {
          clearCartBtn.disabled = true;
          clearCartBtn.textContent = 'Clearing...';
          
          const success = await this.clearCart();
          
          clearCartBtn.disabled = false;
          clearCartBtn.textContent = 'Clear Cart';
        }
      });
    }

    // Place Order button
    const placeOrderBtn = document.querySelector('.place-order-btn');
    if (placeOrderBtn) {
      placeOrderBtn.addEventListener('click', async (e) => {
        e.preventDefault();
        console.log('Place order button clicked - cart.js handler');
        
        // Check if cart is empty
        if (this.cart.items.length === 0) {
          this.showToast('Your cart is empty', 'error');
          return;
        }
        
        console.log('Redirecting to checkout page...');
        // Redirect to checkout page instead of creating order directly
        window.location.href = '/checkout/';
      });
    }
  },

  getCartItems() {
    return this.cart.items;
  },

  getCartCount() {
    return this.cart.total_items;
  },

  getCartTotal() {
    return this.cart.total_price;
  },

  getCSRFToken() {
    const cookies = document.cookie.split(';');
    for (let cookie of cookies) {
      const [name, value] = cookie.trim().split('=');
      if (name === 'csrftoken') {
        return value;
      }
    }
    
    // Fallback: try to get from meta tag
    const csrfMeta = document.querySelector('meta[name="csrf-token"]');
    if (csrfMeta) {
      return csrfMeta.getAttribute('content');
    }
    
    return '';
  },

  showToast(message, type = 'info') {
    // Create toast notification
    const toast = document.createElement('div');
    toast.className = `fixed top-4 right-4 z-[9999] px-6 py-4 rounded-lg font-medium transition-all transform translate-x-full opacity-0 shadow-lg`;
    // Apply inline styles to ensure background color works with maximum priority
    toast.style.cssText = `
      background-color: #facc15 !important;
      color: #000000 !important;
      z-index: 9999 !important;
      opacity: 1 !important;
      background-image: none !important;
      border: none !important;
    `;
    
    if (type === 'success') {
      toast.innerHTML = `
        <div class="flex items-center">
          <svg class="w-5 h-5 mr-3" fill="none" stroke="currentColor" viewBox="0 0 24 24">
            <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M5 13l4 4L19 7"></path>
          </svg>
          <span>${message}</span>
        </div>
      `;
    } else if (type === 'error') {
      toast.innerHTML = `
        <div class="flex items-center">
          <svg class="w-5 h-5 mr-3" fill="none" stroke="currentColor" viewBox="0 0 24 24">
            <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M6 18L18 6M6 6l12 12"></path>
          </svg>
          <span>${message}</span>
        </div>
      `;
    } else {
      toast.innerHTML = `
        <div class="flex items-center">
          <svg class="w-5 h-5 mr-3" fill="none" stroke="currentColor" viewBox="0 0 24 24">
            <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M13 16h-1v-4h-1m1-4h.01M21 12a9 9 0 11-18 0 9 9 0 0118 0z"></path>
          </svg>
          <span>${message}</span>
        </div>
      `;
    }
    
    document.body.appendChild(toast);
    
    // Show toast
    setTimeout(() => {
      toast.classList.remove('translate-x-full', 'opacity-0');
    }, 100);
    
    // Hide toast
    setTimeout(() => {
      toast.classList.add('translate-x-full', 'opacity-0');
      setTimeout(() => {
        if (document.body.contains(toast)) {
          document.body.removeChild(toast);
        }
      }, 300);
    }, 4000); // Increased duration to 4 seconds for better readability
  },

  // Handle add to cart button clicks
  async handleAddToCartClick(button) {
    const product = {
      id: button.getAttribute('data-id'),
      name: button.getAttribute('data-name'),
      price: parseFloat(button.getAttribute('data-price')) || 0,
      qty: 1, // Default quantity
      image: button.getAttribute('data-image'),
      brand: button.getAttribute('data-brand')
    };
    
    // Get quantity from product page if available
    const quantityDisplay = document.getElementById('quantity-display');
    if (quantityDisplay) {
      product.qty = parseInt(quantityDisplay.textContent) || 1;
    }
    
    // Validate required data
    if (!product.id || !product.name || isNaN(product.price)) {
      console.error('Invalid product data:', product);
      this.showToast('Invalid product data', 'error');
      return;
    }
    
    // Show loading state
    const originalText = button.textContent;
    button.innerHTML = `
      <svg class="animate-spin h-5 w-5 mr-2" viewBox="0 0 24 24">
        <circle class="opacity-25" cx="12" cy="12" r="10" stroke="currentColor" stroke-width="4" fill="none"></circle>
        <path class="opacity-75" fill="currentColor" d="M4 12a8 8 0 018-8V0C5.373 0 0 5.373 0 12h4zm2 5.291A7.962 7.962 0 014 12H0c0 3.042 1.135 5.824 3 7.938l3-2.647z"></path>
      </svg>
      Adding...
    `;
    button.disabled = true;
    
    try {
      const success = await this.addToCart(product);
      
      if (success) {
        button.innerHTML = `
          <svg xmlns="http://www.w3.org/2000/svg" width="20" height="20" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" class="mr-2">
            <path d="M20 6L9 17l-5-5"/>
          </svg>
          Added!
        `;
        setTimeout(() => {
          button.innerHTML = originalText;
          button.disabled = false;
        }, 2000);
      } else {
        button.innerHTML = originalText;
        button.disabled = false;
      }
    } catch (error) {
      console.error('Error adding to cart:', error);
      button.innerHTML = originalText;
      button.disabled = false;
    }
  }
};

// Initialize cart when DOM is loaded
document.addEventListener('DOMContentLoaded', async () => {
  // Load cart data
  await ServerCartManager.loadCart();
  
  // Replace the old CartManager with ServerCartManager
  window.CartManager = ServerCartManager;
  
  // Attach event listeners to existing add-to-cart buttons
  document.querySelectorAll('.add-to-cart').forEach(button => {
    button.addEventListener('click', async (e) => {
      e.preventDefault();
      await ServerCartManager.handleAddToCartClick(button);
    });
  });
  
  console.log('Server-side CartManager initialized');
});
