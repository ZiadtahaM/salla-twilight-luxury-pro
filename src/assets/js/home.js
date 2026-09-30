/**
 * Luxury Pro — Homepage JS
 * Compiled by webpack → public/home.js
 *
 * Handles homepage-specific interactivity: hero animations, sliders.
 */

document.addEventListener('DOMContentLoaded', () => {
    initHeroAnimation();
    initComponentObservers();
});

// ─── Hero section entrance animation ─────────────────────────────────────────

function initHeroAnimation() {
    const hero = document.querySelector('[data-luxury-hero]');
    if (!hero) return;

    const elements = hero.querySelectorAll('[data-animate]');
    elements.forEach((el, i) => {
        el.style.animationDelay = `${i * 0.15}s`;
        el.classList.add('animate-fade-up');
    });
}

// ─── Intersection observer for section reveals ────────────────────────────────

function initComponentObservers() {
    if (!('IntersectionObserver' in window)) return;

    const revealObserver = new IntersectionObserver((entries) => {
        entries.forEach(entry => {
            if (entry.isIntersecting) {
                entry.target.classList.add('animate-fade-up');
                revealObserver.unobserve(entry.target);
            }
        });
    }, { threshold: 0.1 });

    document.querySelectorAll('[data-reveal]').forEach(el => {
        revealObserver.observe(el);
    });
}
