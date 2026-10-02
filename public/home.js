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

/***/ "./src/assets/js/home.js"
/*!*******************************!*\
  !*** ./src/assets/js/home.js ***!
  \*******************************/
() {

eval("{/**\n * Luxury Pro — Homepage JS\n * Compiled by webpack → public/home.js\n *\n * Handles homepage-specific interactivity: hero animations, sliders.\n */\n\ndocument.addEventListener('DOMContentLoaded', function () {\n  initHeroAnimation();\n  initComponentObservers();\n});\n\n// ─── Hero section entrance animation ─────────────────────────────────────────\n\nfunction initHeroAnimation() {\n  var hero = document.querySelector('[data-luxury-hero]');\n  if (!hero) return;\n  var elements = hero.querySelectorAll('[data-animate]');\n  elements.forEach(function (el, i) {\n    el.style.animationDelay = \"\".concat(i * 0.15, \"s\");\n    el.classList.add('animate-fade-up');\n  });\n}\n\n// ─── Intersection observer for section reveals ────────────────────────────────\n\nfunction initComponentObservers() {\n  if (!('IntersectionObserver' in window)) return;\n  var revealObserver = new IntersectionObserver(function (entries) {\n    entries.forEach(function (entry) {\n      if (entry.isIntersecting) {\n        entry.target.classList.add('animate-fade-up');\n        revealObserver.unobserve(entry.target);\n      }\n    });\n  }, {\n    threshold: 0.1\n  });\n  document.querySelectorAll('[data-reveal]').forEach(function (el) {\n    revealObserver.observe(el);\n  });\n}\n\n//# sourceURL=webpack://salla-twilight-luxury-pro/./src/assets/js/home.js?\n}");

/***/ }

/******/ 	});
/************************************************************************/
/******/ 	
/******/ 	// startup
/******/ 	// Load entry module and return exports
/******/ 	// This entry module can't be inlined because the eval devtool is used.
/******/ 	let __webpack_exports__ = {};
/******/ 	__webpack_modules__["./src/assets/js/home.js"]();
/******/ 	
/******/ })()
;