# Path B: Retrofit Webpack Build Pipeline into Existing Luxury Theme

## Problem Statement

The `salla-twilight-luxury-pro` theme has valid Twig templates and a luxury design system
but cannot render inside Salla's Twilight engine because it lacks:
- A webpack/postcss/tailwind compilation pipeline
- Compiled CSS/JS output in `public/`
- 14+ missing page templates that Salla routes require
- Proper `header.twig` and `footer.twig` components
- Locale JSON files for translation strings

## Public API / Data Boundary Contract

The theme must produce the following compiled outputs in `public/`:
- `app.css` (compiled from `src/assets/styles/app.scss` via PostCSS + Tailwind)
- `app.js` (compiled from `src/assets/js/app.js` via Webpack + Babel)
- `home.js` (homepage-specific logic)
- `product-card.js`, `main-menu.js`, `add-product-toast.js` (partials)
- `images/` (static assets copied via CopyPlugin)

Templates must load assets via `{{ 'app.css' | asset }}` and `{{ 'app.js' | asset }}`.

## Acceptance Criteria

### Phase 1: Build Pipeline
- [ ] AC-1: `webpack.config.js` exists with entry points for app, home, and partials
- [ ] AC-2: `postcss.config.js` exists with `postcss-import`, `tailwindcss/nesting`, `tailwindcss`, `autoprefixer`
- [ ] AC-3: `tailwind.config.js` scans `src/views/**/*.twig` and `src/assets/js/**/*.js`, extends luxury color palette
- [ ] AC-4: `src/assets/styles/app.scss` exists as SCSS entry point with `@tailwind base/components/utilities` and luxury variable overrides
- [ ] AC-5: `src/assets/js/app.js` exists with Salla Web Component event listeners and Twilight initialization
- [ ] AC-6: `package.json` has all devDependencies: webpack, webpack-cli, css-loader, sass-loader, postcss-loader, mini-css-extract-plugin, css-minimizer-webpack-plugin, copy-webpack-plugin, @babel/core, babel-loader, @babel/preset-env, @babel/runtime, tailwindcss, postcss, postcss-import, postcss-nesting, autoprefixer, sass, @salla.sa/twilight
- [ ] AC-7: `pnpm install` succeeds without errors
- [ ] AC-8: `pnpm run production` produces `public/app.css` and `public/app.js` without errors
- [ ] AC-9: `pnpm run watch` starts webpack in watch mode (replaces the no-op placeholder)

### Phase 2: Template Completeness
- [ ] AC-10: `master.twig` loads `{{ 'app.css' | asset }}` and `{{ 'app.js' | asset }}` instead of inline styles
- [ ] AC-11: `components/header/header.twig` exists as a proper Salla component (extracted from master.twig inline header)
- [ ] AC-12: `components/footer/footer.twig` exists as a proper Salla component (extracted from master.twig inline footer)
- [ ] AC-13: All required page templates exist: blog/index, blog/single, brands/index, brands/single, customer/orders/index, customer/orders/single, customer/wishlist, customer/wallet, customer/notifications, customer/profile, loyalty, thank-you, testimonials, page-single
- [ ] AC-14: `src/locales/ar.json` and `src/locales/en.json` exist with translation strings

### Phase 3: Integration Verification
- [ ] AC-15: `salla theme preview` starts without errors
- [ ] AC-16: The preview URL renders the luxury theme with styles and Salla Web Components functional
- [ ] AC-17: RTL (Arabic) layout works correctly
- [ ] AC-18: Mobile responsive layout works (tested at 375px width)

## Depends-On

- Node.js v22.14.0 (confirmed installed)
- pnpm (needs corepack enable or direct install)
- GitHub repo `ZiadtahaM/salla-twilight-luxury-pro` (confirmed, theme ID 1252059893)

## Sandbox Decoupling Plan

All compilation runs locally. No production data involved. The `salla theme preview` uses an
authenticated draft session on the demo store only. No risk of impacting a live merchant store.
