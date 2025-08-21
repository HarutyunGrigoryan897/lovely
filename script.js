(function() {
  // Mapping of nav items to paths
  const navMap = {
    'Home': '/',
    'Catalog': '/catalog/',
    'Cart': '/cart/',
    'Account': '/account/'
  };

  // Set up navigation click events
  document.addEventListener('DOMContentLoaded', () => {
    document.querySelectorAll('button').forEach(btn => {
      const span = btn.querySelector('span.text-xs');
      if (span) {
        const dest = navMap[span.textContent.trim()];
        if (dest) {
          btn.addEventListener('click', () => {
            window.location.href = dest;
          });
        }
      }
    });

    // Initialize cart UI and events
    updateCartUI(loadCart());
    initAddToCart();
  });

  // Generic toggle elements using data-toggle-target
  document.addEventListener('click', (event) => {
    const toggleEl = event.target.closest('[data-toggle-target]');
    if (toggleEl) {
      const selector = toggleEl.getAttribute('data-toggle-target');
      const target = document.querySelector(selector);
      if (target) {
        target.classList.toggle('hidden');
      }
    }
  });

  // Load cart from localStorage
  function loadCart() {
    try {
      return JSON.parse(localStorage.getItem('cartItems')) || [];
    } catch (e) {
      return [];
    }
  }

  // Save cart to localStorage and update UI
  function saveCart(items) {
    localStorage.setItem('cartItems', JSON.stringify(items));
    updateCartUI(items);
  }

  // Add item to cart
  function addToCart(item) {
    const items = loadCart();
    const existing = items.find(it => it.id === item.id);
    if (existing) {
      existing.qty += 1;
    } else {
      items.push({ id: item.id, name: item.name, price: item.price, qty: 1 });
    }
    saveCart(items);
  }

  // Update cart UI by modifying cart text
  function updateCartUI(items) {
    const count = items.reduce((sum, it) => sum + it.qty, 0);
    document.querySelectorAll('span.text-xs').forEach(span => {
      if (span.textContent.trim().startsWith('Cart')) {
        span.textContent = 'Cart' + (count > 0 ? ' (' + count + ')' : '');
      }
    });
  }

  // Initialize add-to-cart event listeners
  function initAddToCart() {
    // Buttons with data-add-to-cart attribute
    document.querySelectorAll('[data-add-to-cart]').forEach(btn => {
      btn.addEventListener('click', (e) => {
        e.preventDefault();
        const parent = btn.closest('[data-product-id]');
        if (parent) {
          const item = {
            id: parent.dataset.productId,
            name: parent.dataset.productName || parent.querySelector('[data-product-name]')?.textContent || 'Unknown',
            price: parseFloat(parent.dataset.productPrice) || 0
          };
          addToCart(item);
        }
      });
    });
    // Fallback: buttons with text 'Add to cart'
    document.querySelectorAll('button').forEach(btn => {
      if (/add to cart/i.test(btn.textContent)) {
        btn.addEventListener('click', (e) => {
          e.preventDefault();
          const parent = btn.closest('[data-product-id]');
          if (parent) {
            const item = {
              id: parent.dataset.productId,
              name: parent.dataset.productName || parent.querySelector('[data-product-name]')?.textContent || 'Unknown',
              price: parseFloat(parent.dataset.productPrice) || 0
            };
            addToCart(item);
          }
        });
      }
    });
  }
})();
