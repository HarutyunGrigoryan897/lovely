// script.js

// -------------------- NAVIGATION --------------------
document.querySelectorAll("nav a").forEach(link => {
  link.addEventListener("click", e => {
    e.preventDefault();
    const href = link.getAttribute("href");
    if (href) {
      window.location.href = href; // navigate to correct page
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

// -------------------- CART LOGIC --------------------
let cart = [];

// Add to cart buttons
document.querySelectorAll(".add-to-cart").forEach(btn => {
  btn.addEventListener("click", () => {
    const productId = btn.dataset.id;
    const productName = btn.dataset.name;
    const productPrice = parseFloat(btn.dataset.price);

    const existing = cart.find(item => item.id === productId);
    if (existing) {
      existing.qty += 1;
    } else {
      cart.push({ id: productId, name: productName, price: productPrice, qty: 1 });
    }
    updateCartUI();
  });
});

// Cart UI update
function updateCartUI() {
  const cartContainer = document.querySelector(".cart-items");
  const totalEl = document.querySelector(".cart-total");

  if (!cartContainer || !totalEl) return;

  cartContainer.innerHTML = "";
  let total = 0;

  cart.forEach(item => {
    const row = document.createElement("div");
    row.classList.add("cart-item");
    row.innerHTML = `
      <span>${item.name} x ${item.qty}</span>
      <span>$${(item.price * item.qty).toFixed(2)}</span>
      <button class="remove" data-id="${item.id}">Remove</button>
    `;
    cartContainer.appendChild(row);

    total += item.price * item.qty;
  });

  totalEl.textContent = `$${total.toFixed(2)}`;

  // Remove item handler
  document.querySelectorAll(".cart-item .remove").forEach(btn => {
    btn.addEventListener("click", () => {
      const id = btn.dataset.id;
      cart = cart.filter(item => item.id !== id);
      updateCartUI();
    });
  });
}

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
