/* ── AuraBazaar Cart ─────────────────────────────────────────
   Single source of truth for all cart state and UI.
   Loaded once in base.html, available on every page.
────────────────────────────────────────────────────────────── */

var Cart = (function () {
  var _data = {};

  function _load() {
    try {
      _data = JSON.parse(localStorage.getItem("ab_cart")) || {};
    } catch (e) {
      _data = {};
    }
  }

  function _save() {
    localStorage.setItem("ab_cart", JSON.stringify(_data));
  }

  function _totalQty() {
    return Object.values(_data).reduce(function (s, i) {
      return s + i[0];
    }, 0);
  }

  function _totalPrice() {
    return Object.values(_data).reduce(function (s, i) {
      return s + i[0] * i[2];
    }, 0);
  }

  function _renderOffcanvas() {
    var list = document.getElementById("cart-lines");
    var totalEl = document.getElementById("cart-total");
    var countEl = document.getElementById("cart-count");
    if (countEl) countEl.textContent = _totalQty();
    if (!list) return;

    var keys = Object.keys(_data).filter(function (k) {
      return _data[k][0] > 0;
    });

    if (keys.length === 0) {
      list.innerHTML =
        '<div class="cart-empty">' +
        '<svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.5">' +
        '<path d="M6 2L3 6v14a2 2 0 002 2h14a2 2 0 002-2V6l-3-4z"/>' +
        '<line x1="3" y1="6" x2="21" y2="6"/>' +
        '<path d="M16 10a4 4 0 01-8 0"/>' +
        "</svg>" +
        "<p>Your cart is empty</p>" +
        "</div>";
      if (totalEl) totalEl.textContent = "0";
      return;
    }

    var html = "";
    keys.forEach(function (id) {
      var item = _data[id];
      html +=
        '<div class="cart-line">' +
        '<div class="cart-line-info">' +
        '<div class="cart-line-name">' +
        item[1] +
        "</div>" +
        '<div class="cart-line-price">Rs. ' +
        item[2] +
        " × " +
        item[0] +
        "</div>" +
        "</div>" +
        '<div class="qty-control">' +
        "<button onclick=\"Cart.change('" +
        id +
        '\', -1)" aria-label="decrease">−</button>' +
        "<span>" +
        item[0] +
        "</span>" +
        "<button onclick=\"Cart.change('" +
        id +
        '\', 1)" aria-label="increase">+</button>' +
        "</div>" +
        "</div>";
    });

    list.innerHTML = html;
    if (totalEl) totalEl.textContent = _totalPrice();
  }

  // Called by index/search pages to refresh card-level buttons
  function _refreshCardButtons() {
    document.querySelectorAll("[data-product-id]").forEach(function (wrapper) {
      var id = wrapper.dataset.productId;
      var qty = _data[id] && _data[id][0] ? _data[id][0] : 0;
      var actions = wrapper.querySelector(".product-card-actions");
      if (!actions) return;

      if (qty > 0) {
        actions.querySelector(".btn-add-wrap").innerHTML =
          '<div class="qty-stepper">' +
          "<button onclick=\"Cart.change('" +
          id +
          '\', -1); Cart.refreshCards()" aria-label="decrease">−</button>' +
          "<span>" +
          qty +
          "</span>" +
          "<button onclick=\"Cart.change('" +
          id +
          '\', 1); Cart.refreshCards()" aria-label="increase">+</button>' +
          "</div>";
      } else {
        var name = wrapper.dataset.name;
        var price = wrapper.dataset.price;
        actions.querySelector(".btn-add-wrap").innerHTML =
          '<button class="btn-add" onclick="Cart.add(\'' +
          id +
          "', '" +
          name.replace(/'/g, "\\'") +
          "', " +
          price +
          '); Cart.refreshCards()">' +
          '<svg width="14" height="14" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2.5">' +
          '<path d="M12 5v14M5 12h14"/>' +
          "</svg>" +
          "Add" +
          "</button>";
      }
    });
  }

  /* ── Public API ─────────────────────────────────────────── */
  function add(id, name, price) {
    id = String(id);
    if (_data[id]) {
      _data[id][0] += 1;
    } else {
      _data[id] = [1, name, parseInt(price)];
    }
    _save();
    _renderOffcanvas();
    showToast(name + " added to cart");
  }

  function change(id, delta) {
    id = String(id);
    if (!_data[id]) return;
    _data[id][0] = Math.max(0, _data[id][0] + delta);
    if (_data[id][0] === 0) delete _data[id];
    _save();
    _renderOffcanvas();
  }

  function clear() {
    _data = {};
    _save();
    _renderOffcanvas();
    _refreshCardButtons();
    showToast("Cart cleared");
  }

  function getData() {
    return _data;
  }

  function refreshCards() {
    _refreshCardButtons();
  }

  function init() {
    _load();
    _renderOffcanvas();
    _refreshCardButtons();
  }

  return {
    add: add,
    change: change,
    clear: clear,
    getData: getData,
    refreshCards: refreshCards,
    init: init,
  };
})();

/* ── Toast ────────────────────────────────────────────────── */
function showToast(msg) {
  var stack = document.getElementById("toast-stack");
  if (!stack) return;
  var el = document.createElement("div");
  el.className = "toast";
  el.innerHTML =
    '<svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2.5">' +
    '<polyline points="20 6 9 17 4 12"/>' +
    "</svg>" +
    msg;
  stack.appendChild(el);
  setTimeout(function () {
    el.remove();
  }, 3000);
}

/* ── Offcanvas ────────────────────────────────────────────── */
function openCart() {
  document.getElementById("cart-offcanvas").classList.add("open");
  document.getElementById("cart-overlay").classList.add("open");
  document.body.style.overflow = "hidden";
}

function closeCart() {
  document.getElementById("cart-offcanvas").classList.remove("open");
  document.getElementById("cart-overlay").classList.remove("open");
  document.body.style.overflow = "";
}

document.addEventListener("DOMContentLoaded", function () {
  Cart.init();

  var overlay = document.getElementById("cart-overlay");
  if (overlay) overlay.addEventListener("click", closeCart);

  // Mobile nav toggle
  var toggle = document.getElementById("nav-toggle");
  var navLinks = document.getElementById("nav-links");
  if (toggle && navLinks) {
    toggle.addEventListener("click", function () {
      navLinks.classList.toggle("open");
    });
  }
});
