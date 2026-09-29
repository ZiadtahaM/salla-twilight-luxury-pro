# Specification: Salla Twilight Multi-Page Luxury Storefront & Partner Engine

## 1. Exact Problem Statement
The storefront preview currently redirects all navigation tabs to the same index view, lacking discrete pages for product catalog, single product detail, cart review, order tracking, and VIP account management. Furthermore, the storefront styling and presentation must meet Salla Partners tier quality, reflecting authentic Saudi luxury e-commerce aesthetics and strict Twilight engine architecture rather than generic templates.

## 2. Public API and Data Boundary Contract
- Twig Layout Boundaries: Pages inherit from `src/views/layouts/master.twig` and utilize `{{ salla_header() }}` and `{{ salla_footer() }}`.
- Salla Component Layer: Native custom elements `<salla-product-card>`, `<salla-slider>`, `<salla-modal>`, `<salla-add-product-button>`, and `<salla-cart-summary>` maintain native event boundaries.
- JavaScript SDK Integration: Client interactions subscribe to `salla.cart.event.*`, `salla.wishlist.event.*`, and custom drawer state.
- Discrete Navigation Routes:
  - Home: `index.html` (Arabic RTL) and `preview-en.html` (English LTR)
  - Collections / Catalog: `categories.html` and `categories-en.html`
  - Product Detail: `product.html` and `product-en.html`
  - Cart Review: `cart.html` and `cart-en.html`
  - Order Tracking: `tracking.html` and `tracking-en.html`
  - Customer VIP Portal: `account.html` and `account-en.html`
- Offline Image Fallback: All imagery uses self-contained SVG vectors to guarantee sub-50ms render times without external network timeout risks.

## 3. Acceptance Criteria Checklist
- [x] AC 1: All navigation links across desktop and mobile headers resolve to discrete, functional HTML pages with active tab highlights.
- [x] AC 2: Quick-cart sliding drawer operates seamlessly across all pages in both Arabic (RTL) and English (LTR).
- [x] AC 3: High-craft Saudi luxury aesthetic implemented with warm gold (#C5A059), obsidian (#111111), and ivory parchment (#FAF9F6) palettes, serif typography, and micro-interactions.
- [x] AC 4: Complete Salla Twilight Twig templates exist in `src/views/pages/` corresponding to all routes.
- [x] AC 5: Local HTTP server hosts the compiled multi-page suite on port 8080 with zero 404 broken links.
- [x] AC 6: Automated Playwright visual regression captures full-page desktop and mobile screenshots for all pages.
- [x] AC 7: Agent Suit verification suite executes and reports 10/10 passing predicates.
- [x] AC 8: Git commits synchronized with remote repository ZiadtahaM/salla-twilight-luxury-pro.

## 4. Blocked-By / Depends-On DAG Relationships
- Task 1 (Build Script Hardening): Refine `scripts/build_full_store.js` with self-contained assets and bidirectional routes.
- Task 2 (Compilation): Compile all Arabic and English pages into `dist/`. Depends on Task 1.
- Task 3 (Twig Architecture Sync): Verify and align `src/views/pages/` Twig templates with Salla Twilight specs. Depends on Task 1.
- Task 4 (Daemon Server): Start background HTTP server on port 8080. Depends on Task 2.
- Task 5 (Visual Screenshots): Capture Playwright screenshots. Depends on Task 4.
- Task 6 (Agent Suit Audit): Run `scripts/verify_with_agent_suit.py`. Depends on Task 2.
- Task 7 (Git Sync): Commit and push changes to GitHub. Depends on Task 5 and Task 6.

## 5. Sandbox Decoupling Plan (DDIA Sandbox Decoupling)
All page builds and visual captures execute in local ephemeral sandboxes with mock data from `mock/store-data.json`. No live customer PII is handled, and all network calls are stubbed or routed to local vectors to prevent external telemetry leakage.
