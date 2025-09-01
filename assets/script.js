// script.js

// -------------------- WATCH DATA --------------------
const watchData = {
  "audemars-piguet-royal-oak-gold": {
    id: "audemars-piguet-royal-oak-gold",
    name: "Royal Oak Gold",
    brand: "Audemars Piguet",
    price: 45000,
    image: "./assets/watch-1-L_BZsghZ.jpg",
    description: "The Royal Oak Gold represents the pinnacle of luxury watchmaking. Crafted with 18k yellow gold case and bracelet, this timepiece features the iconic octagonal bezel and 'Tapisserie' dial pattern that has defined Audemars Piguet since 1972.",
    specifications: {
      "Case Material": "18k Yellow Gold",
      "Case Size": "41mm",
      "Movement": "Calibre 3120 Automatic",
      "Water Resistance": "50 meters",
      "Power Reserve": "60 hours",
      "Crystal": "Sapphire"
    },
    stock: "In Stock"
  },
  "rolex-submariner": {
    id: "rolex-submariner",
    name: "Submariner",
    brand: "Rolex",
    price: 12500,
    image: "./assets/watch-1-L_BZsghZ.jpg",
    description: "The Rolex Submariner is a legendary dive watch that has become an icon of luxury and precision. With its robust construction and timeless design, it's equally at home beneath the waves or in the boardroom.",
    specifications: {
      "Case Material": "904L Stainless Steel",
      "Case Size": "40mm",
      "Movement": "Calibre 3230 Automatic",
      "Water Resistance": "300 meters",
      "Power Reserve": "70 hours",
      "Crystal": "Sapphire"
    },
    stock: "In Stock"
  },
  "omega-speedmaster": {
    id: "omega-speedmaster",
    name: "Speedmaster",
    brand: "Omega",
    price: 8900,
    image: "./assets/watch-1-L_BZsghZ.jpg",
    description: "The Omega Speedmaster Professional is the legendary 'Moonwatch' that accompanied astronauts to the lunar surface. This manually-wound chronograph represents precision, heritage, and adventure.",
    specifications: {
      "Case Material": "Stainless Steel",
      "Case Size": "42mm",
      "Movement": "Calibre 1863 Manual",
      "Water Resistance": "50 meters",
      "Power Reserve": "48 hours",
      "Crystal": "Hesalite"
    },
    stock: "In Stock"
  },
  "patek-philippe-nautilus": {
    id: "patek-philippe-nautilus",
    name: "Nautilus",
    brand: "Patek Philippe",
    price: 75000,
    image: "./assets/watch-1-L_BZsghZ.jpg",
    description: "The Patek Philippe Nautilus represents the ultimate expression of luxury sports watchmaking. With its distinctive porthole-inspired design and impeccable finishing, it's one of the most coveted watches in the world.",
    specifications: {
      "Case Material": "Stainless Steel",
      "Case Size": "40mm", 
      "Movement": "Calibre 26-330 S C Automatic",
      "Water Resistance": "120 meters",
      "Power Reserve": "45 hours",
      "Crystal": "Sapphire"
    },
    stock: "In Stock"
  },
  "rolex-daytona": {
    id: "rolex-daytona",
    name: "Daytona",
    brand: "Rolex",
    price: 35000,
    image: "./assets/watch-1-L_BZsghZ.jpg",
    description: "The Rolex Daytona is the ultimate racing chronograph, designed for professional drivers and racing enthusiasts. Its precision and reliability have made it a legend on and off the track.",
    specifications: {
      "Case Material": "904L Stainless Steel",
      "Case Size": "40mm",
      "Movement": "Calibre 4130 Automatic",
      "Water Resistance": "100 meters",
      "Power Reserve": "72 hours",
      "Crystal": "Sapphire"
    },
    stock: "In Stock"
  },
  "omega-seamaster": {
    id: "omega-seamaster",
    name: "Seamaster",
    brand: "Omega",
    price: 6500,
    image: "./assets/watch-1-L_BZsghZ.jpg",
    description: "The Omega Seamaster Planet Ocean is a professional dive watch that combines cutting-edge technology with striking design. Built to withstand the depths of the ocean while maintaining elegance.",
    specifications: {
      "Case Material": "Stainless Steel",
      "Case Size": "43.5mm",
      "Movement": "Calibre 8900 Automatic",
      "Water Resistance": "600 meters",
      "Power Reserve": "60 hours",
      "Crystal": "Sapphire"
    },
    stock: "In Stock"
  }
};

// -------------------- NAVIGATION --------------------
const navButtons = document.querySelectorAll(".fixed.bottom-0.left-0.right-0.z-50.bg-luxury-white.border-t.border-luxury-gray.shadow-luxury .grid.grid-cols-4.h-16 button");

const setActiveNav = () => {
  const currentPath = window.location.pathname;

  navButtons.forEach(button => {
    const link = button.querySelector("a");
    if (link) {
      const href = new URL(link.href).pathname;
      if (href === currentPath) {
        const span = link.querySelector("span");
        if (span) {
          span.classList.add("text-luxury-gold");
          span.classList.remove("text-luxury-gray-dark"); // Remove conflicting class
        }
        link.classList.add("bg-luxury-gold/5");
      } else {
        const span = link.querySelector("span");
        if (span) {
          span.classList.remove("text-luxury-gold");
          span.classList.add("text-luxury-gray-dark"); // Re-add original color if not active
        }
        link.classList.remove("bg-luxury-gold/5");
      }
    }
  });
};

setActiveNav(); // Set active class on page load

navButtons.forEach(button => {
  button.addEventListener("click", e => {
    const link = button.querySelector("a");
    if (link) {
      e.preventDefault(); // Prevent default navigation initially
      const href = link.getAttribute("href");
      
      // Remove active class from all links first
      navButtons.forEach(btn => {
        const btnLink = btn.querySelector("a");
        if (btnLink) {
          const btnSpan = btnLink.querySelector("span");
          if (btnSpan) {
            btnSpan.classList.remove("text-luxury-gold");
            btnSpan.classList.add("text-luxury-gray-dark");
          }
          btnLink.classList.remove("bg-luxury-gold/5");
        }
      });

      // Add active class to the clicked link
      const currentSpan = link.querySelector("span");
      if (currentSpan) {
        currentSpan.classList.add("text-luxury-gold");
        currentSpan.classList.remove("text-luxury-gray-dark");
      }
      link.classList.add("bg-luxury-gold/5");

      if (href) {
        window.location.href = href; // Navigate to correct page
      }
    }
  });
});

// -------------------- MOBILE MENU TOGGLE --------------------
const menuBtn = document.querySelector(".menu-toggle");
const navMenu = document.querySelector("nav ul");

if (menuBtn && navMenu) {
  menuBtn.addEventListener("click", () => {
    navMenu.classList.toggle("open"); // toggle menu open/close
  });
}

// -------------------- ORDER MANAGEMENT --------------------
let orders = []; // Orders array

// Order Manager Object
const OrderManager = {
  // Create a new order from current cart
  createOrder: function(cartItems) {
    const order = {
      id: `ORD-${String(orders.length + 1).padStart(3, '0')}`,
      items: cartItems.map(item => ({
        id: item.id,
        name: item.name,
        brand: item.brand,
        price: item.price,
        qty: item.qty,
        image: item.image
      })),
      total: cartItems.reduce((sum, item) => sum + (item.price * item.qty), 0),
      orderDate: new Date().toISOString(),
      status: 'Order Confirmed',
      expectedDelivery: this.calculateExpectedDelivery(),
      trackingNumber: this.generateTrackingNumber(),
      statusHistory: [
        {
          status: 'Order Confirmed',
          date: new Date().toISOString(),
          description: 'Your order has been confirmed and is being prepared'
        }
      ]
    };
    
    orders.unshift(order); // Add to beginning of array (newest first)
    this.saveOrders();
    this.updateOrdersUI();
    
    // Schedule status updates
    this.scheduleStatusUpdates(order.id);
    
    return order;
  },

  // Schedule realistic status updates for the order
  scheduleStatusUpdates: function(orderId) {
    // Update to "Processing" after 2 minutes (for demo - normally would be hours)
    setTimeout(() => {
      this.updateOrderStatus(orderId, 'Processing', 'Your order is being processed and prepared for shipment');
    }, 2 * 60 * 1000);

    // Update to "In Transit" after 5 minutes (for demo)
    setTimeout(() => {
      this.updateOrderStatus(orderId, 'In Transit', 'Your order has been shipped and is on its way');
    }, 5 * 60 * 1000);

    // Update to "Delivered" after 10 minutes (for demo)
    setTimeout(() => {
      const deliveredDate = new Date().toISOString();
      this.updateOrderStatus(orderId, 'Delivered', 'Your order has been delivered successfully', deliveredDate);
    }, 10 * 60 * 1000);
  },

  // Calculate expected delivery date (7-14 days from now)
  calculateExpectedDelivery: function() {
    const today = new Date();
    const deliveryDays = Math.floor(Math.random() * 8) + 7; // 7-14 days
    const deliveryDate = new Date(today.getTime() + (deliveryDays * 24 * 60 * 60 * 1000));
    return deliveryDate.toISOString();
  },

  // Generate a random tracking number
  generateTrackingNumber: function() {
    return 'TLX' + Math.random().toString(36).substr(2, 9).toUpperCase();
  },

  // Get all orders
  getOrders: function() {
    return orders;
  },

  // Get recent orders (last 3)
  getRecentOrders: function() {
    return orders.slice(0, 3);
  },

  // Update order status
  updateOrderStatus: function(orderId, status, description = null, deliveredDate = null) {
    const order = orders.find(order => order.id === orderId);
    if (order) {
      order.status = status;
      if (deliveredDate) {
        order.deliveredDate = deliveredDate;
      }
      
      // Add to status history
      if (!order.statusHistory) {
        order.statusHistory = [];
      }
      
      order.statusHistory.push({
        status: status,
        date: new Date().toISOString(),
        description: description || `Order status updated to ${status}`
      });
      
      this.saveOrders();
      this.updateOrdersUI();
      
      // Show notification if user is on orders or confirmation page
      if (window.location.pathname.includes('orders.html') || window.location.pathname.includes('order-confirmation.html')) {
        this.showStatusNotification(orderId, status);
      }
    }
  },

  // Show status update notification
  showStatusNotification: function(orderId, status) {
    // Create a simple notification
    const notification = document.createElement('div');
    notification.className = 'fixed top-4 right-4 bg-luxury-gold text-luxury-black px-4 py-2 rounded shadow-lg z-50 transition-all duration-300';
    notification.innerHTML = `Order ${orderId} status updated to: ${status}`;
    
    document.body.appendChild(notification);
    
    // Remove notification after 3 seconds
    setTimeout(() => {
      notification.style.opacity = '0';
      setTimeout(() => {
        document.body.removeChild(notification);
      }, 300);
    }, 3000);
  },

  // Save orders to localStorage
  saveOrders: function() {
    try {
      localStorage.setItem("orders", JSON.stringify(orders));
    } catch (error) {
      console.error("Error saving orders:", error);
    }
  },

  // Load orders from localStorage
  loadOrders: function() {
    try {
      const savedOrders = localStorage.getItem("orders");
      if (savedOrders) {
        orders = JSON.parse(savedOrders);
        this.updateOrdersUI();
      } else {
        // Create sample orders if none exist
        this.createSampleOrders();
      }
    } catch (error) {
      console.error("Error loading orders:", error);
      orders = [];
      // Create sample orders on error too
      this.createSampleOrders();
    }
  },

  // Clear all orders (for testing)
  clearAllOrders: function() {
    orders = [];
    localStorage.removeItem('orders');
    this.updateOrdersUI();
    console.log('All orders cleared');
  },

  // Create sample orders for demonstration
  createSampleOrders: function() {
    const sampleOrders = [
      {
        id: 'ORD-001',
        items: [{
          id: 'audemars-piguet-royal-oak-gold',
          name: 'Royal Oak Gold',
          brand: 'Audemars Piguet',
          price: 45000,
          qty: 1,
          image: watchData['audemars-piguet-royal-oak-gold'].image
        }],
        total: 45000,
        orderDate: new Date(Date.now() - 15 * 24 * 60 * 60 * 1000).toISOString(), // 15 days ago
        status: 'Delivered',
        expectedDelivery: new Date(Date.now() - 10 * 24 * 60 * 60 * 1000).toISOString(),
        deliveredDate: new Date(Date.now() - 10 * 24 * 60 * 60 * 1000).toISOString(),
        trackingNumber: 'TLX123456789',
        statusHistory: [
          {
            status: 'Order Confirmed',
            date: new Date(Date.now() - 15 * 24 * 60 * 60 * 1000).toISOString(),
            description: 'Your order has been confirmed and is being prepared'
          },
          {
            status: 'Processing',
            date: new Date(Date.now() - 14 * 24 * 60 * 60 * 1000).toISOString(),
            description: 'Your order is being processed and prepared for shipment'
          },
          {
            status: 'In Transit',
            date: new Date(Date.now() - 12 * 24 * 60 * 60 * 1000).toISOString(),
            description: 'Your order has been shipped and is on its way'
          },
          {
            status: 'Delivered',
            date: new Date(Date.now() - 10 * 24 * 60 * 60 * 1000).toISOString(),
            description: 'Your order has been delivered successfully'
          }
        ]
      },
      {
        id: 'ORD-002',
        items: [{
          id: 'rolex-submariner',
          name: 'Submariner',
          brand: 'Rolex',
          price: 12500,
          qty: 1,
          image: watchData['rolex-submariner'].image
        }],
        total: 12500,
        orderDate: new Date(Date.now() - 5 * 24 * 60 * 60 * 1000).toISOString(), // 5 days ago
        status: 'In Transit',
        expectedDelivery: new Date(Date.now() + 3 * 24 * 60 * 60 * 1000).toISOString(),
        trackingNumber: 'TLX987654321',
        statusHistory: [
          {
            status: 'Order Confirmed',
            date: new Date(Date.now() - 5 * 24 * 60 * 60 * 1000).toISOString(),
            description: 'Your order has been confirmed and is being prepared'
          },
          {
            status: 'Processing',
            date: new Date(Date.now() - 4 * 24 * 60 * 60 * 1000).toISOString(),
            description: 'Your order is being processed and prepared for shipment'
          },
          {
            status: 'In Transit',
            date: new Date(Date.now() - 2 * 24 * 60 * 60 * 1000).toISOString(),
            description: 'Your order has been shipped and is on its way'
          }
        ]
      },
      {
        id: 'ORD-003',
        items: [{
          id: 'omega-seamaster',
          name: 'Seamaster',
          brand: 'Omega',
          price: 6500,
          qty: 1,
          image: watchData['omega-seamaster'].image
        }],
        total: 6500,
        orderDate: new Date(Date.now() - 2 * 24 * 60 * 60 * 1000).toISOString(), // 2 days ago
        status: 'Processing',
        expectedDelivery: new Date(Date.now() + 7 * 24 * 60 * 60 * 1000).toISOString(),
        trackingNumber: 'TLX567890123',
        statusHistory: [
          {
            status: 'Order Confirmed',
            date: new Date(Date.now() - 2 * 24 * 60 * 60 * 1000).toISOString(),
            description: 'Your order has been confirmed and is being prepared'
          },
          {
            status: 'Processing',
            date: new Date(Date.now() - 1 * 24 * 60 * 60 * 1000).toISOString(),
            description: 'Your order is being processed and prepared for shipment'
          }
        ]
      }
    ];
    
    orders = sampleOrders;
    this.saveOrders();
    this.updateOrdersUI();
  },

  // Update orders UI
  updateOrdersUI: function() {
    this.updateOrdersPage();
    this.updateAccountOrdersPreview();
    this.updateAccountOrdersCount();
    this.updateOrderConfirmationPage();
  },

  // Update order confirmation page
  updateOrderConfirmationPage: function() {
    if (!window.location.pathname.includes('order-confirmation.html')) return;
    
    // Get the most recent order (should be the one just placed)
    const recentOrder = orders[0];
    if (!recentOrder) return;
    
    this.populateOrderConfirmation(recentOrder);
    this.populateStatusTimeline(recentOrder);
  },

  // Populate order confirmation details
  populateOrderConfirmation: function(order) {
    const detailsContainer = document.getElementById('order-confirmation-details');
    if (!detailsContainer) return;
    
    const orderDate = new Date(order.orderDate);
    const expectedDate = new Date(order.expectedDelivery);
    
    detailsContainer.innerHTML = `
      <div class="flex justify-between items-center mb-4">
        <span class="font-semibold text-luxury-black">Order ID:</span>
        <span class="text-luxury-gold font-semibold">${order.id}</span>
      </div>
      <div class="flex justify-between items-center mb-4">
        <span class="font-semibold text-luxury-black">Order Date:</span>
        <span>${orderDate.toLocaleDateString('en-US', { weekday: 'long', year: 'numeric', month: 'long', day: 'numeric' })}</span>
      </div>
      <div class="flex justify-between items-center mb-4">
        <span class="font-semibold text-luxury-black">Expected Delivery:</span>
        <span>${expectedDate.toLocaleDateString('en-US', { weekday: 'long', year: 'numeric', month: 'long', day: 'numeric' })}</span>
      </div>
      <div class="flex justify-between items-center mb-4">
        <span class="font-semibold text-luxury-black">Tracking Number:</span>
        <span class="font-mono text-sm">${order.trackingNumber}</span>
      </div>
      <div class="border-t border-luxury-gray pt-4">
        <h3 class="font-semibold text-luxury-black mb-3">Order Items:</h3>
        <div class="space-y-3">
          ${order.items.map(item => `
            <div class="flex items-center gap-4">
              <img src="${item.image}" alt="${item.name}" class="w-12 h-12 object-cover rounded">
              <div class="flex-1">
                <p class="font-semibold text-luxury-black">${item.name}</p>
                <p class="text-sm text-luxury-gray-dark">${item.brand} • Qty: ${item.qty}</p>
              </div>
              <p class="font-semibold text-luxury-black">$${(item.price * item.qty).toLocaleString()}</p>
            </div>
          `).join('')}
        </div>
        <div class="border-t border-luxury-gray mt-4 pt-4 flex justify-between items-center">
          <span class="text-xl font-bold text-luxury-black">Total:</span>
          <span class="text-xl font-bold text-luxury-gold">$${order.total.toLocaleString()}</span>
        </div>
      </div>
    `;
  },

  // Populate status timeline
  populateStatusTimeline: function(order) {
    const timelineContainer = document.getElementById('order-status-timeline');
    if (!timelineContainer) return;
    
    const statusHistory = order.statusHistory || [
      {
        status: order.status,
        date: order.orderDate,
        description: 'Your order has been confirmed'
      }
    ];
    
    const allStatuses = [
      { key: 'Order Confirmed', label: 'Order Confirmed', icon: '✓' },
      { key: 'Processing', label: 'Processing', icon: '⚙️' },
      { key: 'In Transit', label: 'In Transit', icon: '🚚' },
      { key: 'Delivered', label: 'Delivered', icon: '📦' }
    ];
    
    timelineContainer.innerHTML = allStatuses.map((statusItem, index) => {
      const historyItem = statusHistory.find(h => h.status === statusItem.key);
      const isCompleted = historyItem !== undefined;
      const isCurrent = order.status === statusItem.key;
      
      return `
        <div class="flex items-center gap-4">
          <div class="flex items-center justify-center w-10 h-10 rounded-full ${
            isCompleted 
              ? 'bg-green-100 text-green-600' 
              : isCurrent 
                ? 'bg-luxury-gold text-luxury-black' 
                : 'bg-luxury-gray text-luxury-gray-dark'
          }">
            ${isCompleted ? '✓' : statusItem.icon}
          </div>
          <div class="flex-1">
            <div class="flex justify-between items-center">
              <h3 class="font-semibold ${isCompleted || isCurrent ? 'text-luxury-black' : 'text-luxury-gray-dark'}">${statusItem.label}</h3>
              ${historyItem ? `<span class="text-sm text-luxury-gray-dark">${new Date(historyItem.date).toLocaleDateString()}</span>` : ''}
            </div>
            ${historyItem ? `<p class="text-sm text-luxury-gray-dark mt-1">${historyItem.description}</p>` : ''}
          </div>
        </div>
      `;
    }).join('');
  },

  // Update orders page content
  updateOrdersPage: function() {
    const ordersContainer = document.getElementById('orders-container');
    
    if (!ordersContainer || !window.location.pathname.includes('orders.html')) return;
    
    // Clear existing orders
    ordersContainer.innerHTML = '';
    
    if (orders.length === 0) {
      ordersContainer.innerHTML = `
        <div class="text-center py-12">
          <div class="text-luxury-gray-dark mb-4">
            <svg class="mx-auto h-16 w-16 mb-4" fill="none" stroke="currentColor" viewBox="0 0 24 24">
              <path stroke-linecap="round" stroke-linejoin="round" stroke-width="1" d="M16 11V7a4 4 0 00-8 0v4M5 9h14l1 12H4L5 9z"></path>
            </svg>
            <h3 class="text-lg font-semibold text-luxury-gray-dark mb-2">No orders yet</h3>
            <p class="text-luxury-gray-dark mb-6">Start shopping to see your orders here</p>
            <button class="bg-luxury-gold hover:bg-luxury-gold-dark text-luxury-black font-semibold py-2 px-6 rounded transition-colors duration-200" onclick="window.location.href='./catalog.html'">
              Browse Collection
            </button>
          </div>
        </div>
      `;
      return;
    }
    
    // Render orders
    orders.forEach(order => {
      const orderElement = this.createOrderElement(order);
      ordersContainer.appendChild(orderElement);
    });
  },

  // Create order HTML element
  createOrderElement: function(order) {
    const orderDate = new Date(order.orderDate);
    const expectedDate = new Date(order.expectedDelivery);
    const deliveredDate = order.deliveredDate ? new Date(order.deliveredDate) : null;
    
    const statusConfig = this.getStatusConfig(order.status);
    
    const orderDiv = document.createElement('div');
    orderDiv.className = 'rounded-lg border bg-card text-card-foreground shadow-sm p-4 space-y-4';
    
    orderDiv.innerHTML = `
      <div class="flex justify-between items-start">
        <div>
          <div class="flex items-center gap-2 mb-1">
            ${statusConfig.icon}
            <span class="font-semibold text-luxury-black">${order.id}</span>
            <div class="inline-flex items-center rounded-full border px-2.5 py-0.5 text-xs font-semibold transition-colors ${statusConfig.badgeClass}">
              ${order.status}
            </div>
          </div>
          <p class="text-sm text-luxury-gray-dark">Ordered on ${orderDate.toLocaleDateString('en-US', { year: 'numeric', month: 'short', day: 'numeric' })}</p>
          <p class="text-sm text-luxury-gray-dark">
            ${deliveredDate 
              ? `Delivered on ${deliveredDate.toLocaleDateString('en-US', { month: 'short', day: 'numeric', year: 'numeric' })}` 
              : `Expected ${expectedDate.toLocaleDateString('en-US', { month: 'short', day: 'numeric', year: 'numeric' })}`
            }
          </p>
        </div>
        <p class="text-lg font-bold text-luxury-black">$${order.total.toLocaleString()}</p>
      </div>
      <div class="space-y-3">
        ${order.items.map(item => `
          <div class="flex items-center gap-4 p-3 bg-luxury-gray/10 rounded-lg">
            <img alt="${item.name}" class="w-16 h-16 object-cover rounded-lg" src="${item.image}">
            <div class="flex-1">
              <p class="text-sm text-luxury-gold font-medium">${item.brand}</p>
              <h4 class="font-semibold text-luxury-black">${item.name}</h4>
              <p class="text-sm text-luxury-gray-dark">Qty: ${item.qty}</p>
            </div>
            <p class="font-bold text-luxury-black">$${(item.price * item.qty).toLocaleString()}</p>
          </div>
        `).join('')}
      </div>
      <div class="flex gap-2 pt-2">
        <button class="inline-flex items-center justify-center gap-2 whitespace-nowrap text-sm font-medium ring-offset-background transition-colors focus-visible:outline-none focus-visible:ring-2 focus-visible:ring-ring focus-visible:ring-offset-2 disabled:pointer-events-none disabled:opacity-50 border bg-background h-9 rounded-md px-3 border-luxury-gold text-luxury-gold hover:bg-luxury-gold hover:text-luxury-black" onclick="alert('Tracking: ${order.trackingNumber}')">
          Track Order
        </button>
        ${order.status === 'Delivered' ? `
          <button class="inline-flex items-center justify-center gap-2 whitespace-nowrap text-sm font-medium ring-offset-background transition-colors border bg-background hover:text-accent-foreground h-9 rounded-md px-3 border-luxury-gray text-luxury-gray-dark hover:bg-luxury-gray" onclick="OrderManager.reorderItems('${order.id}')">
            Reorder
          </button>
        ` : ''}
      </div>
    `;
    
    return orderDiv;
  },

  // Get status configuration
  getStatusConfig: function(status) {
    const configs = {
      'Order Confirmed': {
        icon: '<svg class="lucide lucide-check-circle w-5 h-5 text-green-600" fill="none" height="24" stroke="currentColor" stroke-linecap="round" stroke-linejoin="round" stroke-width="2" viewBox="0 0 24 24" width="24"><path d="M22 11.08V12a10 10 0 1 1-5.93-9.14"></path><polyline points="22,4 12,14.01 9,11.01"></polyline></svg>',
        badgeClass: 'bg-green-100 text-green-800 hover:bg-green-100'
      },
      'Processing': {
        icon: '<svg class="lucide lucide-clock w-5 h-5 text-luxury-gray-dark" fill="none" height="24" stroke="currentColor" stroke-linecap="round" stroke-linejoin="round" stroke-width="2" viewBox="0 0 24 24" width="24"><circle cx="12" cy="12" r="10"></circle><polyline points="12 6 12 12 16 14"></polyline></svg>',
        badgeClass: 'bg-secondary text-secondary-foreground hover:bg-secondary/80'
      },
      'In Transit': {
        icon: '<svg class="lucide lucide-truck w-5 h-5 text-luxury-gold" fill="none" height="24" stroke="currentColor" stroke-linecap="round" stroke-linejoin="round" stroke-width="2" viewBox="0 0 24 24" width="24"><path d="M14 18V6a2 2 0 0 0-2-2H4a2 2 0 0 0-2 2v11a1 1 0 0 0 1 1h2"></path><path d="M15 18H9"></path><path d="M19 18h2a1 1 0 0 0 1-1v-3.65a1 1 0 0 0-.22-.624l-3.48-4.35A1 1 0 0 0 17.52 8H14"></path><circle cx="17" cy="18" r="2"></circle><circle cx="7" cy="18" r="2"></circle></svg>',
        badgeClass: 'bg-luxury-gold/10 text-luxury-gold hover:bg-luxury-gold/10'
      },
      'Delivered': {
        icon: '<svg class="lucide lucide-circle-check-big w-5 h-5 text-green-600" fill="none" height="24" stroke="currentColor" stroke-linecap="round" stroke-linejoin="round" stroke-width="2" viewBox="0 0 24 24" width="24"><path d="M21.801 10A10 10 0 1 1 17 3.335"></path><path d="m9 11 3 3L22 4"></path></svg>',
        badgeClass: 'bg-green-100 text-green-800 hover:bg-green-100'
      }
    };
    return configs[status] || configs['Processing'];
  },

  // Update account page orders preview
  updateAccountOrdersPreview: function() {
    const recentOrdersContainer = document.querySelector('#account-recent-orders');
    
    if (!recentOrdersContainer) return;
    
    const recentOrders = this.getRecentOrders();
    
    if (recentOrders.length === 0) {
      recentOrdersContainer.innerHTML = `
        <div class="text-center py-8">
          <p class="text-luxury-gray-dark mb-4">No recent orders</p>
          <button class="bg-luxury-gold hover:bg-luxury-gold-dark text-luxury-black font-semibold py-2 px-4 rounded transition-colors duration-200" onclick="window.location.href='./catalog.html'">
            Start Shopping
          </button>
        </div>
      `;
      return;
    }
    
    recentOrdersContainer.innerHTML = recentOrders.map(order => {
      const orderDate = new Date(order.orderDate);
      const statusConfig = this.getStatusConfig(order.status);
      
      return `
        <div class="rounded-lg border bg-card text-card-foreground shadow-sm p-4 cursor-pointer hover:shadow-card transition-all duration-300" onclick="window.location.href='./orders.html'">
          <div class="flex justify-between items-start mb-3">
            <div>
              <div class="flex items-center gap-2 mb-1">
                <span class="font-semibold text-luxury-black">${order.id}</span>
                <div class="inline-flex items-center rounded-full border px-2.5 py-0.5 text-xs font-semibold transition-colors ${statusConfig.badgeClass}">
                  ${order.status}
                </div>
              </div>
              <p class="text-sm text-luxury-gray-dark">${orderDate.toLocaleDateString('en-US', { month: 'short', day: 'numeric' })}</p>
            </div>
            <p class="font-bold text-luxury-black">$${order.total.toLocaleString()}</p>
          </div>
          <p class="text-sm text-luxury-gray-dark">${order.items.length} item${order.items.length > 1 ? 's' : ''}</p>
        </div>
      `;
    }).join('');
  },

  // Update account orders count
  updateAccountOrdersCount: function() {
    const ordersCountElement = document.querySelector('.orders-count');
    if (ordersCountElement) {
      ordersCountElement.textContent = orders.length;
    }
    
    // Update total spent
    const totalSpentElement = document.querySelector('.total-spent');
    if (totalSpentElement) {
      const totalSpent = orders.reduce((sum, order) => sum + order.total, 0);
      totalSpentElement.textContent = `$${totalSpent.toLocaleString()}`;
    }
  },

  // Reorder items from a previous order
  reorderItems: function(orderId) {
    const order = orders.find(o => o.id === orderId);
    if (!order) return;
    
    // Add all items from the order to cart
    order.items.forEach(item => {
      CartManager.addToCart({
        id: item.id,
        name: item.name,
        price: item.price,
        qty: item.qty,
        image: item.image,
        brand: item.brand
      });
    });
    
    alert(`${order.items.length} item(s) added to cart!`);
    
    // Redirect to cart
    window.location.href = './cart.html';
  }
};

// -------------------- CART LOGIC --------------------
let favorites = []; // Favorites array

// Favorites Manager Object
const FavoritesManager = {
  // Add item to favorites
  addToFavorites: function(watchData) {
    const existingItem = favorites.find(item => item.id === watchData.id);
    if (existingItem) {
      console.log("Item already in favorites");
      return false;
    }
    
    favorites.push({
      id: watchData.id,
      name: watchData.name,
      price: parseFloat(watchData.price) || 0,
      image: watchData.image,
      brand: watchData.brand,
      addedAt: new Date().toISOString()
    });
    
    this.saveFavorites();
    this.updateFavoritesUI();
    return true;
  },

  // Remove item from favorites
  removeFromFavorites: function(watchId) {
    const initialLength = favorites.length;
    favorites = favorites.filter(item => item.id !== watchId);
    
    if (favorites.length < initialLength) {
      this.saveFavorites();
      this.updateFavoritesUI();
      return true;
    }
    return false;
  },

  // Toggle favorite status
  toggleFavorite: function(watchData) {
    const isInFavorites = favorites.some(item => item.id === watchData.id);
    if (isInFavorites) {
      return this.removeFromFavorites(watchData.id);
    } else {
      return this.addToFavorites(watchData);
    }
  },

  // Check if item is in favorites
  isInFavorites: function(watchId) {
    return favorites.some(item => item.id === watchId);
  },

  // Get all favorites
  getFavorites: function() {
    return [...favorites];
  },

  // Get favorites count
  getFavoritesCount: function() {
    return favorites.length;
  },

  // Clear all favorites
  clearFavorites: function() {
    favorites = [];
    this.saveFavorites();
    this.updateFavoritesUI();
  },

  // Save favorites to localStorage
  saveFavorites: function() {
    try {
      localStorage.setItem("favorites", JSON.stringify(favorites));
    } catch (error) {
      console.error("Error saving favorites:", error);
    }
  },

  // Load favorites from localStorage
  loadFavorites: function() {
    try {
      const savedFavorites = localStorage.getItem("favorites");
      if (savedFavorites) {
        favorites = JSON.parse(savedFavorites);
        this.updateFavoritesUI();
      }
    } catch (error) {
      console.error("Error loading favorites:", error);
      favorites = [];
    }
  },

  // Update favorites UI
  updateFavoritesUI: function() {
    this.updateFavoriteButtons();
    this.updateFavoritesPage();
    this.updateAccountFavoritesPreview();
  },

  // Update favorite buttons across all pages
  updateFavoriteButtons: function() {
    const favoriteButtons = document.querySelectorAll('.favorite-button');
    favoriteButtons.forEach(button => {
      const watchId = button.dataset.id;
      const heartIcon = button.querySelector('svg');
      
      if (this.isInFavorites(watchId)) {
        // Item is favorited - fill the heart and change color
        heartIcon.setAttribute('fill', 'currentColor');
        button.classList.add('text-luxury-gold');
        button.classList.remove('text-luxury-gray-dark');
      } else {
        // Item is not favorited - outline only
        heartIcon.setAttribute('fill', 'none');
        button.classList.remove('text-luxury-gold');
        button.classList.add('text-luxury-gray-dark');
      }
    });
  },

  // Update favorites page content
  updateFavoritesPage: function() {
    const favoritesContainer = document.getElementById('favorites-container');
    const emptyState = document.getElementById('empty-favorites-state');
    
    if (!favoritesContainer) return; // Not on favorites page
    
    if (favorites.length === 0) {
      // Show empty state
      favoritesContainer.style.display = 'none';
      if (emptyState) emptyState.style.display = 'block';
    } else {
      // Show favorites
      if (emptyState) emptyState.style.display = 'none';
      favoritesContainer.style.display = 'block';
      
      // Render favorites
      favoritesContainer.innerHTML = favorites.map(item => `
        <div class="bg-luxury-white rounded-lg shadow-md overflow-hidden">
          <div class="relative">
            <img src="${item.image}" alt="${item.name}" class="w-full h-48 object-cover">
            <button class="absolute top-3 right-3 p-2 rounded-full transition-colors duration-200 bg-luxury-white/90 text-luxury-gold favorite-button" 
                    data-id="${item.id}" data-name="${item.name}" data-price="${item.price}" data-image="${item.image}" data-brand="${item.brand}">
              <svg class="lucide lucide-heart" fill="currentColor" height="16" stroke="currentColor" stroke-linecap="round" stroke-linejoin="round" stroke-width="2" viewBox="0 0 24 24" width="16" xmlns="http://www.w3.org/2000/svg">
                <path d="M19 14c1.49-1.46 3-3.21 3-5.5A5.5 5.5 0 0 0 16.5 3c-1.76 0-3 .5-4.5 2-1.5-1.5-2.74-2-4.5-2A5.5 5.5 0 0 0 2 8.5c0 2.3 1.5 4.05 3 5.5l7 7Z"></path>
              </svg>
            </button>
          </div>
          <div class="p-4">
            <div class="flex justify-between items-start mb-2">
              <h3 class="text-lg font-semibold text-luxury-black">${item.name}</h3>
              <p class="text-sm text-luxury-gray-dark">${item.brand}</p>
            </div>
            <p class="text-xl font-bold text-luxury-gold mb-3">$${item.price.toLocaleString()}</p>
            <div class="flex gap-2">
              <button class="flex-1 bg-luxury-gold hover:bg-luxury-gold-dark text-luxury-black font-semibold py-2 px-4 rounded transition-colors duration-200 add-to-cart-btn"
                      data-id="${item.id}" data-name="${item.name}" data-price="${item.price}" data-image="${item.image}" data-brand="${item.brand}">
                Add to Cart
              </button>
              <button class="px-4 py-2 border border-luxury-gray rounded hover:bg-luxury-gray/10 transition-colors duration-200 view-details-btn"
                      onclick="window.location.href='./watch.html?id=${item.id}'">
                View Details
              </button>
            </div>
          </div>
        </div>
      `).join('');
      
      // Re-attach event listeners for new buttons
      this.attachFavoriteListeners();
      CartManager.attachCartListeners();
    }
  },

  // Update account page favorites preview
  updateAccountFavoritesPreview: function() {
    const accountFavoritesContainer = document.getElementById('account-favorites-preview');
    
    if (!accountFavoritesContainer) return; // Not on account page
    
    if (favorites.length === 0) {
      // Show empty state
      accountFavoritesContainer.innerHTML = `
        <div class="text-center py-8">
          <svg class="lucide lucide-heart mx-auto text-luxury-gray mb-2" fill="none" height="32" stroke="currentColor" stroke-linecap="round" stroke-linejoin="round" stroke-width="2" viewBox="0 0 24 24" width="32" xmlns="http://www.w3.org/2000/svg">
            <path d="M19 14c1.49-1.46 3-3.21 3-5.5A5.5 5.5 0 0 0 16.5 3c-1.76 0-3 .5-4.5 2-1.5-1.5-2.74-2-4.5-2A5.5 5.5 0 0 0 2 8.5c0 2.3 1.5 4.05 3 5.5l7 7Z"></path>
          </svg>
          <p class="text-sm text-luxury-gray-dark">No favorites yet</p>
        </div>
      `;
    } else {
      // Show preview of first 3 favorites
      const previewFavorites = favorites.slice(0, 3);
      
      accountFavoritesContainer.innerHTML = previewFavorites.map(item => `
        <div class="rounded-lg border bg-card text-card-foreground shadow-sm p-4 cursor-pointer hover:shadow-card transition-all duration-300" onclick="window.location.href='./watch.html?id=${item.id}'">
          <div class="flex items-center gap-4">
            <img alt="${item.name}" class="w-12 h-12 object-cover rounded-lg" src="${item.image}">
            <div class="flex-1">
              <div class="flex justify-between items-start mb-1">
                <p class="font-semibold text-luxury-black">${item.name}</p>
                <button class="p-1 rounded-full transition-colors duration-200 text-luxury-gold hover:text-luxury-gold-dark favorite-button" 
                        data-id="${item.id}" data-name="${item.name}" data-price="${item.price}" data-image="${item.image}" data-brand="${item.brand}">
                  <svg class="lucide lucide-heart" fill="currentColor" height="14" stroke="currentColor" stroke-linecap="round" stroke-linejoin="round" stroke-width="2" viewBox="0 0 24 24" width="14" xmlns="http://www.w3.org/2000/svg">
                    <path d="M19 14c1.49-1.46 3-3.21 3-5.5A5.5 5.5 0 0 0 16.5 3c-1.76 0-3 .5-4.5 2-1.5-1.5-2.74-2-4.5-2A5.5 5.5 0 0 0 2 8.5c0 2.3 1.5 4.05 3 5.5l7 7Z"></path>
                  </svg>
                </button>
              </div>
              <p class="text-sm text-luxury-gray-dark mb-1">${item.brand}</p>
              <div class="flex justify-between items-center">
                <p class="font-bold text-luxury-black">$${item.price.toLocaleString()}</p>
              </div>
            </div>
          </div>
        </div>
      `).join('');
      
      // Re-attach event listeners for new buttons
      this.attachFavoriteListeners();
    }
  }
};

// Update favorites UI function (keeping for compatibility)
function updateFavoritesUI() {
  FavoritesManager.updateFavoritesUI();
}

// CartManager for encapsulated cart logic
const CartManager = {
  cart: [],

  loadCart() {
    const savedCart = localStorage.getItem("cart");
    if (savedCart) {
      try {
        const parsedCart = JSON.parse(savedCart);
        // Validate and clean cart data
        this.cart = parsedCart.filter(item => {
          return item && 
                 item.id && 
                 item.name && 
                 !isNaN(item.price) && 
                 item.price > 0 &&
                 !isNaN(item.qty) && 
                 item.qty > 0;
        }).map(item => ({
          id: item.id,
          name: item.name,
          price: Number(item.price),
          qty: Number(item.qty),
          image: item.image || './assets/hero-watch-D40AmJ87.jpg'
        }));
        
        // Save cleaned cart back to localStorage
        if (this.cart.length !== parsedCart.length) {
          this.saveCart();
        }
      } catch (e) {
        console.error("Error loading cart from localStorage:", e);
        this.cart = [];
        this.saveCart();
      }
    }
    this.updateCartUI();
  },

  saveCart() {
    localStorage.setItem("cart", JSON.stringify(this.cart));
  },

  addToCart(product) {
    // Validate product fields
    const id = product.id || `unknown-${Date.now()}`;
    const name = product.name || "Unknown Product";
    const price = isNaN(product.price) ? 0 : Number(product.price);
    const qty = isNaN(product.qty) || product.qty < 1 ? 1 : Number(product.qty);
    const image = product.image || './assets/hero-watch-D40AmJ87.jpg';

    const existing = this.cart.find(item => item.id === id);
    if (existing) {
      existing.qty += qty;
    } else {
      this.cart.push({ id, name, price, qty, image });
    }
    this.saveCart();
    this.updateCartUI();
  },

  removeFromCart(productId) {
    this.cart = this.cart.filter(item => item.id !== productId);
    this.saveCart();
    this.updateCartUI();
  },

  updateQuantity(productId, newQuantity) {
    const item = this.cart.find(item => item.id === productId);
    if (item) {
      item.qty = newQuantity;
      if (item.qty <= 0) {
        this.removeFromCart(productId);
      } else {
        this.saveCart();
        this.updateCartUI();
      }
    }
  },

  getCartTotal() {
    return this.cart.reduce((total, item) => {
      const price = isNaN(item.price) ? 0 : Number(item.price);
      const qty = isNaN(item.qty) ? 0 : Number(item.qty);
      return total + price * qty;
    }, 0);
  },

  getCartItemCount() {
    return this.cart.reduce((count, item) => {
      const qty = isNaN(item.qty) ? 0 : Number(item.qty);
      return count + qty;
    }, 0);
  },

  getCartItems() {
    return this.cart;
  },

  clearCart() {
    this.cart = [];
    this.saveCart();
    this.updateCartUI();
  },

  updateCartUI() {
    console.log("Updating Cart UI. Current cart:", this.cart); // Debugging
    const cartContainer = document.querySelector(".cart-items");
    const totalEl = document.querySelector(".cart-total");
    const cartItemCountEls = document.querySelectorAll(".cart-item-count"); // For global cart count
    const orderSummaryItems = document.querySelector(".order-summary-items"); // For checkout page
    const orderSummaryTotal = document.querySelector(".order-summary-total"); // For checkout page

    if (cartContainer) {
      cartContainer.innerHTML = "";
      if (this.cart.length === 0 && window.location.pathname.includes("cart.html")) {
        cartContainer.innerHTML = `
          <div class="text-center py-12">
            <svg class="lucide lucide-shopping-bag mx-auto text-luxury-gray mb-4" fill="none" height="64" stroke="currentColor" stroke-linecap="round" stroke-linejoin="round" stroke-width="2" viewBox="0 0 24 24" width="64" xmlns="http://www.w3.org/2000/svg">
              <path d="M6 2 3 6v14a2 2 0 0 0 2 2h14a2 2 0 0 0 2-2V6l-3-4Z"></path>
              <path d="M3 6h18"></path>
              <path d="M16 10a4 4 0 0 1-8 0"></path>
            </svg>
            <h2 class="text-xl font-semibold text-luxury-gray-dark mb-2">Your cart is empty</h2>
            <p class="text-luxury-gray-dark mb-6">Add some exquisite watches to your cart to begin your journey.</p>
            <a href="./catalog.html" class="inline-flex items-center justify-center gap-2 whitespace-nowrap rounded-md text-sm ring-offset-background transition-colors focus-visible:outline-none focus-visible:ring-2 focus-visible:ring-ring focus-visible:ring-offset-2 disabled:pointer-events-none disabled:opacity-50 [&_svg]:pointer-events-none [&_svg]:size-4 [&_svg]:shrink-0 h-10 px-4 py-2 bg-luxury-gold hover:bg-luxury-gold-dark text-luxury-black font-semibold">Browse Collection</a>
          </div>
        `;
      } else {
        this.cart.forEach(item => {
          const row = document.createElement("div");
          row.classList.add("cart-item", "flex", "items-center", "justify-between", "py-2", "border-b", "border-luxury-gray-light");
          
          // Ensure all values are valid
          const itemName = item.name || "Unknown Product";
          const itemPrice = isNaN(item.price) ? 0 : Number(item.price);
          const itemQty = isNaN(item.qty) ? 1 : Number(item.qty);
          const itemImage = item.image || './assets/hero-watch-D40AmJ87.jpg';
          const itemId = item.id || `unknown-${Date.now()}`;
          const totalPrice = itemPrice * itemQty;
          
          row.innerHTML = `
            <div class="flex items-center gap-4">
              <img src="${itemImage}" alt="${itemName}" class="w-16 h-16 object-cover rounded-md">
              <div>
                <span class="font-medium text-luxury-black">${itemName}</span>
                <div class="flex items-center mt-1">
                  <button class="update-qty" data-id="${itemId}" data-change="-1">
                    <svg xmlns="http://www.w3.org/2000/svg" width="20" height="20" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round" class="lucide lucide-minus text-luxury-gray-dark hover:text-luxury-gold">
                      <path d="M5 12h14"></path>
                    </svg>
                  </button>
                  <span class="w-8 text-center text-luxury-black">${itemQty}</span>
                  <button class="update-qty" data-id="${itemId}" data-change="1">
                    <svg xmlns="http://www.w3.org/2000/svg" width="20" height="20" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round" class="lucide lucide-plus text-luxury-gray-dark hover:text-luxury-gold">
                      <path d="M12 5v14"></path>
                      <path d="M5 12h14"></path>
                    </svg>
                  </button>
                </div>
              </div>
            </div>
            <div class="flex items-center gap-4">
              <span class="font-semibold text-luxury-black">$${totalPrice.toFixed(2)}</span>
              <button class="remove-from-cart text-luxury-gray-dark hover:text-red-500" data-id="${itemId}">
                <svg xmlns="http://www.w3.org/2000/svg" width="20" height="20" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round" class="lucide lucide-x-circle">
                  <circle cx="12" cy="12" r="10"></circle>
                  <path d="m15 9-6 6"></path>
                  <path d="m9 9 6 6"></path>
                </svg>
              </button>
            </div>
          `;
          cartContainer.appendChild(row);
        });

        // Add event listeners for remove and quantity buttons
        cartContainer.querySelectorAll(".remove-from-cart").forEach(btn => {
          btn.addEventListener("click", () => {
            CartManager.removeFromCart(btn.dataset.id);
          });
        });

        cartContainer.querySelectorAll(".update-qty").forEach(btn => {
          btn.addEventListener("click", () => {
            const id = btn.dataset.id;
            const change = parseInt(btn.dataset.change);
            const item = CartManager.cart.find(cartItem => cartItem.id === id);
            if (item) {
              CartManager.updateQuantity(id, item.qty + change);
            }
          });
        });
      }
    }

    if (totalEl) {
      const total = this.getCartTotal();
      totalEl.textContent = `$${isNaN(total) ? '0.00' : total.toFixed(2)}`;
    }

    const count = this.getCartItemCount();
    cartItemCountEls.forEach(el => {
      el.textContent = isNaN(count) ? '0' : count;
      el.style.display = count > 0 ? 'flex' : 'none';
    });

    // Update order summary on checkout page
    if (orderSummaryItems && orderSummaryTotal) {
      orderSummaryItems.innerHTML = "";
      this.cart.forEach(item => {
        const itemEl = document.createElement("div");
        itemEl.classList.add("flex", "justify-between", "text-luxury-black");
        
        // Ensure all values are valid
        const itemName = item.name || "Unknown Product";
        const itemPrice = isNaN(item.price) ? 0 : Number(item.price);
        const itemQty = isNaN(item.qty) ? 1 : Number(item.qty);
        const totalPrice = itemPrice * itemQty;
        
        itemEl.innerHTML = `
          <span>${itemName} x ${itemQty}</span>
          <span>$${totalPrice.toFixed(2)}</span>
        `;
        orderSummaryItems.appendChild(itemEl);
      });
      const total = this.getCartTotal();
      orderSummaryTotal.textContent = `$${isNaN(total) ? '0.00' : total.toFixed(2)}`;
    }

    // Ensure elements are visible on cart.html if cart has items
    const cartContainerDiv = document.querySelector(".cart-container");
    if (cartContainerDiv && window.location.pathname.includes("cart.html")) {
      if (this.cart.length > 0) {
        cartContainerDiv.querySelector(".cart-items-display").style.display = "block";
        cartContainerDiv.querySelector(".cart-summary").style.display = "block";
      } else {
        cartContainerDiv.querySelector(".cart-items-display").style.display = "none";
        cartContainerDiv.querySelector(".cart-summary").style.display = "none";
      }
    }

    // Initial display for empty cart on cart.html
    const emptyCartMessage = document.querySelector(".cart-items > .text-center");
    if (window.location.pathname.includes("cart.html")) {
      if (this.cart.length === 0) {
        if (!emptyCartMessage) {
          cartContainer.innerHTML = `
            <div class="text-center py-12">
              <svg class="lucide lucide-shopping-bag mx-auto text-luxury-gray mb-4" fill="none" height="64" stroke="currentColor" stroke-linecap="round" stroke-linejoin="round" stroke-width="2" viewBox="0 0 24 24" width="64" xmlns="http://www.w3.org/2000/svg">
                <path d="M6 2 3 6v14a2 2 0 0 0 2 2h14a2 2 0 0 0 2-2V6l-3-4Z"></path>
                <path d="M3 6h18"></path>
                <path d="M16 10a4 4 0 0 1-8 0"></path>
              </svg>
              <h2 class="text-xl font-semibold text-luxury-gray-dark mb-2">Your cart is empty</h2>
              <p class="text-luxury-gray-dark mb-6">Add some exquisite watches to your cart to begin your journey.</p>
              <a href="./catalog.html" class="inline-flex items-center justify-center gap-2 whitespace-nowrap rounded-md text-sm ring-offset-background transition-colors focus-visible:outline-none focus-visible:ring-2 focus-visible:ring-ring focus-visible:ring-offset-2 disabled:pointer-events-none disabled:opacity-50 [&_svg]:pointer-events-none [&_svg]:size-4 [&_svg]:shrink-0 h-10 px-4 py-2 bg-luxury-gold hover:bg-luxury-gold-dark text-luxury-black font-semibold">Browse Collection</a>
            </div>
          `;
        }
        if (cartContainerDiv) {
          cartContainerDiv.querySelector(".cart-items-display").style.display = "none";
          cartContainerDiv.querySelector(".cart-summary").style.display = "none";
        }
      } else {
        if (cartContainerDiv) {
          cartContainerDiv.querySelector(".cart-items-display").style.display = "block";
          cartContainerDiv.querySelector(".cart-summary").style.display = "block";
        }
      }
    }
  },

  attachCartListeners() {
    // Attach event listeners to all "Add to Cart" buttons
    const addToCartButtons = document.querySelectorAll('.add-to-cart-btn');
    
    addToCartButtons.forEach(button => {
      // Remove any existing event listeners to prevent duplicates
      button.removeEventListener('click', this.handleAddToCart);
      
      // Add new event listener
      button.addEventListener('click', this.handleAddToCart.bind(this));
    });
    
    console.log(`Attached cart listeners to ${addToCartButtons.length} buttons`);
  },

  handleAddToCart(event) {
    event.preventDefault();
    const button = event.currentTarget;
    
    // Get product data from button attributes
    const product = {
      id: button.dataset.id,
      name: button.dataset.name,
      price: parseFloat(button.dataset.price),
      image: button.dataset.image,
      brand: button.dataset.brand,
      qty: 1
    };
    
    // Validate required data
    if (!product.id || !product.name || isNaN(product.price)) {
      console.error('Invalid product data:', product);
      return;
    }
    
    // Add to cart
    this.addToCart(product);
    
    // Show success feedback
    const originalText = button.textContent;
    button.textContent = 'Added!';
    button.disabled = true;
    
    setTimeout(() => {
      button.textContent = originalText;
      button.disabled = false;
    }, 1000);
    
    console.log('Added to cart:', product);
  }
};

// Load cart and favorites from local storage on page load
document.addEventListener("DOMContentLoaded", () => {
  console.log("DOM Content Loaded. Initializing scripts.");
  
  // Clear any corrupted cart data first
  const savedCart = localStorage.getItem("cart");
  if (savedCart) {
    try {
      const parsedCart = JSON.parse(savedCart);
      const hasCorruptedData = parsedCart.some(item => 
        !item || !item.id || !item.name || isNaN(item.price) || isNaN(item.qty) ||
        item.name === "undefined" || item.name === "null" || 
        item.price === null || item.qty === null
      );
      if (hasCorruptedData) {
        console.log("Found corrupted cart data, clearing...");
        localStorage.removeItem("cart");
      }
    } catch (e) {
      console.log("Cart data is corrupted, clearing...");
      localStorage.removeItem("cart");
    }
  }
  
  CartManager.loadCart(); // Load cart using CartManager

  // Load favorites using FavoritesManager
  FavoritesManager.loadFavorites();

  // Attach cart listeners after a short delay to ensure DOM is ready
  setTimeout(() => {
    CartManager.attachCartListeners();
  }, 100);
});

// Add to cart buttons (for catalog.html and other pages)
document.addEventListener("DOMContentLoaded", () => {
  document.querySelectorAll(".add-to-cart").forEach(btn => {
    // Skip the watch detail page add-to-cart button as it has its own handler
    if (btn.classList.contains('product-detail-add-to-cart')) {
      return;
    }
    
    btn.addEventListener("click", (e) => {
      e.preventDefault();
      console.log("Add to Cart button clicked!"); // Debugging
      
      // Get data from button attributes first
      let productId = btn.dataset.id || btn.getAttribute('data-id');
      let productName = btn.dataset.name || btn.getAttribute('data-name');
      let productPrice = parseFloat(btn.dataset.price || btn.getAttribute('data-price'));
      let productImage = btn.dataset.image || btn.getAttribute('data-image');
      let productBrand = btn.dataset.brand || btn.getAttribute('data-brand');
      let quantity = 1;

      // If data attributes are missing, try to extract from DOM
      if (!productId || !productName || isNaN(productPrice)) {
        const productElement = btn.closest("div.rounded-lg.border.bg-card.text-card-foreground.shadow-sm.group.cursor-pointer.overflow-hidden.transition-all.duration-300.hover\\:shadow-card.hover\\:-translate-y-1");
        
        if (productElement) {
          const nameEl = productElement.querySelector("h3.font-semibold.text-luxury-black.mb-2");
          const priceEl = productElement.querySelector("p.text-xl.font-bold.text-luxury-black");
          const brandEl = productElement.querySelector("span.text-sm.text-luxury-gold.font-medium");
          const imageEl = productElement.querySelector("img");

          productName = productName || (nameEl ? nameEl.textContent.trim() : "Unknown Product");
          productPrice = isNaN(productPrice) ? (priceEl ? parseFloat(priceEl.textContent.replace(/[^0-9.]/g, '')) : 0) : productPrice;
          productBrand = productBrand || (brandEl ? brandEl.textContent.trim() : "Unknown Brand");
          productImage = productImage || (imageEl ? imageEl.src : './assets/hero-watch-D40AmJ87.jpg');
          productId = productId || `${productBrand.replace(/\s/g, '-').toLowerCase()}-${productName.replace(/\s/g, '-').toLowerCase()}`;
        }
      }

      // Set default image if still missing
      if (!productImage) {
        productImage = './assets/hero-watch-D40AmJ87.jpg';
      }

      // Create full product name with brand if available
      const fullProductName = productBrand && productBrand !== "Unknown Brand" ? 
        `${productBrand} ${productName}` : productName;

      console.log("Final product data:", {
        id: productId,
        name: fullProductName,
        price: productPrice,
        qty: quantity,
        image: productImage
      });

      // Validate data before adding to cart
      if (!productId || !productName || isNaN(productPrice) || productPrice <= 0) {
        console.error("Invalid product data:", { productId, productName, productPrice, quantity, productImage });
        alert("Error: Invalid product data. Cannot add to cart.");
        return;
      }

      CartManager.addToCart({ 
        id: productId, 
        name: fullProductName, 
        price: productPrice, 
        qty: quantity, 
        image: productImage 
      });
    });
  });
});

// Event listener for clearing the cart on cart.html
document.addEventListener("DOMContentLoaded", () => {
  const clearCartButton = document.querySelector(".clear-cart-button");
  if (clearCartButton) {
    clearCartButton.addEventListener("click", () => {
      CartManager.clearCart();
    });
  }

  setupPlaceOrderButton();
});

function setupPlaceOrderButton() {
  const placeOrderButton = document.querySelector(".place-order-button");
  console.log("setupPlaceOrderButton called, button found:", !!placeOrderButton);
  
  if (placeOrderButton && !placeOrderButton.hasAttribute('data-order-listener-attached')) {
    console.log("Place order button found and event listener attached");
    
    // Mark that we've attached the listener
    placeOrderButton.setAttribute('data-order-listener-attached', 'true');
    
    placeOrderButton.addEventListener("click", function(e) {
      e.preventDefault();
      e.stopPropagation();
      console.log("Place order button clicked");
      
      // Prevent multiple clicks
      if (this.disabled) {
        console.log("Button already disabled, ignoring click");
        return;
      }
      
      const cartItems = CartManager.getCartItems();
      console.log("Cart items:", cartItems);
      if (cartItems.length === 0) {
        alert("Your cart is empty! Go to catalog to add items first.");
        return;
      }
      
      // Add loading state to button
      this.disabled = true;
      this.innerHTML = `
        <svg class="animate-spin -ml-1 mr-3 h-5 w-5" xmlns="http://www.w3.org/2000/svg" fill="none" viewBox="0 0 24 24">
          <circle class="opacity-25" cx="12" cy="12" r="10" stroke="currentColor" stroke-width="4"></circle>
          <path class="opacity-75" fill="currentColor" d="M4 12a8 8 0 018-8V0C5.373 0 0 5.373 0 12h4zm2 5.291A7.962 7.962 0 014 12H0c0 3.042 1.135 5.824 3 7.938l3-2.647z"></path>
        </svg>
        Processing Order...
      `;
      
      // Simulate processing delay
      setTimeout(() => {
        try {
          // Create order before clearing cart
          const order = OrderManager.createOrder(cartItems);
          console.log("Order created:", order);
          
          // Clear cart
          CartManager.clearCart();
          
          // Store order ID for confirmation page
          sessionStorage.setItem('lastOrderId', order.id);
          
          // Redirect to confirmation page
          window.location.href = "./order-confirmation.html";
        } catch (error) {
          console.error("Error creating order:", error);
          alert("There was an error processing your order. Please try again.");
          
          // Reset button state
          this.disabled = false;
          this.innerHTML = "Place Order";
        }
      }, 2000); // 2 second delay for realistic processing feel
    });
  } else if (placeOrderButton && placeOrderButton.hasAttribute('data-order-listener-attached')) {
    console.log("Place order button already has listener attached, skipping");
  } else {
    console.log("Place order button NOT found!");
  }
}

// Initial UI update for cart and favorites when DOM is ready
document.addEventListener("DOMContentLoaded", () => {
  console.log("DOM Content Loaded - script.js is running");
  CartManager.loadCart();
  FavoritesManager.loadFavorites();
  OrderManager.loadOrders();
  
  // Add debug function for testing checkout
  window.addTestItemToCart = function() {
    const testItem = {
      id: 'rolex-submariner',
      name: 'Submariner',
      brand: 'Rolex',
      price: 12500,
      qty: 1,
      image: './assets/hero-watch-D40AmJ87.jpg'
    };
    CartManager.addToCart(testItem);
    console.log("Test item added to cart");
  };
  
  // Test if we're on checkout page
  if (window.location.pathname.includes('checkout.html')) {
    console.log("On checkout page - looking for place order button");
    setTimeout(() => {
      const btn = document.querySelector(".place-order-button");
      console.log("Place order button found:", btn);
      if (btn) {
        console.log("Button classes:", btn.className);
        console.log("Button text:", btn.textContent);
      }
    }, 1000);
  }
});

// -------------------- TOGGLE PANELS --------------------
document.querySelectorAll("[data-toggle]").forEach(btn => {
  btn.addEventListener("click", () => {
    const targetId = btn.dataset.toggle;
    const target = document.getElementById(targetId);
    if (target) {
      target.classList.toggle("open");
    }
  });
});

// -------------------- FAVORITES FUNCTIONALITY --------------------

// Attach favorite button listeners
FavoritesManager.attachFavoriteListeners = function() {
  const favoriteButtons = document.querySelectorAll('.favorite-button');
  favoriteButtons.forEach(button => {
    // Remove existing listeners to prevent duplicates
    button.removeEventListener('click', handleFavoriteClick);
    button.addEventListener('click', handleFavoriteClick);
  });
};

// Handle favorite button click
function handleFavoriteClick(e) {
  e.preventDefault();
  e.stopPropagation();
  
  const button = e.currentTarget;
  const watchData = {
    id: button.dataset.id,
    name: button.dataset.name,
    price: button.dataset.price,
    image: button.dataset.image,
    brand: button.dataset.brand
  };
  
  if (!watchData.id) {
    console.error("Watch data is incomplete:", watchData);
    return;
  }
  
  const wasToggled = FavoritesManager.toggleFavorite(watchData);
  
  if (wasToggled) {
    const isNowFavorited = FavoritesManager.isInFavorites(watchData.id);
    console.log(isNowFavorited ? "Added to favorites:" : "Removed from favorites:", watchData.name);
  }
}

// Initialize favorites when DOM is ready
document.addEventListener("DOMContentLoaded", () => {
  // Load watch details if on watch page
  loadWatchDetails();
  
  // Initialize catalog filters if on catalog page
  initializeCatalogFilters();
  
  // Force catalog filter initialization if elements exist (fallback)
  setTimeout(() => {
    const searchInput = document.getElementById('search-input');
    const brandFilter = document.getElementById('brand-filter');
    const priceFilter = document.getElementById('price-filter');
    
    if (searchInput && brandFilter && priceFilter && typeof initializeCatalogFilters === 'function') {
      console.log('Force initializing catalog filters...');
      
      // Override path check temporarily
      const originalPathname = window.location.pathname;
      Object.defineProperty(window.location, 'pathname', {
        configurable: true,
        value: '/catalog.html'
      });
      
      initializeCatalogFilters();
      
      // Restore original pathname
      Object.defineProperty(window.location, 'pathname', {
        configurable: true,
        value: originalPathname
      });
    }
  }, 200);
  
  // Initialize quantity controls if on watch page
  initializeQuantityControls();
  
  // Initialize customization controls if on watch page
  initializeCustomizationControls();
  
  // Attach favorite listeners after a brief delay to ensure all elements are loaded
  setTimeout(() => {
    FavoritesManager.attachFavoriteListeners();
  }, 100);
  
  // Add clear favorites functionality for settings page
  const clearFavoritesBtn = document.getElementById('clear-favorites-btn');
  if (clearFavoritesBtn) {
    clearFavoritesBtn.addEventListener('click', () => {
      if (confirm('Are you sure you want to clear all favorites? This action cannot be undone.')) {
        FavoritesManager.clearFavorites();
        alert('All favorites have been cleared.');
      }
    });
  }
});

// -------------------- WATCH DETAILS PAGE --------------------

// Initialize quantity controls
function initializeQuantityControls() {
  if (!window.location.pathname.endsWith('watch.html')) return;
  
  const minusBtn = document.getElementById('quantity-minus');
  const plusBtn = document.getElementById('quantity-plus');
  const quantityDisplay = document.getElementById('quantity-display');
  
  if (!minusBtn || !plusBtn || !quantityDisplay) return;
  
  let currentQuantity = 1;
  
  // Minus button
  minusBtn.addEventListener('click', () => {
    if (currentQuantity > 1) {
      currentQuantity--;
      quantityDisplay.textContent = currentQuantity;
      updateAddToCartPrice();
    }
  });
  
  // Plus button
  plusBtn.addEventListener('click', () => {
    if (currentQuantity < 99) { // Limit to 99
      currentQuantity++;
      quantityDisplay.textContent = currentQuantity;
      updateAddToCartPrice();
    }
  });
  
  // Update Add to Cart button price
  function updateAddToCartPrice() {
    // Check if customization is initialized and use the customization price update instead
    const addToCartTextElement = document.getElementById('add-to-cart-text');
    if (addToCartTextElement) {
      // Call the customization price update function if it exists
      const customizationControlsExist = document.getElementById('gold-carat');
      if (customizationControlsExist) {
        // Trigger customization price update which will handle quantity
        const event = new Event('change');
        document.getElementById('gold-carat').dispatchEvent(event);
        return;
      }
    }
    
    // Fallback for non-customizable products
    const addToCartBtn = document.querySelector('.add-to-cart.product-detail-add-to-cart');
    if (addToCartBtn) {
      const price = parseInt(addToCartBtn.getAttribute('data-price'));
      const totalPrice = price * currentQuantity;
      addToCartBtn.innerHTML = `
        <svg xmlns="http://www.w3.org/2000/svg" width="20" height="20" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round" class="lucide lucide-shopping-cart">
          <circle cx="8" cy="21" r="1"></circle>
          <circle cx="19" cy="21" r="1"></circle>
          <path d="M2.05 2.05h2l2.66 12.42a2 2 0 0 0 2 1.58h9.78a2 2 0 0 0 1.95-1.57L20.99 7H5.12"></path>
        </svg>
        Add to Cart - $${totalPrice.toLocaleString()}
      `;
    }
  }
  
  // Add cart functionality to the Add to Cart button
  const addToCartBtn = document.querySelector('.add-to-cart.product-detail-add-to-cart');
  if (addToCartBtn && !addToCartBtn.hasAttribute('data-listener-attached')) {
    addToCartBtn.setAttribute('data-listener-attached', 'true');
    addToCartBtn.addEventListener('click', () => {
      const productId = addToCartBtn.getAttribute('data-id');
      const productName = addToCartBtn.getAttribute('data-name');
      const productPrice = parseInt(addToCartBtn.getAttribute('data-price'));
      const productImage = addToCartBtn.getAttribute('data-image');
      const productBrand = addToCartBtn.getAttribute('data-brand');
      
      if (productId && productName && productPrice) {
        CartManager.addToCart({
          id: productId,
          name: productName,
          price: productPrice,
          qty: currentQuantity, // Use the current quantity from our controls
          image: productImage,
          brand: productBrand
        });
        
        console.log(`Added ${currentQuantity} x ${productName} to cart`);
      }
    });
  }
}

// Initialize customization controls
function initializeCustomizationControls() {
  if (!window.location.pathname.endsWith('watch.html')) return;
  
  const goldCaratSelect = document.getElementById('gold-carat');
  const diamondTypeSelect = document.getElementById('diamond-type');
  const diamondCaratSelect = document.getElementById('diamond-carat');
  const diamondCaratSection = document.getElementById('diamond-carat-section');
  const customizationPriceElement = document.getElementById('customization-price');
  const totalPriceElement = document.getElementById('total-price');
  const addToCartTextElement = document.getElementById('add-to-cart-text');
  
  if (!goldCaratSelect || !diamondTypeSelect || !diamondCaratSelect || !diamondCaratSection) return;
  
  const basePrice = 45000; // Base price of the watch
  
  // Pricing for customizations
  const goldCaratPrices = {
    '14k': 0,
    '18k': 2500,
    '22k': 5000,
    '24k': 7500
  };
  
  const diamondTypePrices = {
    'none': 0,
    'artificial': 1500,
    'real': 8000
  };
  
  const diamondCaratPrices = {
    '0.25': 0,
    '0.50': 3000,
    '0.75': 6000,
    '1.0': 12000,
    '1.5': 20000,
    '2.0': 35000
  };
  
  // Calculate total customization price
  function calculateCustomizationPrice() {
    const goldCarat = goldCaratSelect.value;
    const diamondType = diamondTypeSelect.value;
    const diamondCarat = diamondCaratSelect.value;
    
    let customizationPrice = 0;
    customizationPrice += goldCaratPrices[goldCarat] || 0;
    customizationPrice += diamondTypePrices[diamondType] || 0;
    
    // Only add diamond carat price if real diamonds are selected
    if (diamondType === 'real') {
      customizationPrice += diamondCaratPrices[diamondCarat] || 0;
    }
    
    return customizationPrice;
  }
  
  // Update price display
  function updatePriceDisplay() {
    const customizationPrice = calculateCustomizationPrice();
    const totalPrice = basePrice + customizationPrice;
    const quantityElement = document.getElementById('quantity-display');
    const quantity = quantityElement ? parseInt(quantityElement.textContent || '1') : 1;
    const finalTotal = totalPrice * quantity;
    
    // Update customization price display
    if (customizationPriceElement) {
      customizationPriceElement.textContent = `+$${customizationPrice.toLocaleString()}`;
    }
    
    // Update total price display
    if (totalPriceElement) {
      totalPriceElement.textContent = `$${totalPrice.toLocaleString()}`;
    }
    
    // Update add to cart button text
    if (addToCartTextElement) {
      addToCartTextElement.textContent = `Add to Cart - $${finalTotal.toLocaleString()}`;
    }
    
    // Update the data-price attribute for cart functionality
    const addToCartBtn = document.querySelector('.add-to-cart.product-detail-add-to-cart');
    if (addToCartBtn) {
      addToCartBtn.setAttribute('data-price', totalPrice.toString());
    }
  }
  
  // Show/hide diamond carat section based on diamond type
  function toggleDiamondCaratSection() {
    const diamondType = diamondTypeSelect.value;
    if (diamondCaratSection) {
      if (diamondType === 'real') {
        diamondCaratSection.style.display = 'block';
      } else {
        diamondCaratSection.style.display = 'none';
      }
    }
  }
  
  // Event listeners
  goldCaratSelect.addEventListener('change', updatePriceDisplay);
  diamondTypeSelect.addEventListener('change', () => {
    toggleDiamondCaratSection();
    updatePriceDisplay();
  });
  diamondCaratSelect.addEventListener('change', updatePriceDisplay);
  
  // Listen for quantity changes
  const quantityDisplay = document.getElementById('quantity-display');
  if (quantityDisplay) {
    const observer = new MutationObserver(updatePriceDisplay);
    observer.observe(quantityDisplay, { childList: true, characterData: true, subtree: true });
  }
  
  // Initialize display
  toggleDiamondCaratSection();
  updatePriceDisplay();
}

// Load watch details based on URL parameter
function loadWatchDetails() {
  // Check if we're on the watch page
  if (!window.location.pathname.endsWith('watch.html')) return;
  
  // Get watch ID from URL parameter
  const urlParams = new URLSearchParams(window.location.search);
  const watchId = urlParams.get('id');
  
  if (!watchId || !watchData[watchId]) {
    // Default to first watch if no ID or invalid ID
    const defaultWatchId = "audemars-piguet-royal-oak-gold";
    const watch = watchData[defaultWatchId];
    updateWatchPageContent(watch);
    return;
  }
  
  const watch = watchData[watchId];
  updateWatchPageContent(watch);
}

// -------------------- CATALOG FILTERS --------------------

// Initialize catalog filters
function initializeCatalogFilters() {
  // More flexible path checking for different environments
  const pathname = window.location.pathname;
  const href = window.location.href;
  const isCatalogPage = pathname.endsWith('catalog.html') || 
                       pathname.includes('catalog.html') || 
                       href.includes('catalog.html') ||
                       pathname === '/catalog.html' ||
                       pathname === '/';
  
  if (!isCatalogPage) return;
  
  console.log('Initializing catalog filters...');
  
  const searchInput = document.getElementById('search-input');
  const brandFilter = document.getElementById('brand-filter');
  const priceFilter = document.getElementById('price-filter');
  const brandDropdown = document.getElementById('brand-dropdown');
  const priceDropdown = document.getElementById('price-dropdown');
  
  console.log('Filter elements:', {
    searchInput: !!searchInput,
    brandFilter: !!brandFilter,
    priceFilter: !!priceFilter,
    brandDropdown: !!brandDropdown,
    priceDropdown: !!priceDropdown
  });
  
  if (!searchInput || !brandFilter || !priceFilter) {
    console.error('Missing filter elements, aborting initialization');
    return;
  }
  
  let currentFilters = {
    search: '',
    brand: 'all',
    price: 'all'
  };
  
  // Search functionality
  if (searchInput) {
    searchInput.addEventListener('input', (e) => {
      currentFilters.search = e.target.value.toLowerCase();
      filterWatches(currentFilters);
    });
  }
  
  // Brand filter dropdown
  if (brandFilter && brandDropdown) {
    console.log('Adding brand filter event listeners');
    const brandChevron = brandFilter.querySelector('.lucide-chevron-down');
    
    brandFilter.addEventListener('click', (e) => {
      console.log('Brand filter clicked!');
      e.preventDefault();
      e.stopPropagation();
      
      const isHidden = brandDropdown.classList.contains('hidden');
      
      // Close other dropdown
      priceDropdown?.classList.add('hidden');
      const priceChevron = priceFilter?.querySelector('.lucide-chevron-down');
      if (priceChevron) {
        priceChevron.style.transform = 'rotate(0deg)';
      }
      
      // Toggle current dropdown
      brandDropdown.classList.toggle('hidden');
      
      // Animate chevron
      if (brandChevron) {
        brandChevron.style.transform = isHidden ? 'rotate(180deg)' : 'rotate(0deg)';
      }
    });
    
    const brandOptions = brandDropdown.querySelectorAll('.brand-option');
    console.log('Found brand options:', brandOptions.length);
    brandOptions.forEach(option => {
      option.addEventListener('click', (e) => {
        console.log('Brand option clicked:', option.dataset.brand);
        e.preventDefault();
        e.stopPropagation();
        currentFilters.brand = option.dataset.brand;
        
        // Update button text using the new ID
        const brandText = document.getElementById('brand-filter-text');
        if (brandText) {
          brandText.textContent = option.textContent;
        }
        
        brandDropdown.classList.add('hidden');
        
        // Reset chevron
        const brandChevron = brandFilter.querySelector('.lucide-chevron-down');
        if (brandChevron) {
          brandChevron.style.transform = 'rotate(0deg)';
        }
        
        filterWatches(currentFilters);
      });
    });
  }

  // Price filter dropdown
  if (priceFilter && priceDropdown) {
    console.log('Adding price filter event listeners');
    const priceChevron = priceFilter.querySelector('.lucide-chevron-down');
    
    priceFilter.addEventListener('click', (e) => {
      console.log('Price filter clicked!');
      e.preventDefault();
      e.stopPropagation();
      
      const isHidden = priceDropdown.classList.contains('hidden');
      
      // Close other dropdown
      brandDropdown?.classList.add('hidden');
      const brandChevron = brandFilter?.querySelector('.lucide-chevron-down');
      if (brandChevron) {
        brandChevron.style.transform = 'rotate(0deg)';
      }
      
      // Toggle current dropdown
      priceDropdown.classList.toggle('hidden');
      
      // Animate chevron
      if (priceChevron) {
        priceChevron.style.transform = isHidden ? 'rotate(180deg)' : 'rotate(0deg)';
      }
    });
    
    const priceOptions = priceDropdown.querySelectorAll('.price-option');
    console.log('Found price options:', priceOptions.length);
    priceOptions.forEach(option => {
      option.addEventListener('click', (e) => {
        console.log('Price option clicked:', option.dataset.price);
        e.preventDefault();
        e.stopPropagation();
        currentFilters.price = option.dataset.price;
        
        // Update button text using the new ID
        const priceText = document.getElementById('price-filter-text');
        if (priceText) {
          priceText.textContent = option.textContent;
        }
        
        priceDropdown.classList.add('hidden');
        
        // Reset chevron
        const priceChevron = priceFilter.querySelector('.lucide-chevron-down');
        if (priceChevron) {
          priceChevron.style.transform = 'rotate(0deg)';
        }
        
        filterWatches(currentFilters);
      });
    });
  }

  // Close dropdowns when clicking outside
  document.addEventListener('click', (e) => {
    if (!brandFilter?.contains(e.target)) {
      brandDropdown?.classList.add('hidden');
      const brandChevron = brandFilter?.querySelector('.lucide-chevron-down');
      if (brandChevron) {
        brandChevron.style.transform = 'rotate(0deg)';
      }
    }
    if (!priceFilter?.contains(e.target)) {
      priceDropdown?.classList.add('hidden');
      const priceChevron = priceFilter?.querySelector('.lucide-chevron-down');
      if (priceChevron) {
        priceChevron.style.transform = 'rotate(0deg)';
      }
    }
  });  // Initial render
  console.log('Rendering initial watch grid with', Object.values(watchData).length, 'watches');
  renderWatchGrid(Object.values(watchData));
  console.log('Catalog filters initialization complete');
}

// Filter watches based on current filters
function filterWatches(filters) {
  let filteredWatches = Object.values(watchData);
  
  // Search filter
  if (filters.search) {
    filteredWatches = filteredWatches.filter(watch => 
      watch.name.toLowerCase().includes(filters.search) ||
      watch.brand.toLowerCase().includes(filters.search) ||
      watch.description.toLowerCase().includes(filters.search)
    );
  }
  
  // Brand filter
  if (filters.brand !== 'all') {
    filteredWatches = filteredWatches.filter(watch => 
      watch.brand === filters.brand
    );
  }
  
  // Price filter
  if (filters.price !== 'all') {
    filteredWatches = filteredWatches.filter(watch => {
      const price = watch.price;
      switch (filters.price) {
        case '0-10000':
          return price < 10000;
        case '10000-25000':
          return price >= 10000 && price <= 25000;
        case '25000-50000':
          return price >= 25000 && price <= 50000;
        case '50000+':
          return price > 50000;
        default:
          return true;
      }
    });
  }
  
  renderWatchGrid(filteredWatches);
}

// Render watch grid
function renderWatchGrid(watches) {
  const grid = document.getElementById('watches-grid');
  const resultsCount = document.getElementById('results-count');
  
  if (!grid) return;
  
  // Update results count
  if (resultsCount) {
    resultsCount.textContent = `${watches.length} watch${watches.length !== 1 ? 'es' : ''} found`;
  }
  
  // Render watches
  grid.innerHTML = watches.map(watch => `
    <div class="rounded-lg border bg-card text-card-foreground shadow-sm group cursor-pointer overflow-hidden transition-all duration-300 hover:shadow-card hover:-translate-y-1" data-id="${watch.id}">
      <a href="./watch.html?id=${watch.id}">
        <div class="relative">
          <img alt="${watch.name}" class="w-full h-48 object-cover transition-transform duration-300 group-hover:scale-105" src="${watch.image}">
          <button class="absolute top-3 right-3 p-2 rounded-full transition-colors duration-200 bg-luxury-white/90 text-luxury-gray-dark hover:text-luxury-gold favorite-button" data-id="${watch.id}" data-name="${watch.name}" data-price="${watch.price}" data-image="${watch.image}" data-brand="${watch.brand}" onclick="event.preventDefault(); event.stopPropagation();">
            <svg class="lucide lucide-heart" fill="none" height="16" stroke="currentColor" stroke-linecap="round" stroke-linejoin="round" stroke-width="2" viewBox="0 0 24 24" width="16" xmlns="http://www.w3.org/2000/svg">
              <path d="M19 14c1.49-1.46 3-3.21 3-5.5A5.5 5.5 0 0 0 16.5 3c-1.76 0-3 .5-4.5 2-1.5-1.5-2.74-2-4.5-2A5.5 5.5 0 0 0 2 8.5c0 2.3 1.5 4.05 3 5.5l7 7Z"></path>
            </svg>
          </button>
        </div>
      </a>
      <div class="p-4">
        <div class="flex items-center justify-between mb-2">
          <span class="text-sm text-luxury-gold font-medium">${watch.brand}</span>
          <div class="flex items-center">
            <svg class="lucide lucide-star fill-luxury-gold text-luxury-gold" fill="none" height="12" stroke="currentColor" stroke-linecap="round" stroke-linejoin="round" stroke-width="2" viewBox="0 0 24 24" width="12" xmlns="http://www.w3.org/2000/svg">
              <path d="M11.525 2.295a.53.53 0 0 1 .95 0l2.31 4.679a2.123 2.123 0 0 0 1.595 1.16l5.166.756a.53.53 0 0 1 .294.904l-3.736 3.638a2.123 2.123 0 0 0-.611 1.878l.882 5.14a.53.53 0 0 1-.771.56l-4.618-2.428a2.122 2.122 0 0 0-1.973 0L6.396 21.01a.53.53 0 0 1-.77-.56l.881-5.139a2.122 2.122 0 0 0-.611-1.879L2.16 9.795a.53.53 0 0 1 .294-.906l5.165-.755a2.122 2.122 0 0 0 1.597-1.16z"></path>
            </svg>
            <svg class="lucide lucide-star fill-luxury-gold text-luxury-gold" fill="none" height="12" stroke="currentColor" stroke-linecap="round" stroke-linejoin="round" stroke-width="2" viewBox="0 0 24 24" width="12" xmlns="http://www.w3.org/2000/svg">
              <path d="M11.525 2.295a.53.53 0 0 1 .95 0l2.31 4.679a2.123 2.123 0 0 0 1.595 1.16l5.166.756a.53.53 0 0 1 .294.904l-3.736 3.638a2.123 2.123 0 0 0-.611 1.878l.882 5.14a.53.53 0 0 1-.771.56l-4.618-2.428a2.122 2.122 0 0 0-1.973 0L6.396 21.01a.53.53 0 0 1-.77-.56l.881-5.139a2.122 2.122 0 0 0-.611-1.879L2.16 9.795a.53.53 0 0 1 .294-.906l5.165-.755a2.122 2.122 0 0 0 1.597-1.16z"></path>
            </svg>
            <svg class="lucide lucide-star fill-luxury-gold text-luxury-gold" fill="none" height="12" stroke="currentColor" stroke-linecap="round" stroke-linejoin="round" stroke-width="2" viewBox="0 0 24 24" width="12" xmlns="http://www.w3.org/2000/svg">
              <path d="M11.525 2.295a.53.53 0 0 1 .95 0l2.31 4.679a2.123 2.123 0 0 0 1.595 1.16l5.166.756a.53.53 0 0 1 .294.904l-3.736 3.638a2.123 2.123 0 0 0-.611 1.878l.882 5.14a.53.53 0 0 1-.771.56l-4.618-2.428a2.122 2.122 0 0 0-1.973 0L6.396 21.01a.53.53 0 0 1-.77-.56l.881-5.139a2.122 2.122 0 0 0-.611-1.879L2.16 9.795a.53.53 0 0 1 .294-.906l5.165-.755a2.122 2.122 0 0 0 1.597-1.16z"></path>
            </svg>
            <svg class="lucide lucide-star fill-luxury-gold text-luxury-gold" fill="none" height="12" stroke="currentColor" stroke-linecap="round" stroke-linejoin="round" stroke-width="2" viewBox="0 0 24 24" width="12" xmlns="http://www.w3.org/2000/svg">
              <path d="M11.525 2.295a.53.53 0 0 1 .95 0l2.31 4.679a2.123 2.123 0 0 0 1.595 1.16l5.166.756a.53.53 0 0 1 .294.904l-3.736 3.638a2.123 2.123 0 0 0-.611 1.878l.882 5.14a.53.53 0 0 1-.771.56l-4.618-2.428a2.122 2.122 0 0 0-1.973 0L6.396 21.01a.53.53 0 0 1-.77-.56l.881-5.139a2.122 2.122 0 0 0-.611-1.879L2.16 9.795a.53.53 0 0 1 .294-.906l5.165-.755a2.122 2.122 0 0 0 1.597-1.16z"></path>
            </svg>
            <svg class="lucide lucide-star fill-luxury-gold text-luxury-gold" fill="none" height="12" stroke="currentColor" stroke-linecap="round" stroke-linejoin="round" stroke-width="2" viewBox="0 0 24 24" width="12" xmlns="http://www.w3.org/2000/svg">
              <path d="M11.525 2.295a.53.53 0 0 1 .95 0l2.31 4.679a2.123 2.123 0 0 0 1.595 1.16l5.166.756a.53.53 0 0 1 .294.904l-3.736 3.638a2.123 2.123 0 0 0-.611 1.878l.882 5.14a.53.53 0 0 1-.771.56l-4.618-2.428a2.122 2.122 0 0 0-1.973 0L6.396 21.01a.53.53 0 0 1-.70-.56l.881-5.139a2.122 2.122 0 0 0-.611-1.879L2.16 9.795a.53.53 0 0 1 .294-.906l5.165-.755a2.122 2.122 0 0 0 1.597-1.16z"></path>
            </svg>
          </div>
        </div>
        <h3 class="font-semibold text-luxury-black mb-2 group-hover:text-luxury-gold transition-colors duration-200">${watch.name}</h3>
        <p class="text-xl font-bold text-luxury-black">$${watch.price.toLocaleString()}</p>
        <button class="add-to-cart mt-4 inline-flex items-center justify-center gap-2 whitespace-nowrap rounded-md text-sm ring-offset-background transition-colors focus-visible:outline-none focus-visible:ring-2 focus-visible:ring-ring focus-visible:ring-offset-2 disabled:pointer-events-none disabled:opacity-50 [&_svg]:pointer-events-none [&_svg]:size-4 [&_svg]:shrink-0 h-10 px-4 py-2 bg-luxury-gold hover:bg-luxury-gold-dark text-luxury-black font-semibold w-full"
                data-id="${watch.id}"
                data-name="${watch.name}"
                data-price="${watch.price}"
                data-image="${watch.image}"
                data-brand="${watch.brand}">
          <svg xmlns="http://www.w3.org/2000/svg" width="24" height="24" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round" class="lucide lucide-shopping-cart mr-2 h-5 w-5">
            <circle cx="8" cy="21" r="1"></circle>
            <circle cx="19" cy="21" r="1"></circle>
            <path d="M2.05 2.05h2l2.66 12.42a2 2 0 0 0 2 1.58h9.78a2 2 0 0 0 1.95-1.57l1.65-7.43H5.12"></path>
          </svg>
          Add to Cart
        </button>
      </div>
    </div>
  `).join('');
  
  // Re-attach event listeners
  FavoritesManager.attachFavoriteListeners();
  CartManager.attachCartListeners();
}

// Update watch page content with specific watch data
function updateWatchPageContent(watch) {
  // Update page title
  document.title = `${watch.name} - ${watch.brand} | Teluxe`;
  
  // Update watch image
  const watchImage = document.querySelector('.px-4.space-y-6 img');
  if (watchImage) {
    watchImage.src = watch.image;
    watchImage.alt = watch.name;
  }
  
  // Update watch name and brand
  const watchNameElement = document.querySelector('.text-2xl.font-bold.text-luxury-black');
  if (watchNameElement) {
    watchNameElement.textContent = watch.name;
  }
  
  const watchBrandElement = document.querySelector('.text-lg.text-luxury-gold.font-medium');
  if (watchBrandElement) {
    watchBrandElement.textContent = watch.brand;
  }
  
  // Update price
  const priceElement = document.querySelector('.text-3xl.font-bold.text-luxury-black');
  if (priceElement) {
    priceElement.textContent = `$${watch.price.toLocaleString()}`;
  }
  
  // Update description
  const descriptionElement = document.querySelector('.text-luxury-gray-dark.leading-relaxed');
  if (descriptionElement) {
    descriptionElement.textContent = watch.description;
  }
  
  // Update specifications
  const specsContainer = document.querySelector('.grid.grid-cols-2.gap-4');
  if (specsContainer) {
    specsContainer.innerHTML = Object.entries(watch.specifications).map(([key, value]) => `
      <div class="text-center">
        <p class="font-semibold text-luxury-black">${value}</p>
        <p class="text-sm text-luxury-gray-dark">${key}</p>
      </div>
    `).join('');
  }
  
  // Update favorite button data attributes
  const favoriteButton = document.querySelector('.favorite-button');
  if (favoriteButton) {
    favoriteButton.setAttribute('data-id', watch.id);
    favoriteButton.setAttribute('data-name', watch.name);
    favoriteButton.setAttribute('data-price', watch.price);
    favoriteButton.setAttribute('data-image', watch.image);
    favoriteButton.setAttribute('data-brand', watch.brand);
  }
  
  // Update add to cart button data attributes
  const addToCartButton = document.querySelector('.add-to-cart.product-detail-add-to-cart');
  if (addToCartButton) {
    addToCartButton.setAttribute('data-id', watch.id);
    addToCartButton.setAttribute('data-name', watch.name);
    addToCartButton.setAttribute('data-price', watch.price);
    addToCartButton.setAttribute('data-image', watch.image);
    addToCartButton.setAttribute('data-brand', watch.brand);
  }
  
  // Update page data-id attribute
  const pageContainer = document.querySelector('.px-4.space-y-6[data-id]');
  if (pageContainer) {
    pageContainer.setAttribute('data-id', watch.id);
  }
}
