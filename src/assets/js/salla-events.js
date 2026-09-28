/**
 * Salla Twilight Frontend Event Integrations
 * Attaches to Salla Twilight JavaScript SDK events on the storefront.
 */

document.addEventListener('DOMContentLoaded', () => {
  if (typeof salla === 'undefined') {
    console.warn('Salla Twilight SDK is not loaded. Operating in offline/fallback mode.');
    return;
  }

  // 1. Listen for Add to Cart events
  salla.cart.event.onItemAdded((response) => {
    console.log('[Salla Event] Item added to cart:', response);
    // Refresh cart summary counter and trigger custom luxury drawer
    const toast = document.getElementById('toast');
    if (toast) {
      toast.classList.remove('opacity-0', 'pointer-events-none');
      setTimeout(() => toast.classList.add('opacity-0', 'pointer-events-none'), 3000);
    }
  });

  // 2. Listen for Item Removed events
  salla.cart.event.onItemRemoved((response) => {
    console.log('[Salla Event] Item removed from cart:', response);
  });

  // 3. Listen for Customer Wishlist updates
  salla.wishlist.event.onAdded((response) => {
    console.log('[Salla Event] Added to wishlist:', response);
  });
});
