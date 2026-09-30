/**
 * Luxury Pro — Main JS Entry Point
 * Compiled by webpack → public/app.js
 *
 * Initializes Salla Web Components event system and core theme behavior.
 */

// ─── Salla Platform Event Listeners ─────────────────────────────────────────

document.addEventListener('DOMContentLoaded', () => {
    initHeader();
    initMobileMenu();
    initSallaEvents();
});

// ─── Header scroll behavior ──────────────────────────────────────────────────

function initHeader() {
    const header = document.querySelector('.luxury-header');
    if (!header) return;

    const onScroll = () => {
        header.classList.toggle('scrolled', window.scrollY > 20);
    };

    window.addEventListener('scroll', onScroll, { passive: true });
    onScroll(); // Run once on load
}

// ─── Mobile menu toggle ──────────────────────────────────────────────────────

function initMobileMenu() {
    const triggers = document.querySelectorAll('[data-menu-trigger]');
    const menu = document.querySelector('[data-mobile-menu]');
    const overlay = document.querySelector('[data-menu-overlay]');

    if (!triggers.length || !menu) return;

    const openMenu = () => {
        menu.classList.remove('-translate-x-full', 'translate-x-full');
        menu.classList.add('translate-x-0');
        if (overlay) overlay.classList.remove('hidden');
        document.body.style.overflow = 'hidden';
    };

    const closeMenu = () => {
        menu.classList.add(document.documentElement.dir === 'rtl' ? 'translate-x-full' : '-translate-x-full');
        menu.classList.remove('translate-x-0');
        if (overlay) overlay.classList.add('hidden');
        document.body.style.overflow = '';
    };

    triggers.forEach(t => t.addEventListener('click', openMenu));
    if (overlay) overlay.addEventListener('click', closeMenu);

    // Close on Escape
    document.addEventListener('keydown', (e) => {
        if (e.key === 'Escape') closeMenu();
    });
}

// ─── Salla Web Component Events ──────────────────────────────────────────────

function initSallaEvents() {
    // Guard: Salla's event system may not be loaded yet on some pages
    if (typeof salla === 'undefined') return;

    // Cart updated — refresh cart summary
    salla.event.on('cart.updated', () => {
        // salla-cart-summary web component auto-updates; nothing needed here
        // Custom animations or notifications can go here
    });

    // Product added to cart
    salla.event.on('product.addedToCart', (event) => {
        const { product } = event.detail || {};
        if (!product) return;
        // Trigger the native Salla add-product-toast
        document.dispatchEvent(new CustomEvent('salla:product:added', {
            detail: { product }
        }));
    });

    // Wishlist toggled
    salla.event.on('wishlist.toggled', (event) => {
        // Salla handles wishlist state; hook here for analytics or animations
    });

    // Order completed
    salla.event.on('checkout.completed', (event) => {
        // Hook for post-purchase events (analytics, loyalty messages, etc.)
    });
}

// ─── Lazy loading for images ─────────────────────────────────────────────────

if ('IntersectionObserver' in window) {
    const lazyImages = document.querySelectorAll('img[data-src]');
    const imageObserver = new IntersectionObserver((entries) => {
        entries.forEach(entry => {
            if (entry.isIntersecting) {
                const img = entry.target;
                img.src = img.dataset.src;
                if (img.dataset.srcset) img.srcset = img.dataset.srcset;
                img.removeAttribute('data-src');
                imageObserver.unobserve(img);
            }
        });
    }, { rootMargin: '200px 0px' });

    lazyImages.forEach(img => imageObserver.observe(img));
}
