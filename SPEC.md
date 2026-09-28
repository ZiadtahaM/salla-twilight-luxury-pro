# Architectural Specification: Salla Twilight Luxury Pro Theme

## 1. Problem Statement
Design and engineer a bespoke, calm luxury storefront on Salla Pro for Naif A. The theme must feel exclusive and distinct from stock themes while preserving 100% of native Salla ecommerce capabilities (cart calculations, customer authentication, checkout redirect, shipping estimator, and inventory webhooks).

## 2. Public API & Data Boundary Contract
All data mutations and state queries must flow through Salla Twilight official APIs and native custom elements:
- Storefront hooks: `{{ salla_header() }}` and `{{ salla_footer() }}` must never be omitted.
- Cart and checkout: Use `<salla-cart-summary>`, `<salla-add-product-button>`, and `salla.cart.event.*` rather than naked form posts or custom AJAX endpoints.
- Component registration: Every merchant-editable block must be registered in `twilight.json` under `components` with typed fields, default values, and localized labels.

## 3. Acceptance Criteria Checklist
- [x] AC 1: `twilight.json` passes schema validation with zero duplicate IDs and explicit field types.
- [x] AC 2: Root HTML layout dynamically switches `dir="rtl"` and `dir="ltr"` based on customer language.
- [x] AC 3: High-contrast overlay protection ensures minimum 4.5:1 text contrast on custom banners regardless of merchant-uploaded image brightness.
- [x] AC 4: Responsive image `<picture>` markup eliminates mobile overfetching with dedicated mobile and desktop breakpoints.
- [x] AC 5: Zero text baked into banner artwork; all headings and copy are rendered as live, crawlable HTML.
- [x] AC 6: Focus rings and skip-navigation links allow full keyboard accessibility.
- [x] AC 7: Salla Twilight CI workflow deterministically validates schema and layout hooks on every git push.

## 4. 5-Tier Verification Gate
1. Tier 1 (Static Contract): `node` CI script validates `twilight.json` structure and Twig hook inclusion.
2. Tier 2 (Visual & Breakpoints): 360px (mobile), 768px (tablet), and 1440px (desktop) verified in Arabic and English.
3. Tier 3 (Salla Runtime Invariants): Preview verified through `salla theme preview` on official demo store.
4. Tier 4 (Performance & UX): Core Web Vitals LCP < 2.0s, CLS < 0.05, font loading sub-50ms via preload.
5. Tier 5 (Store Integrity): Zero tampering with Salla secure payment gateways or authenticated session tokens.
