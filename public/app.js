/*
 * ATTENTION: The "eval" devtool has been used (maybe by default in mode: "development").
 * This devtool is neither made for production nor for readable output files.
 * It uses "eval()" calls to create a separate source file in the browser devtools.
 * If you are trying to read the output file, select a different devtool (https://webpack.js.org/configuration/devtool/)
 * or disable the default devtool with "devtool: false".
 * If you are looking for production-ready output files, see mode: "production" (https://webpack.js.org/configuration/mode/).
 */
/******/ (() => { // webpackBootstrap
/******/ 	var __webpack_modules__ = ({

/***/ "./src/assets/js/app.js"
/*!******************************!*\
  !*** ./src/assets/js/app.js ***!
  \******************************/
() {

eval("{/**\n * Luxury Pro — Main JS Entry Point\n * Compiled by webpack → public/app.js\n *\n * Initializes Salla Web Components event system and core theme behavior.\n */\n\n// ─── Salla Platform Event Listeners ─────────────────────────────────────────\n\ndocument.addEventListener('DOMContentLoaded', function () {\n  initHeader();\n  initMobileMenu();\n  initSallaEvents();\n});\n\n// ─── Header scroll behavior ──────────────────────────────────────────────────\n\nfunction initHeader() {\n  var header = document.querySelector('.luxury-header');\n  if (!header) return;\n  var onScroll = function onScroll() {\n    header.classList.toggle('scrolled', window.scrollY > 20);\n  };\n  window.addEventListener('scroll', onScroll, {\n    passive: true\n  });\n  onScroll(); // Run once on load\n}\n\n// ─── Mobile menu toggle ──────────────────────────────────────────────────────\n\nfunction initMobileMenu() {\n  var triggers = document.querySelectorAll('[data-menu-trigger]');\n  var menu = document.querySelector('[data-mobile-menu]');\n  var overlay = document.querySelector('[data-menu-overlay]');\n  if (!triggers.length || !menu) return;\n  var openMenu = function openMenu() {\n    menu.classList.remove('-translate-x-full', 'translate-x-full');\n    menu.classList.add('translate-x-0');\n    if (overlay) overlay.classList.remove('hidden');\n    document.body.style.overflow = 'hidden';\n  };\n  var closeMenu = function closeMenu() {\n    menu.classList.add(document.documentElement.dir === 'rtl' ? 'translate-x-full' : '-translate-x-full');\n    menu.classList.remove('translate-x-0');\n    if (overlay) overlay.classList.add('hidden');\n    document.body.style.overflow = '';\n  };\n  triggers.forEach(function (t) {\n    return t.addEventListener('click', openMenu);\n  });\n  if (overlay) overlay.addEventListener('click', closeMenu);\n\n  // Close on Escape\n  document.addEventListener('keydown', function (e) {\n    if (e.key === 'Escape') closeMenu();\n  });\n}\n\n// ─── Salla Web Component Events ──────────────────────────────────────────────\n\nfunction initSallaEvents() {\n  // Guard: Salla's event system may not be loaded yet on some pages\n  if (typeof salla === 'undefined') return;\n\n  // Cart updated — refresh cart summary\n  salla.event.on('cart.updated', function () {\n    // salla-cart-summary web component auto-updates; nothing needed here\n    // Custom animations or notifications can go here\n  });\n\n  // Product added to cart\n  salla.event.on('product.addedToCart', function (event) {\n    var _ref = event.detail || {},\n      product = _ref.product;\n    if (!product) return;\n    // Trigger the native Salla add-product-toast\n    document.dispatchEvent(new CustomEvent('salla:product:added', {\n      detail: {\n        product: product\n      }\n    }));\n  });\n\n  // Wishlist toggled\n  salla.event.on('wishlist.toggled', function (event) {\n    // Salla handles wishlist state; hook here for analytics or animations\n  });\n\n  // Order completed\n  salla.event.on('checkout.completed', function (event) {\n    // Hook for post-purchase events (analytics, loyalty messages, etc.)\n  });\n}\n\n// ─── Lazy loading for images ─────────────────────────────────────────────────\n\nif ('IntersectionObserver' in window) {\n  var lazyImages = document.querySelectorAll('img[data-src]');\n  var imageObserver = new IntersectionObserver(function (entries) {\n    entries.forEach(function (entry) {\n      if (entry.isIntersecting) {\n        var img = entry.target;\n        img.src = img.dataset.src;\n        if (img.dataset.srcset) img.srcset = img.dataset.srcset;\n        img.removeAttribute('data-src');\n        imageObserver.unobserve(img);\n      }\n    });\n  }, {\n    rootMargin: '200px 0px'\n  });\n  lazyImages.forEach(function (img) {\n    return imageObserver.observe(img);\n  });\n}\n\n//# sourceURL=webpack://salla-twilight-luxury-pro/./src/assets/js/app.js?\n}");

/***/ },

/***/ "./src/assets/styles/app.scss"
/*!************************************!*\
  !*** ./src/assets/styles/app.scss ***!
  \************************************/
(__unused_webpack_module, __webpack_exports__, __webpack_require__) {

"use strict";
eval("{__webpack_require__.r(__webpack_exports__);\n// extracted by mini-css-extract-plugin\n\n\n//# sourceURL=webpack://salla-twilight-luxury-pro/./src/assets/styles/app.scss?\n}");

/***/ }

/******/ 	});
/************************************************************************/
/******/ 	// The require scope
/******/ 	const __webpack_require__ = {};
/******/ 	
/************************************************************************/
/******/ 	/* webpack/runtime/make namespace object */
/******/ 	// define __esModule on exports
/******/ 	__webpack_require__.r = (exports) => {
/******/ 		Object.defineProperty(exports, Symbol.toStringTag, { value: 'Module' });
/******/ 		Object.defineProperty(exports, '__esModule', { value: true });
/******/ 	};
/******/ 	
/************************************************************************/
/******/ 	
/******/ 	// startup
/******/ 	// Load entry module and return exports
/******/ 	// This entry module can't be inlined because the eval devtool is used.
/******/ 	__webpack_modules__["./src/assets/styles/app.scss"](0,{},__webpack_require__);
/******/ 	let __webpack_exports__ = {};
/******/ 	__webpack_modules__["./src/assets/js/app.js"](0,__webpack_exports__,__webpack_require__);
/******/ 	
/******/ })()
;