/**
 * scripts/build_full_store.js
 * Master Static Builder for Salla Twilight Luxury Pro Theme
 * Compiles 13 production-grade HTML artifacts into dist/
 * Covers Home, Categories, Product, Cart, Tracking, and Account in Arabic & English.
 * 100% offline self-contained with vector SVG luxury artwork.
 */

const fs = require('fs');
const path = require('path');

const ROOT_DIR = path.resolve(__dirname, '..');
const DIST_DIR = path.join(ROOT_DIR, 'dist');
if (!fs.existsSync(DIST_DIR)) fs.mkdirSync(DIST_DIR, { recursive: true });

// ============================================================================
// 1. HIGH-CRAFT VECTOR GRAPHICS GENERATORS (Zero Network Latency)
// ============================================================================

function generateHeroSvg(width, height, isRtl) {
  const svg = `<svg xmlns="http://www.w3.org/2000/svg" width="${width}" height="${height}" viewBox="0 0 ${width} ${height}">
    <defs>
      <radialGradient id="heroGlow" cx="${isRtl ? '75%' : '25%'}" cy="40%" r="65%">
        <stop offset="0%" stop-color="#2c2720"/>
        <stop offset="45%" stop-color="#191715"/>
        <stop offset="100%" stop-color="#0c0b0a"/>
      </radialGradient>
      <linearGradient id="goldAcc" x1="0%" y1="0%" x2="100%" y2="100%">
        <stop offset="0%" stop-color="#DFC488"/>
        <stop offset="50%" stop-color="#C5A059"/>
        <stop offset="100%" stop-color="#8E6A26"/>
      </linearGradient>
      <pattern id="arabesqueGrid" width="80" height="80" patternUnits="userSpaceOnUse">
        <path d="M40 0 L80 40 L40 80 L0 40 Z" fill="none" stroke="#C5A059" stroke-width="0.75" stroke-opacity="0.12"/>
        <circle cx="40" cy="40" r="14" fill="none" stroke="#C5A059" stroke-width="0.5" stroke-opacity="0.1"/>
        <circle cx="40" cy="40" r="4" fill="#C5A059" fill-opacity="0.15"/>
      </pattern>
    </defs>
    <rect width="${width}" height="${height}" fill="url(#heroGlow)"/>
    <rect width="${width}" height="${height}" fill="url(#arabesqueGrid)"/>
    
    <!-- Atmospheric Luxury Silhouette Curves -->
    <path d="M0,${height * 0.75} Q${width * 0.45},${height * 0.6} ${width},${height * 0.8} L${width},${height} L0,${height} Z" fill="#080707" fill-opacity="0.7"/>
    <path d="M0,${height * 0.85} Q${width * 0.6},${height * 0.72} ${width},${height * 0.9} L${width},${height} L0,${height} Z" fill="#040404" fill-opacity="0.85"/>
    
    <!-- Gold Accents -->
    <circle cx="${isRtl ? width * 0.82 : width * 0.18}" cy="${height * 0.35}" r="${height * 0.28}" fill="url(#goldAcc)" fill-opacity="0.06"/>
    <circle cx="${isRtl ? width * 0.25 : width * 0.75}" cy="${height * 0.6}" r="${height * 0.2}" fill="#ffffff" fill-opacity="0.02"/>
  </svg>`;
  return `data:image/svg+xml;base64,${Buffer.from(svg).toString('base64')}`;
}

function generateProductSvg(id, category, isRtl) {
  // Individualized high-end luxury vector illustrations
  const vectors = {
    abaya: `
      <!-- Cashmere Abaya Silhouette -->
      <path d="M150 110 Q200 80 250 110 L290 420 Q200 440 110 420 Z" fill="#151413"/>
      <path d="M200 110 L200 425" stroke="#C5A059" stroke-width="3" stroke-linecap="round"/>
      <path d="M185 130 Q200 145 215 130" fill="none" stroke="#DFC488" stroke-width="2.5"/>
      <path d="M175 160 Q200 180 225 160" fill="none" stroke="#DFC488" stroke-width="2"/>
      <circle cx="200" cy="210" r="3" fill="#C5A059"/>
      <circle cx="200" cy="240" r="3" fill="#C5A059"/>
      <circle cx="200" cy="270" r="3" fill="#C5A059"/>
    `,
    oud: `
      <!-- Crystal Oud Flacon -->
      <rect x="180" y="90" width="40" height="35" rx="3" fill="#C5A059"/>
      <path d="M190 70 L210 70 L215 90 L185 90 Z" fill="#DFC488"/>
      <rect x="135" y="125" width="130" height="190" rx="14" fill="#2A1B0E" stroke="#C5A059" stroke-width="2"/>
      <rect x="145" y="135" width="110" height="170" rx="8" fill="#B87322" fill-opacity="0.8"/>
      <!-- Label -->
      <rect x="160" y="185" width="80" height="70" fill="#FAF9F6"/>
      <rect x="165" y="190" width="70" height="60" fill="none" stroke="#C5A059" stroke-width="1"/>
      <text x="200" y="215" font-family="serif" font-size="10" font-weight="bold" text-anchor="middle" fill="#111">OUD ROYAL</text>
      <text x="200" y="235" font-family="sans-serif" font-size="7" letter-spacing="1" text-anchor="middle" fill="#888">AGED EXTRACT</text>
    `,
    tote: `
      <!-- Leather Handbag -->
      <path d="M160 160 Q200 80 240 160" fill="none" stroke="#C5A059" stroke-width="6" stroke-linecap="round"/>
      <path d="M125 160 L275 160 L295 350 Q200 370 105 350 Z" fill="#8B4513"/>
      <path d="M140 160 L140 355" stroke="#63300C" stroke-width="2" stroke-dasharray="4,4"/>
      <path d="M260 160 L260 355" stroke="#63300C" stroke-width="2" stroke-dasharray="4,4"/>
      <rect x="185" y="190" width="30" height="24" rx="4" fill="#DFC488" stroke="#8E6A26" stroke-width="1.5"/>
    `,
    teaset: `
      <!-- Imperial Porcelain Tea & Kahwa Set -->
      <path d="M150 200 Q200 160 250 200 L240 310 Q200 330 160 310 Z" fill="#FAF9F6" stroke="#E5E2DC" stroke-width="2"/>
      <path d="M245 220 Q290 250 235 290" fill="none" stroke="#C5A059" stroke-width="5" stroke-linecap="round"/>
      <path d="M155 230 Q120 210 135 270" fill="none" stroke="#C5A059" stroke-width="4"/>
      <circle cx="200" cy="180" r="14" fill="#C5A059"/>
      <path d="M170 240 Q200 255 230 240" fill="none" stroke="#C5A059" stroke-width="2"/>
    `,
    kaftan: `
      <!-- Royal Emerald Silk Kaftan -->
      <path d="M140 110 Q200 85 260 110 L300 420 Q200 440 100 420 Z" fill="#0B3B24"/>
      <path d="M200 110 L200 425" stroke="#C5A059" stroke-width="3"/>
      <path d="M170 110 L230 110 L215 170 L185 170 Z" fill="#C5A059"/>
    `,
    musk: `
      <!-- Imperial White Musk Vial -->
      <rect x="175" y="100" width="50" height="220" rx="25" fill="#FAF9F6" stroke="#E5E2DC" stroke-width="2"/>
      <rect x="185" y="65" width="30" height="35" fill="#DFC488"/>
      <circle cx="200" cy="50" r="15" fill="#C5A059"/>
      <text x="200" y="210" font-family="serif" font-size="11" font-weight="bold" text-anchor="middle" fill="#C5A059">WHITE MUSK</text>
    `,
    wallet: `
      <!-- Alligator Leather Card Holder -->
      <rect x="120" y="170" width="160" height="120" rx="8" fill="#1C1A18" stroke="#C5A059" stroke-width="1.5"/>
      <path d="M120 210 L280 210" stroke="#333" stroke-width="2"/>
      <path d="M120 245 L280 245" stroke="#333" stroke-width="2"/>
      <text x="200" y="278" font-family="serif" font-size="14" font-weight="bold" text-anchor="middle" fill="#DFC488">EM</text>
    `,
    mabkhara: `
      <!-- Artisan Brass Mabkhara -->
      <path d="M150 280 L250 280 L230 350 L170 350 Z" fill="#8E6A26"/>
      <rect x="135" y="260" width="130" height="20" rx="3" fill="#C5A059"/>
      <path d="M145 260 Q200 140 255 260 Z" fill="#DFC488"/>
      <circle cx="200" cy="200" r="8" fill="#8E6A26"/>
      <circle cx="180" cy="225" r="5" fill="#8E6A26"/>
      <circle cx="220" cy="225" r="5" fill="#8E6A26"/>
      <!-- Gold Smoke Tendrils -->
      <path d="M200 130 Q215 95 195 70 Q185 50 200 30" fill="none" stroke="#C5A059" stroke-width="2.5" stroke-linecap="round" opacity="0.6"/>
    `
  };

  const selectedVector = vectors[id] || vectors.abaya;

  const svg = `<svg xmlns="http://www.w3.org/2000/svg" width="400" height="500" viewBox="0 0 400 500">
    <defs>
      <linearGradient id="bgGrad" x1="0%" y1="0%" x2="100%" y2="100%">
        <stop offset="0%" stop-color="#FAF9F6"/>
        <stop offset="100%" stop-color="#EFECE6"/>
      </linearGradient>
      <radialGradient id="pedestalGlow" cx="50%" cy="80%" r="50%">
        <stop offset="0%" stop-color="#DFC488" stop-opacity="0.3"/>
        <stop offset="100%" stop-color="#FAF9F6" stop-opacity="0"/>
      </radialGradient>
    </defs>
    <rect width="400" height="500" fill="url(#bgGrad)"/>
    <ellipse cx="200" cy="420" rx="140" ry="25" fill="url(#pedestalGlow)"/>
    ${selectedVector}
  </svg>`;

  return `data:image/svg+xml;base64,${Buffer.from(svg).toString('base64')}`;
}

// Generate shared SVG images
const heroImgDesktopAr = generateHeroSvg(1920, 960, true);
const heroImgMobileAr = generateHeroSvg(800, 1000, true);
const heroImgDesktopEn = generateHeroSvg(1920, 960, false);
const heroImgMobileEn = generateHeroSvg(800, 1000, false);

const productsData = [
  { id: 'abaya', titleAr: 'عباية مخمل كشميري مطرزة يدويًا', titleEn: 'Hand-Embroidered Cashmere Velvet Abaya', catAr: 'أزياء فاخرة', catEn: 'Haute Couture', price: '1,850.00', badgeAr: 'إصدار حصري (مرقم)', badgeEn: 'Limited Reserve' },
  { id: 'oud', titleAr: 'عطر العود الملكي المعتّق 100 مل', titleEn: 'Royal Aged Oud Crystal Decanter 100ml', catAr: 'عطور خاصة', catEn: 'Private Blend', price: '1,250.00', badgeAr: 'الأكثر طلباً', badgeEn: 'Bestseller' },
  { id: 'tote', titleAr: 'حقيبة يد هيرمس كلاسيك جلد جملي', titleEn: 'Artisan Bridle Leather Luxury Tote', catAr: 'جلديات فاخرة', catEn: 'Artisan Leather', price: '3,400.00', badgeAr: 'مقتنيات نادرة', badgeEn: 'Private Vault' },
  { id: 'teaset', titleAr: 'طقم شاي وبورسلين ملكي مطلي بذهب 24K', titleEn: 'Imperial 24K Gold Trim Porcelain Tea Set', catAr: 'ديكور ومقتنيات', catEn: 'Imperial Living', price: '980.00', badgeAr: 'حرفي يدوي', badgeEn: 'Handcrafted' },
  { id: 'kaftan', titleAr: 'قفطان حرير طبيعي زمردي منسوج', titleEn: 'Royal Emerald Pure Silk Kaftan', catAr: 'أزياء فاخرة', catEn: 'Haute Couture', price: '2,200.00', badgeAr: 'قطعة وحيدة', badgeEn: 'One of One' },
  { id: 'musk', titleAr: 'مسك الغزال الأبيض الصافي في زجاجة كريستال', titleEn: 'Imperial White Musk Crystal Elixir', catAr: 'عطور خاصة', catEn: 'Private Blend', price: '850.00', badgeAr: 'نادر جداً', badgeEn: 'Collector Grade' },
  { id: 'wallet', titleAr: 'محفظة بطاقات جلد تمساح فاحم', titleEn: 'Alligator Embossed Luxury Card Case', catAr: 'جلديات فاخرة', catEn: 'Artisan Leather', price: '1,150.00', badgeAr: null, badgeEn: null },
  { id: 'mabkhara', titleAr: 'مبخرة نحاس أندلسية منقوشة بالذهب', titleEn: 'Artisan Pierced Brass Incense Burner', catAr: 'ديكور ومقتنيات', catEn: 'Imperial Living', price: '720.00', badgeAr: 'تراث أصيل', badgeEn: 'Heritage Craft' }
];

// Attach self-contained vector SVGs
productsData.forEach(p => {
  p.img = generateProductSvg(p.id, p.catAr, true);
});

// ============================================================================
// 2. SHARED ULTRA-LUXURY CSS SYSTEM (Responsive & RTL/LTR Native)
// ============================================================================

const LUXURY_CSS = `
  :root {
    --lux-bg: #FAF9F6;
    --lux-surface: #FFFFFF;
    --lux-black: #111111;
    --lux-dark: #1C1B1A;
    --lux-gold: #C5A059;
    --lux-gold-light: #F4EAD4;
    --lux-gold-hover: #AF8B43;
    --lux-border: #E8E5DF;
    --lux-border-light: #F0ECE4;
    --lux-text: #1C1B1A;
    --lux-muted: #736E66;
    --font-serif: "Cormorant Garamond", Georgia, "Amiri", serif;
    --font-sans: -apple-system, BlinkMacSystemFont, "Segoe UI", Roboto, "IBM Plex Sans Arabic", sans-serif;
  }
  
  * { box-sizing: border-box; margin: 0; padding: 0; }
  
  body {
    font-family: var(--font-sans);
    background-color: var(--lux-bg);
    color: var(--lux-text);
    line-height: 1.6;
    -webkit-font-smoothing: antialiased;
    min-height: 100vh;
    display: flex;
    flex-direction: column;
    padding-bottom: 72px; /* space for mobile bottom bar */
  }
  @media (min-width: 769px) {
    body { padding-bottom: 0; }
  }

  a { color: inherit; text-decoration: none; }

  /* Skip Link */
  .skip-link {
    position: absolute; top: -100px; left: 1rem; z-index: 10000;
    background: var(--lux-black); color: #fff; padding: 0.5rem 1rem;
    font-size: 0.8rem; font-weight: 600;
  }
  .skip-link:focus { top: 1rem; }

  /* Header */
  header.site-header {
    position: sticky; top: 0; z-index: 1000;
    background: rgba(250, 249, 246, 0.96);
    backdrop-filter: blur(16px);
    border-bottom: 1px solid var(--lux-border);
    height: 72px; display: flex; align-items: center;
  }
  .header-wrap {
    max-width: 1320px; width: 100%; margin: 0 auto; padding: 0 1.5rem;
    display: flex; align-items: center; justify-content: space-between;
  }
  .brand-group { display: flex; align-items: center; gap: 2rem; }
  .brand-logo-wrap { display: flex; align-items: center; gap: 0.75rem; }
  .brand-emblem {
    width: 32px; height: 32px; border: 1.5px solid var(--lux-gold);
    display: flex; align-items: center; justify-content: center;
    font-family: var(--font-serif); font-size: 1.1rem; font-weight: 700; color: var(--lux-gold);
  }
  .brand-logo {
    font-family: var(--font-serif); font-size: 1.5rem; font-weight: 700;
    letter-spacing: -0.02em; color: var(--lux-black); white-space: nowrap;
  }
  
  nav.desktop-nav { display: flex; align-items: center; gap: 1.75rem; }
  nav.desktop-nav a {
    font-size: 0.88rem; font-weight: 500; color: var(--lux-muted);
    transition: color 0.2s; position: relative; padding: 0.5rem 0;
  }
  nav.desktop-nav a:hover, nav.desktop-nav a.active { color: var(--lux-black); font-weight: 600; }
  nav.desktop-nav a.active::after {
    content: ''; position: absolute; bottom: 0; left: 0; right: 0;
    height: 2px; background: var(--lux-gold);
  }

  .header-actions { display: flex; align-items: center; gap: 0.85rem; }
  .btn-lang {
    font-size: 0.75rem; text-transform: uppercase; font-weight: 600;
    padding: 0.35rem 0.65rem; border: 1px solid var(--lux-border); border-radius: 2px;
    background: transparent; cursor: pointer; transition: all 0.2s;
  }
  .btn-lang:hover { border-color: var(--lux-black); }

  .btn-cart-trigger {
    background: none; border: none; cursor: pointer; color: var(--lux-black);
    display: flex; align-items: center; gap: 0.4rem; font-size: 0.82rem; font-weight: 600;
    padding: 0.4rem;
  }
  .badge-count {
    background: var(--lux-gold); color: #000; font-size: 0.65rem; font-weight: 700;
    padding: 0.15rem 0.45rem; border-radius: 99px;
  }
  .btn-account-pill {
    background: var(--lux-black); color: #fff; border: 1px solid var(--lux-black);
    padding: 0.45rem 1rem; font-size: 0.78rem; text-transform: uppercase; letter-spacing: 0.05em;
    border-radius: 2px; font-weight: 600; cursor: pointer; display: flex; align-items: center; gap: 0.4rem;
  }
  .btn-account-pill:hover { background: #000; }

  .mobile-menu-btn {
    display: none; background: none; border: none; cursor: pointer; color: var(--lux-black); padding: 0.3rem;
  }

  /* Slide-out Mobile Navigation Drawer */
  .mobile-nav-overlay {
    position: fixed; inset: 0; background: rgba(0,0,0,0.6); backdrop-filter: blur(4px);
    z-index: 9998; opacity: 0; pointer-events: none; transition: opacity 0.3s ease;
  }
  .mobile-nav-overlay.active { opacity: 1; pointer-events: auto; }
  .mobile-nav-drawer {
    position: fixed; top: 0; bottom: 0; width: 85%; max-width: 320px;
    background: var(--lux-surface); z-index: 9999; display: flex; flex-direction: column;
    box-shadow: 0 0 40px rgba(0,0,0,0.3); transition: transform 0.35s cubic-bezier(0.16, 1, 0.3, 1);
  }
  [dir="rtl"] .mobile-nav-drawer { right: 0; left: auto; transform: translateX(100%); }
  [dir="rtl"] .mobile-nav-drawer.open { transform: translateX(0); }
  [dir="ltr"] .mobile-nav-drawer { left: 0; right: auto; transform: translateX(-100%); }
  [dir="ltr"] .mobile-nav-drawer.open { transform: translateX(0); }

  .mobile-nav-header {
    padding: 1.25rem 1.5rem; border-bottom: 1px solid var(--lux-border);
    display: flex; align-items: center; justify-content: space-between;
  }
  .mobile-nav-links { padding: 1.5rem; display: flex; flex-direction: column; gap: 1.25rem; flex-grow: 1; }
  .mobile-nav-links a {
    font-size: 1rem; font-weight: 500; color: var(--lux-text); display: flex; align-items: center; justify-content: space-between;
    padding-bottom: 0.75rem; border-bottom: 1px solid var(--lux-border-light);
  }
  .mobile-nav-links a.active { color: var(--lux-gold); font-weight: 700; }
  .mobile-nav-footer { padding: 1.5rem; border-top: 1px solid var(--lux-border); background: var(--lux-bg); }

  /* Mobile Bottom Navigation Bar */
  .mobile-bottom-bar {
    display: none; position: fixed; bottom: 0; left: 0; right: 0; z-index: 900;
    height: 64px; background: rgba(255, 255, 255, 0.98); backdrop-filter: blur(12px);
    border-top: 1px solid var(--lux-border);
    grid-template-columns: repeat(5, 1fr); align-items: center; text-align: center;
  }
  .mobile-tab-item {
    display: flex; flex-direction: column; align-items: center; justify-content: center;
    color: var(--lux-muted); font-size: 0.65rem; font-weight: 600; height: 100%; position: relative;
  }
  .mobile-tab-item.active { color: var(--lux-gold); }
  .mobile-tab-item svg { width: 20px; height: 20px; margin-bottom: 2px; }

  @media (max-width: 768px) {
    header.site-header { height: 62px; }
    nav.desktop-nav { display: none; }
    .btn-account-pill { display: none; }
    .mobile-menu-btn { display: block; }
    .mobile-bottom-bar { display: grid; }
    .brand-logo { font-size: 1.25rem; }
  }

  /* Quick-Cart Sliding Drawer */
  .drawer-overlay {
    position: fixed; inset: 0; background: rgba(0,0,0,0.6); backdrop-filter: blur(4px);
    z-index: 9998; opacity: 0; pointer-events: none; transition: opacity 0.3s ease;
  }
  .drawer-overlay.active { opacity: 1; pointer-events: auto; }
  .cart-drawer {
    position: fixed; top: 0; bottom: 0; width: 100%; max-width: 440px;
    background: var(--lux-surface); z-index: 9999; display: flex; flex-direction: column;
    box-shadow: -10px 0 40px rgba(0,0,0,0.25); transition: transform 0.35s cubic-bezier(0.16, 1, 0.3, 1);
  }
  [dir="rtl"] .cart-drawer { left: 0; right: auto; transform: translateX(-100%); }
  [dir="rtl"] .cart-drawer.open { transform: translateX(0); }
  [dir="ltr"] .cart-drawer { right: 0; left: auto; transform: translateX(100%); }
  [dir="ltr"] .cart-drawer.open { transform: translateX(0); }

  .drawer-header {
    padding: 1.5rem; border-bottom: 1px solid var(--lux-border);
    display: flex; align-items: center; justify-content: space-between;
  }
  .drawer-body { padding: 1.5rem; flex-grow: 1; overflow-y: auto; }
  .drawer-footer { padding: 1.5rem; border-top: 1px solid var(--lux-border); background: var(--lux-bg); }

  .free-ship-bar {
    background: var(--lux-gold-light); padding: 0.75rem 1rem; border-radius: 4px;
    margin-bottom: 1rem; font-size: 0.78rem; color: #684E1A; font-weight: 600;
  }
  .ship-track { height: 4px; background: #D9C8A5; border-radius: 2px; margin-top: 0.5rem; overflow: hidden; }
  .ship-progress { height: 100%; width: 100%; background: var(--lux-gold); }

  .cart-item {
    display: flex; gap: 1rem; margin-bottom: 1.25rem; padding-bottom: 1.25rem;
    border-bottom: 1px solid var(--lux-border); align-items: center;
  }
  .cart-item-img {
    width: 72px; height: 96px; object-fit: cover; background: #eee; flex-shrink: 0; border: 1px solid var(--lux-border);
  }
  .qty-ctrl {
    display: inline-flex; border: 1px solid var(--lux-border); align-items: center; margin-top: 0.5rem;
  }
  .qty-ctrl button {
    background: none; border: none; width: 26px; height: 26px; cursor: pointer; font-size: 0.9rem; font-weight: bold;
  }
  .qty-ctrl span { width: 30px; text-align: center; font-size: 0.8rem; font-weight: 600; }

  /* Footer */
  footer {
    background: #0E0D0C; color: #9E9A91; padding: 5rem 1.5rem 2rem;
    margin-top: auto; border-top: 1px solid #242220;
  }
  .footer-inner {
    max-width: 1320px; margin: 0 auto; display: grid; grid-template-columns: 2fr 1fr 1fr 1fr;
    gap: 3rem; margin-bottom: 4rem;
  }
  .footer-inner h4 {
    color: #fff; font-size: 0.85rem; text-transform: uppercase; letter-spacing: 0.1em;
    margin-bottom: 1.25rem; font-weight: 600;
  }
  .footer-inner ul { list-style: none; }
  .footer-inner ul li { margin-bottom: 0.75rem; font-size: 0.85rem; }
  .footer-inner ul li a:hover { color: #fff; }
  .footer-bar {
    max-width: 1320px; margin: 0 auto; padding-top: 2rem; border-top: 1px solid #1C1A18;
    display: flex; justify-content: space-between; font-size: 0.78rem; color: #66635C;
  }
  @media (max-width: 900px) {
    .footer-inner { grid-template-columns: 1fr; gap: 2rem; }
    .footer-bar { flex-direction: column; gap: 1rem; }
  }
`;

// ============================================================================
// 3. UI COMPONENTS HELPERS (Header, Drawer, Mobile Nav, Footer)
// ============================================================================

function getNavigationPaths(pageKey, isRtl) {
  // Bi-directional clean linking table
  const routes = {
    home: { ar: 'index.html', en: 'preview-en.html' },
    cat: { ar: 'categories.html', en: 'categories-en.html' },
    prod: { ar: 'product.html', en: 'product-en.html' },
    cart: { ar: 'cart.html', en: 'cart-en.html' },
    track: { ar: 'tracking.html', en: 'tracking-en.html' },
    acc: { ar: 'account.html', en: 'account-en.html' }
  };

  const currentRoutes = routes[pageKey] || routes.home;
  const langTarget = isRtl ? currentRoutes.en : currentRoutes.ar;

  return {
    routes,
    langTarget,
    homeHref: isRtl ? routes.home.ar : routes.home.en,
    catHref: isRtl ? routes.cat.ar : routes.cat.en,
    prodHref: isRtl ? routes.prod.ar : routes.prod.en,
    cartHref: isRtl ? routes.cart.ar : routes.cart.en,
    trackHref: isRtl ? routes.track.ar : routes.track.en,
    accHref: isRtl ? routes.acc.ar : routes.acc.en
  };
}

function getHeader(activeTab, isRtl) {
  const p = getNavigationPaths(activeTab, isRtl);

  const t = isRtl ? {
    brand: "دار النخبة", home: "الرئيسية", cat: "المجموعات الخاصة",
    prod: "القطع المميزة", track: "تتبع الطلبات", cart: "السلة",
    acc: "حسابي (VIP)", lang: "English", skip: "الانتقال إلى المحتوى"
  } : {
    brand: "ELITE MAISON", home: "Home", cat: "Collections",
    prod: "Exclusives", track: "Track Order", cart: "Cart",
    acc: "VIP Account", lang: "عربي", skip: "Skip to content"
  };

  return `
  <a href="#main" class="skip-link">${t.skip}</a>
  <header role="banner" class="site-header">
    <div class="header-wrap">
      <div class="brand-group">
        <button class="mobile-menu-btn" onclick="openMobileNav()" aria-label="Toggle Navigation">
          <svg width="24" height="24" fill="none" stroke="currentColor" viewBox="0 0 24 24"><path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M4 6h16M4 12h16M4 18h16"/></svg>
        </button>
        <a href="${p.homeHref}" class="brand-logo-wrap">
          <div class="brand-emblem">EM</div>
          <span class="brand-logo">${t.brand}</span>
        </a>
        <nav class="desktop-nav">
          <a href="${p.homeHref}" class="${activeTab === 'home' ? 'active' : ''}">${t.home}</a>
          <a href="${p.catHref}" class="${activeTab === 'cat' ? 'active' : ''}">${t.cat}</a>
          <a href="${p.prodHref}" class="${activeTab === 'prod' ? 'active' : ''}">${t.prod}</a>
          <a href="${p.trackHref}" class="${activeTab === 'track' ? 'active' : ''}">${t.track}</a>
        </nav>
      </div>

      <div class="header-actions">
        <a href="${p.langTarget}" class="btn-lang">${t.lang}</a>
        <button class="btn-cart-trigger" onclick="openCart()" aria-label="${t.cart}">
          <svg width="20" height="20" fill="none" stroke="currentColor" viewBox="0 0 24 24"><path stroke-linecap="round" stroke-linejoin="round" stroke-width="1.8" d="M16 11V7a4 4 0 00-8 0v4M5 9h14l1 12H4L5 9z"/></svg>
          <span class="badge-count" id="headerCartCount">2</span>
        </button>
        <a href="${p.accHref}" class="btn-account-pill">
          <svg width="15" height="15" fill="none" stroke="currentColor" viewBox="0 0 24 24"><path stroke-linecap="round" stroke-linejoin="round" stroke-width="1.8" d="M16 7a4 4 0 11-8 0 4 4 0 018 0zM12 14a7 7 0 00-7 7h14a7 7 0 00-7-7z"/></svg>
          <span>${t.acc}</span>
        </a>
      </div>
    </div>
  </header>
  `;
}

function getMobileElements(activeTab, isRtl) {
  const p = getNavigationPaths(activeTab, isRtl);

  const t = isRtl ? {
    home: "الرئيسية", cat: "المجموعات", prod: "المميزة", cart: "السلة", track: "التتبع", acc: "حسابي"
  } : {
    home: "Home", cat: "Catalog", prod: "Featured", cart: "Cart", track: "Track", acc: "Account"
  };

  return `
  <!-- Mobile Slide Navigation Drawer -->
  <div class="mobile-nav-overlay" id="mobileNavOverlay" onclick="closeMobileNav()"></div>
  <aside class="mobile-nav-drawer" id="mobileNavDrawer" aria-label="Mobile Navigation">
    <div class="mobile-nav-header">
      <span class="brand-logo" style="font-size:1.2rem;">${isRtl ? 'دار النخبة' : 'ELITE MAISON'}</span>
      <button onclick="closeMobileNav()" style="background:none; border:none; font-size:1.6rem; cursor:pointer;">&times;</button>
    </div>
    <div class="mobile-nav-links">
      <a href="${p.homeHref}" class="${activeTab === 'home' ? 'active' : ''}">
        <span>${t.home}</span>
        <span>&larr;</span>
      </a>
      <a href="${p.catHref}" class="${activeTab === 'cat' ? 'active' : ''}">
        <span>${t.cat}</span>
        <span>&larr;</span>
      </a>
      <a href="${p.prodHref}" class="${activeTab === 'prod' ? 'active' : ''}">
        <span>${t.prod}</span>
        <span>&larr;</span>
      </a>
      <a href="${p.cartHref}" class="${activeTab === 'cart' ? 'active' : ''}">
        <span>${t.cart}</span>
        <span>&larr;</span>
      </a>
      <a href="${p.trackHref}" class="${activeTab === 'track' ? 'active' : ''}">
        <span>${t.track}</span>
        <span>&larr;</span>
      </a>
      <a href="${p.accHref}" class="${activeTab === 'acc' ? 'active' : ''}">
        <span>${t.acc}</span>
        <span>&larr;</span>
      </a>
    </div>
    <div class="mobile-nav-footer">
      <a href="${p.langTarget}" class="btn-lang" style="display:block; text-align:center; padding:0.6rem;">
        ${isRtl ? 'Switch to English' : 'التحويل إلى اللغة العربية'}
      </a>
    </div>
  </aside>

  <!-- Mobile Bottom Tab Bar -->
  <nav class="mobile-bottom-bar" aria-label="Mobile Tab Bar">
    <a href="${p.homeHref}" class="mobile-tab-item ${activeTab === 'home' ? 'active' : ''}">
      <svg fill="none" stroke="currentColor" viewBox="0 0 24 24"><path stroke-linecap="round" stroke-linejoin="round" stroke-width="1.8" d="M3 12l2-2m0 0l7-7 7 7M5 10v10a1 1 0 001 1h3m10-11l2 2m-2-2v10a1 1 0 01-1 1h-3m-6 0a1 1 0 001-1v-4a1 1 0 011-1h2a1 1 0 011 1v4a1 1 0 001 1m-6 0h6"/></svg>
      <span>${t.home}</span>
    </a>
    <a href="${p.catHref}" class="mobile-tab-item ${activeTab === 'cat' ? 'active' : ''}">
      <svg fill="none" stroke="currentColor" viewBox="0 0 24 24"><path stroke-linecap="round" stroke-linejoin="round" stroke-width="1.8" d="M4 6a2 2 0 012-2h2a2 2 0 012 2v2a2 2 0 01-2 2H6a2 2 0 01-2-2V6zM14 6a2 2 0 012-2h2a2 2 0 012 2v2a2 2 0 01-2 2h-2a2 2 0 01-2-2V6zM4 16a2 2 0 012-2h2a2 2 0 012 2v2a2 2 0 01-2 2H6a2 2 0 01-2-2v-2zM14 16a2 2 0 012-2h2a2 2 0 012 2v2a2 2 0 01-2 2h-2a2 2 0 01-2-2v-2z"/></svg>
      <span>${t.cat}</span>
    </a>
    <a href="javascript:void(0)" onclick="openCart()" class="mobile-tab-item ${activeTab === 'cart' ? 'active' : ''}">
      <svg fill="none" stroke="currentColor" viewBox="0 0 24 24"><path stroke-linecap="round" stroke-linejoin="round" stroke-width="1.8" d="M16 11V7a4 4 0 00-8 0v4M5 9h14l1 12H4L5 9z"/></svg>
      <span>${t.cart}</span>
    </a>
    <a href="${p.trackHref}" class="mobile-tab-item ${activeTab === 'track' ? 'active' : ''}">
      <svg fill="none" stroke="currentColor" viewBox="0 0 24 24"><path stroke-linecap="round" stroke-linejoin="round" stroke-width="1.8" d="M9 12l2 2 4-4m5.618-4.016A11.955 11.955 0 0112 2.944a11.955 11.955 0 01-8.618 3.04A12.02 12.02 0 003 9c0 5.591 3.824 10.29 9 11.622 5.176-1.332 9-6.03 9-11.622 0-1.042-.133-2.052-.382-3.016z"/></svg>
      <span>${t.track}</span>
    </a>
    <a href="${p.accHref}" class="mobile-tab-item ${activeTab === 'acc' ? 'active' : ''}">
      <svg fill="none" stroke="currentColor" viewBox="0 0 24 24"><path stroke-linecap="round" stroke-linejoin="round" stroke-width="1.8" d="M16 7a4 4 0 11-8 0 4 4 0 018 0zM12 14a7 7 0 00-7 7h14a7 7 0 00-7-7z"/></svg>
      <span>${t.acc}</span>
    </a>
  </nav>
  `;
}

function getDrawer(isRtl) {
  const p = getNavigationPaths('home', isRtl);
  const p1 = productsData[0];
  const p2 = productsData[1];

  return `
  <div class="drawer-overlay" id="drawerOverlay" onclick="closeCart()"></div>
  <aside class="cart-drawer" id="cartDrawer" aria-label="Quick Cart">
    <div class="drawer-header">
      <h3 style="font-family: var(--font-serif); font-size: 1.25rem;">${isRtl ? 'سلة المقتنيات (2)' : 'Shopping Cart (2)'}</h3>
      <button onclick="closeCart()" style="background:none; border:none; font-size:1.5rem; cursor:pointer;">&times;</button>
    </div>
    <div class="drawer-body">
      <div class="free-ship-bar">
        <span>${isRtl ? 'مؤهل للشحن الفاخر المجاني المؤمن' : 'Complimentary Insured Shipping Applied'}</span>
        <div class="ship-track"><div class="ship-progress"></div></div>
      </div>
      <div class="cart-item">
        <img src="${p1.img}" class="cart-item-img" alt="${isRtl ? p1.titleAr : p1.titleEn}">
        <div style="flex-grow:1;">
          <h4 style="font-size:0.9rem;">${isRtl ? p1.titleAr : p1.titleEn}</h4>
          <span style="font-size:0.75rem; color:var(--lux-muted);">${isRtl ? 'المقاس: 54 M | إصدار حصري' : 'Size: 54 M | Limited'}</span>
          <div style="font-size:0.9rem; font-weight:700; margin-top:0.25rem;">1,850.00 SAR</div>
          <div class="qty-ctrl">
            <button onclick="updateDrawerQty(-1)">-</button>
            <span id="drawerQty1">1</span>
            <button onclick="updateDrawerQty(1)">+</button>
          </div>
        </div>
        <button style="background:none; border:none; color:#c00; cursor:pointer;" onclick="this.closest('.cart-item').remove()">🗑️</button>
      </div>
      <div class="cart-item">
        <img src="${p2.img}" class="cart-item-img" alt="${isRtl ? p2.titleAr : p2.titleEn}">
        <div style="flex-grow:1;">
          <h4 style="font-size:0.9rem;">${isRtl ? p2.titleAr : p2.titleEn}</h4>
          <span style="font-size:0.75rem; color:var(--lux-muted);">${isRtl ? 'حجم: 100 مل | أصلي 100%' : '100ml | Pure Extract'}</span>
          <div style="font-size:0.9rem; font-weight:700; margin-top:0.25rem;">1,250.00 SAR</div>
          <div class="qty-ctrl">
            <button onclick="updateDrawerQty(-1)">-</button>
            <span id="drawerQty2">1</span>
            <button onclick="updateDrawerQty(1)">+</button>
          </div>
        </div>
        <button style="background:none; border:none; color:#c00; cursor:pointer;" onclick="this.closest('.cart-item').remove()">🗑️</button>
      </div>
    </div>
    <div class="drawer-footer">
      <div style="display:flex; justify-content:space-between; font-size:0.85rem; color:var(--lux-muted); margin-bottom:0.4rem;">
        <span>${isRtl ? 'المجموع الفرعي' : 'Subtotal'}</span>
        <span id="drawerSubtotalTxt">3,100.00 SAR</span>
      </div>
      <div style="display:flex; justify-content:space-between; font-size:1.1rem; font-weight:700; color:var(--lux-black); margin-bottom:1.25rem;">
        <span>${isRtl ? 'الإجمالي الشامل (VAT)' : 'Total (incl. VAT)'}</span>
        <span style="color:var(--lux-gold);" id="drawerTotalTxt">3,100.00 SAR</span>
      </div>
      <a href="${p.cartHref}" style="display:block; text-align:center; padding:0.9rem; background:#000; color:#fff; font-weight:600; font-size:0.85rem; text-transform:uppercase; letter-spacing:0.08em; margin-bottom:0.5rem;">
        ${isRtl ? 'معاينة السلة الكاملة' : 'View Full Cart'}
      </a>
      <a href="https://salla.sa" target="_blank" style="display:block; text-align:center; padding:0.9rem; background:var(--lux-gold); color:#000; font-weight:700; font-size:0.85rem; text-transform:uppercase; letter-spacing:0.08em;">
        ${isRtl ? 'إتمام الطلب عبر سلة برو' : 'Checkout with Salla Pro'}
      </a>
    </div>
  </aside>

  <script>
    function openCart() {
      document.getElementById('drawerOverlay').classList.add('active');
      document.getElementById('cartDrawer').classList.add('open');
    }
    function closeCart() {
      document.getElementById('drawerOverlay').classList.remove('active');
      document.getElementById('cartDrawer').classList.remove('open');
    }
    function openMobileNav() {
      document.getElementById('mobileNavOverlay').classList.add('active');
      document.getElementById('mobileNavDrawer').classList.add('open');
    }
    function closeMobileNav() {
      document.getElementById('mobileNavOverlay').classList.remove('active');
      document.getElementById('mobileNavDrawer').classList.remove('open');
    }
    function updateDrawerQty(delta) {
      const q = document.getElementById('drawerQty1');
      if (!q) return;
      let val = parseInt(q.innerText) + delta;
      if (val < 1) val = 1;
      q.innerText = val;
      const total = (1850 * val + 1250).toLocaleString('en-US', { minimumFractionDigits: 2 });
      document.getElementById('drawerSubtotalTxt').innerText = total + ' SAR';
      document.getElementById('drawerTotalTxt').innerText = total + ' SAR';
    }
  </script>
  `;
}

function getFooter(isRtl) {
  const p = getNavigationPaths('home', isRtl);

  return `
  <footer>
    <div class="footer-inner">
      <div>
        <div class="brand-logo-wrap" style="margin-bottom:1rem;">
          <div class="brand-emblem">EM</div>
          <span class="brand-logo" style="color:#fff; font-size:1.3rem;">${isRtl ? 'دار النخبة الفاخرة' : 'ELITE MAISON'}</span>
        </div>
        <p style="font-size:0.85rem; line-height:1.8; max-width:360px; color:#A8A49C;">
          ${isRtl ? 'بوتيك سعودي رفيع المستوى مصمم ومبني وفق أرقى معايير الفخامة العالمية على منصة سلة برو بواسطة شركاء سalla المعتمدين.' : 'A premier Saudi luxury boutique engineered to the highest global standards on Salla Pro by certified Salla Partners.'}
        </p>
        <div style="margin-top:1.25rem; font-size:0.75rem; color:#888;">
          ${isRtl ? 'السجل التجاري: 1010892014 | الرقم الضريبي: 301294829100003' : 'CR: 1010892014 | VAT ID: 301294829100003'}
        </div>
      </div>
      <div>
        <h4>${isRtl ? 'التسوق والاستكشاف' : 'Explore Boutique'}</h4>
        <ul>
          <li><a href="${p.homeHref}">${isRtl ? 'الرئيسية' : 'Home'}</a></li>
          <li><a href="${p.catHref}">${isRtl ? 'المجموعات الخاصة' : 'Private Reserve'}</a></li>
          <li><a href="${p.prodHref}">${isRtl ? 'القطع الأكثر طلباً' : 'Bestsellers'}</a></li>
          <li><a href="${p.cartHref}">${isRtl ? 'سلة المشتريات' : 'Shopping Cart'}</a></li>
        </ul>
      </div>
      <div>
        <h4>${isRtl ? 'خدمة العملاء والطلبات' : 'Client Concierge'}</h4>
        <ul>
          <li><a href="${p.trackHref}">${isRtl ? 'تتبع الشحنة الفاخرة' : 'Track Consignment'}</a></li>
          <li><a href="${p.accHref}">${isRtl ? 'حسابي والعضوية' : 'VIP Account'}</a></li>
          <li><a href="javascript:void(0)">${isRtl ? 'الشحن والتوصيل المصفح' : 'Insured Delivery'}</a></li>
          <li><a href="javascript:void(0)">${isRtl ? 'سياسة الاستبدال والضمان' : 'Returns & Warranty'}</a></li>
        </ul>
      </div>
      <div>
        <h4>${isRtl ? 'الدفع والأمان والاعتماد' : 'Payments & Compliance'}</h4>
        <p style="font-size:0.8rem; margin-bottom:1rem; color:#A8A49C;">
          ${isRtl ? 'معاملات مشفرة 100% معتمدة من البنك المركزي السعودي (ساما) عبر بوابة سلة.' : '100% encrypted & SAMA approved via Salla Payments.'}
        </p>
        <div style="font-size:0.8rem; color:#D4AF37; font-weight:600; line-height:1.8;">
          Mada &bull; Visa &bull; Mastercard &bull; Apple Pay &bull; Tamara &bull; Tabby
        </div>
      </div>
    </div>
    <div class="footer-bar">
      <span>&copy; 2026 ${isRtl ? 'دار النخبة الفاخرة. جميع الحقوق محفوظة.' : 'Elite Maison. All Rights Reserved.'}</span>
      <span>Certified Salla Pro Partner Theme &bull; Twilight Engine</span>
    </div>
  </footer>
  `;
}

// ============================================================================
// 4. MASTER PAGE BUILDERS
// ============================================================================

// 1. Home Page Builder
function buildHomePage(isRtl) {
  const p = getNavigationPaths('home', isRtl);
  const heroImg = isRtl ? heroImgDesktopAr : heroImgDesktopEn;
  const heroImgMob = isRtl ? heroImgMobileAr : heroImgMobileEn;

  return `<!DOCTYPE html>
<html lang="${isRtl ? 'ar' : 'en'}" dir="${isRtl ? 'rtl' : 'ltr'}">
<head>
  <meta charset="UTF-8">
  <meta name="viewport" content="width=device-width, initial-scale=1.0">
  <title>${isRtl ? 'دار النخبة الفاخرة | المتجر الرسمي المعتمد' : 'Elite Maison | Official Luxury Boutique'}</title>
  <style>
    ${LUXURY_CSS}
    
    /* Hero Banner 2.0 */
    .hero-section {
      position: relative; width: 100%; min-height: 600px;
      display: flex; align-items: center; justify-content: center;
      overflow: hidden; background: #0E0D0C;
    }
    .hero-bg-picture, .hero-bg-picture img {
      position: absolute; inset: 0; width: 100%; height: 100%; object-fit: cover;
    }
    .hero-overlay {
      position: absolute; inset: 0; background: rgba(14, 13, 12, 0.45);
    }
    .hero-content {
      position: relative; z-index: 10; max-width: 820px; margin: 0 auto;
      padding: 4rem 1.5rem; text-align: center; color: #fff;
    }
    .hero-eyebrow {
      display: inline-block; font-size: 0.8rem; text-transform: uppercase;
      letter-spacing: 0.15em; color: var(--lux-gold); font-weight: 700; margin-bottom: 1.25rem;
    }
    .hero-title {
      font-family: var(--font-serif); font-size: 3.5rem; font-weight: 700;
      line-height: 1.15; margin-bottom: 1.25rem; text-shadow: 0 4px 20px rgba(0,0,0,0.6);
    }
    .hero-subtitle {
      font-size: 1.1rem; line-height: 1.8; color: #E5E2DC; max-width: 640px; margin: 0 auto 2.5rem;
    }
    .hero-cta {
      display: inline-flex; align-items: center; gap: 0.75rem;
      padding: 1.1rem 2.5rem; background: var(--lux-gold); color: #000;
      font-weight: 700; font-size: 0.88rem; text-transform: uppercase; letter-spacing: 0.1em;
      border: none; cursor: pointer; transition: background 0.2s;
    }
    .hero-cta:hover { background: #dfc488; }

    /* Trust Invariants Strip */
    .trust-strip {
      background: var(--lux-surface); border-bottom: 1px solid var(--lux-border);
      padding: 1.5rem 1rem;
    }
    .trust-wrap {
      max-width: 1320px; margin: 0 auto; display: grid; grid-template-columns: repeat(4, 1fr);
      gap: 1.5rem; text-align: center;
    }
    .trust-item h4 { font-size: 0.85rem; font-weight: 700; margin-bottom: 0.2rem; color: var(--lux-black); }
    .trust-item p { font-size: 0.75rem; color: var(--lux-muted); }

    /* Category Blocks */
    .section-wrap { max-width: 1320px; margin: 5rem auto; padding: 0 1.5rem; }
    .section-header {
      display: flex; justify-content: space-between; align-items: flex-end;
      margin-bottom: 2.5rem; padding-bottom: 1rem; border-bottom: 1px solid var(--lux-border);
    }
    .section-title { font-family: var(--font-serif); font-size: 2.2rem; font-weight: 700; color: var(--lux-black); }
    .section-subtitle { font-size: 0.88rem; color: var(--lux-muted); margin-top: 0.25rem; }
    .view-all-link { font-size: 0.85rem; font-weight: 600; color: var(--lux-black); }

    .category-grid { display: grid; grid-template-columns: repeat(3, 1fr); gap: 2rem; }
    .category-card {
      position: relative; height: 320px; overflow: hidden; background: #222;
      display: flex; flex-direction: column; justify-content: flex-end; padding: 2rem;
      border: 1px solid var(--lux-border); transition: transform 0.3s;
    }
    .category-card:hover { transform: translateY(-4px); }
    .category-card img {
      position: absolute; inset: 0; width: 100%; height: 100%; object-fit: cover; opacity: 0.6;
      transition: transform 0.6s ease;
    }
    .category-card:hover img { transform: scale(1.05); opacity: 0.75; }
    .category-card-content { position: relative; z-index: 2; color: #fff; }
    .category-card-content h3 { font-family: var(--font-serif); font-size: 1.5rem; margin-bottom: 0.25rem; }

    /* Featured Products Grid */
    .product-grid { display: grid; grid-template-columns: repeat(4, 1fr); gap: 2rem; }
    .product-card {
      background: var(--lux-surface); border: 1px solid var(--lux-border);
      display: flex; flex-direction: column; transition: all 0.3s cubic-bezier(0.16, 1, 0.3, 1);
    }
    .product-card:hover { transform: translateY(-4px); box-shadow: 0 16px 32px rgba(0,0,0,0.06); border-color: var(--lux-gold); }
    .card-img-wrap { position: relative; aspect-ratio: 3/4; overflow: hidden; background: #eee; }
    .card-img-wrap img { width: 100%; height: 100%; object-fit: cover; transition: transform 0.6s ease; }
    .product-card:hover .card-img-wrap img { transform: scale(1.04); }
    .card-badge {
      position: absolute; top: 0.75rem; ${isRtl ? 'right' : 'left'}: 0.75rem;
      background: #000; color: var(--lux-gold); font-size: 0.65rem; font-weight: 700;
      padding: 0.25rem 0.6rem; text-transform: uppercase;
    }
    .card-body { padding: 1.25rem; display: flex; flex-direction: column; flex-grow: 1; justify-content: space-between; }
    .card-body h3 { font-size: 0.95rem; margin-bottom: 0.3rem; font-weight: 600; line-height: 1.4; }
    .card-foot {
      display: flex; justify-content: space-between; align-items: center; padding-top: 1rem; border-top: 1px solid var(--lux-border);
    }
    .btn-card-add {
      background: var(--lux-black); color: #fff; border: none; padding: 0.5rem 0.9rem;
      font-size: 0.78rem; font-weight: 600; cursor: pointer; border-radius: 2px;
    }
    .btn-card-add:hover { background: #000; }

    @media (max-width: 900px) {
      .hero-title { font-size: 2.3rem; }
      .trust-wrap { grid-template-columns: repeat(2, 1fr); }
      .category-grid { grid-template-columns: 1fr; }
      .product-grid { grid-template-columns: repeat(2, 1fr); }
    }
    @media (max-width: 600px) {
      .product-grid { grid-template-columns: 1fr; }
      .trust-wrap { grid-template-columns: 1fr; }
    }
  </style>
</head>
<body>
  ${getHeader('home', isRtl)}

  <main id="main">
    <!-- Hero Banner 2.0 -->
    <section class="hero-section">
      <picture class="hero-bg-picture">
        <source media="(min-width: 768px)" srcset="${heroImg}">
        <source media="(max-width: 767px)" srcset="${heroImgMob}">
        <img src="${heroImg}" alt="Elite Maison Luxury Reserve">
      </picture>
      <div class="hero-overlay"></div>
      <div class="hero-content">
        <span class="hero-eyebrow">${isRtl ? 'تشكيلة الشتاء الحصرية | إصدار محدود' : 'Winter 2026 Private Reserve'}</span>
        <h1 class="hero-title">${isRtl ? 'الأناقة في أبهى صورها والتفرد الذي يليق بك' : 'Timeless Luxury, Crafted to Perfection'}</h1>
        <p class="hero-subtitle">${isRtl ? 'مقتنيات نادرة صُممت بحرفية متناهية لتلبي ذوق النخبة الباحثين عن الأصالة المطلقة والتفرد.' : 'Handpicked rare pieces designed for discerning connoisseurs who appreciate pure craftsmanship.'}</p>
        <a href="${p.catHref}" class="hero-cta">
          <span>${isRtl ? 'استكشف التشكيلة الخاصة' : 'Explore Reserve'}</span>
          <span>&larr;</span>
        </a>
      </div>
    </section>

    <!-- Trust Invariants Strip -->
    <section class="trust-strip">
      <div class="trust-wrap">
        <div class="trust-item">
          <h4>${isRtl ? 'حرفية يدوية معتمدة' : 'Master Craftsmanship'}</h4>
          <p>${isRtl ? 'صُنع بحب في الرياض وإيطاليا' : 'Artisan crafted in Riyadh & Italy'}</p>
        </div>
        <div class="trust-item">
          <h4>${isRtl ? 'شحن مصفح ومؤمن' : 'Insured Express Courier'}</h4>
          <p>${isRtl ? 'توصيل خلال 24-48 ساعة عبر سمسا' : 'Delivered in 24-48 hrs via SMSA'}</p>
        </div>
        <div class="trust-item">
          <h4>${isRtl ? 'تقسيط ميسر 0% فوائد' : 'Interest-Free Installments'}</h4>
          <p>${isRtl ? 'قسّم على 4 دفعات مع تمارا وتابي' : 'Split in 4 via Tamara & Tabby'}</p>
        </div>
        <div class="trust-item">
          <h4>${isRtl ? 'منصة سلة برو المعتمدة' : 'Certified Salla Pro Store'}</h4>
          <p>${isRtl ? 'معاملات آمنة ومشفرة 100%' : '100% secure checkout'}</p>
        </div>
      </div>
    </section>

    <!-- Curated Categories -->
    <section class="section-wrap">
      <div class="section-header">
        <div>
          <h2 class="section-title">${isRtl ? 'المجموعات الحصرية' : 'Curated Collections'}</h2>
          <p class="section-subtitle">${isRtl ? 'تصفح تشكيلاتنا المصممة وفق أرقى معايير الجودة' : 'Explore signature categories refined for elegance'}</p>
        </div>
        <a href="${p.catHref}" class="view-all-link">${isRtl ? 'عرض كافة المجموعات &larr;' : 'View All &rarr;'}</a>
      </div>
      <div class="category-grid">
        <a href="${p.catHref}" class="category-card">
          <img src="${productsData[0].img}" alt="Couture">
          <div class="category-card-content">
            <h3>${isRtl ? 'الأزياء والعبايات الفاخرة' : 'Haute Couture & Abayas'}</h3>
            <span style="font-size:0.8rem; color:var(--lux-gold); font-weight:600;">${isRtl ? '4 قطع حصرية' : '4 Pieces'}</span>
          </div>
        </a>
        <a href="${p.catHref}" class="category-card">
          <img src="${productsData[1].img}" alt="Fragrance">
          <div class="category-card-content">
            <h3>${isRtl ? 'العطور الملكية والدهن' : 'Royal Fragrance & Oud'}</h3>
            <span style="font-size:0.8rem; color:var(--lux-gold); font-weight:600;">${isRtl ? '2 عطور نادرة' : '2 Blends'}</span>
          </div>
        </a>
        <a href="${p.catHref}" class="category-card">
          <img src="${productsData[2].img}" alt="Leather">
          <div class="category-card-content">
            <h3>${isRtl ? 'المقتنيات الجلدية والتحف' : 'Artisan Leather & Living'}</h3>
            <span style="font-size:0.8rem; color:var(--lux-gold); font-weight:600;">${isRtl ? '2 مقتنيات نادرة' : '2 Pieces'}</span>
          </div>
        </a>
      </div>
    </section>

    <!-- Featured Products -->
    <section class="section-wrap" style="margin-top:2rem;">
      <div class="section-header">
        <div>
          <h2 class="section-title">${isRtl ? 'القطع الأكثر تميزاً' : 'Private Reserve Exclusives'}</h2>
          <p class="section-subtitle">${isRtl ? 'مختارات الموسم الأكثر طلباً واقتناءً' : 'Most coveted collector releases of the season'}</p>
        </div>
        <a href="${p.catHref}" class="view-all-link">${isRtl ? 'تصفح المتجر بالكامل &larr;' : 'Explore All &rarr;'}</a>
      </div>
      <div class="product-grid">
        ${productsData.slice(0, 4).map(pItem => `
          <article class="product-card">
            <div class="card-img-wrap">
              <a href="${p.prodHref}"><img src="${pItem.img}" alt="${isRtl ? pItem.titleAr : pItem.titleEn}"></a>
              ${pItem.badgeAr ? `<span class="card-badge">${isRtl ? pItem.badgeAr : pItem.badgeEn}</span>` : ''}
            </div>
            <div class="card-body">
              <div>
                <span style="font-size:0.7rem; text-transform:uppercase; color:var(--lux-gold); font-weight:700;">${isRtl ? pItem.catAr : pItem.catEn}</span>
                <h3 style="margin-top:0.25rem;"><a href="${p.prodHref}">${isRtl ? pItem.titleAr : pItem.titleEn}</a></h3>
              </div>
              <div class="card-foot">
                <span style="font-weight:700; font-size:0.95rem;">${pItem.price} SAR</span>
                <button class="btn-card-add" onclick="openCart()">${isRtl ? 'إضافة للسلة' : 'Add to Bag'}</button>
              </div>
            </div>
          </article>
        `).join('')}
      </div>
    </section>
  </main>

  ${getFooter(isRtl)}
  ${getDrawer(isRtl)}
  ${getMobileElements('home', isRtl)}
</body>
</html>`;
}

// 2. Categories Page Builder
function buildCategoriesPage(isRtl) {
  const p = getNavigationPaths('cat', isRtl);

  return `<!DOCTYPE html>
<html lang="${isRtl ? 'ar' : 'en'}" dir="${isRtl ? 'rtl' : 'ltr'}">
<head>
  <meta charset="UTF-8">
  <meta name="viewport" content="width=device-width, initial-scale=1.0">
  <title>${isRtl ? 'المجموعات الخاصة | دار النخبة' : 'Private Reserve Collections | Elite Maison'}</title>
  <style>
    ${LUXURY_CSS}
    .catalog-hero {
      background: #141312; color: #fff; padding: 4.5rem 1.5rem; text-align: center;
      border-bottom: 1px solid var(--lux-border);
    }
    .catalog-hero h1 { font-family: var(--font-serif); font-size: 2.8rem; margin-bottom: 0.5rem; color: #fff; }
    .catalog-hero p { color: #BBB7AD; font-size: 1rem; max-width: 600px; margin: 0 auto; }

    .catalog-layout {
      max-width: 1320px; margin: 3rem auto; padding: 0 1.5rem;
      display: grid; grid-template-columns: 260px 1fr; gap: 3rem;
    }
    .filter-box {
      background: var(--lux-surface); border: 1px solid var(--lux-border); padding: 1.5rem;
      border-radius: 2px; position: sticky; top: 90px;
    }
    .filter-box h3 { font-size: 0.95rem; text-transform: uppercase; letter-spacing: 0.05em; margin-bottom: 1.25rem; font-weight:700; }
    .filter-group { margin-bottom: 1.5rem; padding-bottom: 1.25rem; border-bottom: 1px solid var(--lux-border); }
    .filter-group h4 { font-size: 0.8rem; text-transform: uppercase; color: var(--lux-muted); margin-bottom: 0.75rem; font-weight:600; }
    .filter-item { display: flex; align-items: center; gap: 0.5rem; font-size: 0.85rem; margin-bottom: 0.5rem; cursor: pointer; }
    
    .toolbar {
      display: flex; justify-content: space-between; align-items: center;
      margin-bottom: 2rem; padding-bottom: 1rem; border-bottom: 1px solid var(--lux-border);
    }
    .select-sort {
      padding: 0.5rem 1rem; border: 1px solid var(--lux-border); background: #fff;
      font-size: 0.85rem; border-radius: 2px;
    }
    .product-grid {
      display: grid; grid-template-columns: repeat(3, 1fr); gap: 2rem;
    }
    .product-card {
      background: var(--lux-surface); border: 1px solid var(--lux-border);
      display: flex; flex-direction: column; transition: all 0.3s cubic-bezier(0.16, 1, 0.3, 1);
    }
    .product-card:hover { transform: translateY(-4px); box-shadow: 0 16px 32px rgba(0,0,0,0.06); border-color: var(--lux-gold); }
    .card-img-wrap { position: relative; aspect-ratio: 3/4; overflow: hidden; background: #eee; }
    .card-img-wrap img { width: 100%; height: 100%; object-fit: cover; transition: transform 0.6s ease; }
    .product-card:hover .card-img-wrap img { transform: scale(1.05); }
    .badge {
      position: absolute; top: 0.75rem; ${isRtl ? 'right' : 'left'}: 0.75rem;
      background: #000; color: var(--lux-gold); font-size: 0.65rem; font-weight: 700;
      padding: 0.25rem 0.6rem; text-transform: uppercase;
    }
    .card-info { padding: 1.25rem; display: flex; flex-direction: column; flex-grow: 1; justify-content: space-between; }
    .card-info h3 { font-size: 0.95rem; margin-bottom: 0.3rem; font-weight: 600; line-height: 1.4; }
    .card-bottom {
      display: flex; justify-content: space-between; align-items: center; padding-top: 1rem; border-top: 1px solid var(--lux-border);
    }
    .btn-add {
      background: var(--lux-black); color: #fff; border: none; padding: 0.5rem 0.9rem;
      font-size: 0.78rem; font-weight: 600; cursor: pointer; border-radius: 2px;
    }
    .btn-add:hover { background: #000; }

    @media (max-width: 900px) {
      .catalog-layout { grid-template-columns: 1fr; }
      .filter-box { display: none; }
      .product-grid { grid-template-columns: repeat(2, 1fr); }
    }
    @media (max-width: 600px) {
      .product-grid { grid-template-columns: 1fr; }
    }
  </style>
</head>
<body>
  ${getHeader('cat', isRtl)}
  
  <div class="catalog-hero">
    <h1>${isRtl ? 'المجموعات الخاصة | Private Reserve' : 'Private Reserve Collections'}</h1>
    <p>${isRtl ? 'قطع نادرة صُممت بحرفية متناهية لتلبي ذوق النخبة الباحثين عن التفرد.' : 'Rare pieces crafted with exceptional precision for discerning collectors.'}</p>
  </div>

  <main class="catalog-layout" id="main">
    <aside class="filter-box">
      <h3>${isRtl ? 'تصفية المنتجات' : 'Refine Catalog'}</h3>
      <div class="filter-group">
        <h4>${isRtl ? 'التصنيف' : 'Category'}</h4>
        <label class="filter-item"><input type="checkbox" checked> ${isRtl ? 'الأزياء والعبايات الفاخرة' : 'Couture & Abayas'} (4)</label>
        <label class="filter-item"><input type="checkbox" checked> ${isRtl ? 'العطور الملكية والدهن' : 'Royal Fragrances'} (2)</label>
        <label class="filter-item"><input type="checkbox" checked> ${isRtl ? 'المقتنيات الجلدية' : 'Artisan Leather'} (1)</label>
        <label class="filter-item"><input type="checkbox" checked> ${isRtl ? 'الديكور والمقتنيات' : 'Imperial Porcelain'} (1)</label>
      </div>
      <div class="filter-group">
        <h4>${isRtl ? 'نطاق السعر (ر.س)' : 'Price Range (SAR)'}</h4>
        <input type="range" min="500" max="5000" value="3500" style="width:100%; accent-color:var(--lux-gold);">
        <div style="display:flex; justify-content:space-between; font-size:0.75rem; color:var(--lux-muted); margin-top:0.3rem;">
          <span>500 SAR</span>
          <span>5,000 SAR</span>
        </div>
      </div>
      <div class="filter-group">
        <h4>${isRtl ? 'التوفر' : 'Availability'}</h4>
        <label class="filter-item"><input type="checkbox" checked> ${isRtl ? 'جاهز للشحن الفوري' : 'In Stock (Express Dispatch)'}</label>
        <label class="filter-item"><input type="checkbox"> ${isRtl ? 'حجز مسبق للتشكيلة' : 'Pre-order Reserved'}</label>
      </div>
    </aside>

    <div>
      <div class="toolbar">
        <span style="font-size:0.85rem; color:var(--lux-muted); font-weight:500;">
          ${isRtl ? 'عرض 8 من أصل 8 قطع نادرة' : 'Showing 8 of 8 exclusive items'}
        </span>
        <select class="select-sort">
          <option>${isRtl ? 'الأحدث إصداراً' : 'Latest Release'}</option>
          <option>${isRtl ? 'الأعلى طلباً وتميزاً' : 'Most Exclusive'}</option>
          <option>${isRtl ? 'السعر: من الأعلى إلى الأقل' : 'Price: High to Low'}</option>
          <option>${isRtl ? 'السعر: من الأقل إلى الأعلى' : 'Price: Low to High'}</option>
        </select>
      </div>

      <div class="product-grid">
        ${productsData.map(pItem => `
          <article class="product-card">
            <div class="card-img-wrap">
              <a href="${p.prodHref}"><img src="${pItem.img}" alt="${isRtl ? pItem.titleAr : pItem.titleEn}"></a>
              ${pItem.badgeAr ? `<span class="badge">${isRtl ? pItem.badgeAr : pItem.badgeEn}</span>` : ''}
            </div>
            <div class="card-info">
              <div>
                <span style="font-size:0.7rem; text-transform:uppercase; color:var(--lux-gold); font-weight:600;">${isRtl ? pItem.catAr : pItem.catEn}</span>
                <h3 style="margin-top:0.2rem;"><a href="${p.prodHref}">${isRtl ? pItem.titleAr : pItem.titleEn}</a></h3>
              </div>
              <div class="card-bottom">
                <span style="font-weight:700; font-size:0.95rem;">${pItem.price} SAR</span>
                <button class="btn-add" onclick="openCart()">${isRtl ? 'إضافة للسلة' : 'Add to Cart'}</button>
              </div>
            </div>
          </article>
        `).join('')}
      </div>
    </div>
  </main>

  ${getFooter(isRtl)}
  ${getDrawer(isRtl)}
  ${getMobileElements('cat', isRtl)}
</body>
</html>`;
}

// 3. Product Single Page Builder
function buildProductPage(isRtl) {
  const p = getNavigationPaths('prod', isRtl);
  const pItem = productsData[0];

  return `<!DOCTYPE html>
<html lang="${isRtl ? 'ar' : 'en'}" dir="${isRtl ? 'rtl' : 'ltr'}">
<head>
  <meta charset="UTF-8">
  <meta name="viewport" content="width=device-width, initial-scale=1.0">
  <title>${isRtl ? pItem.titleAr + ' | دار النخبة' : pItem.titleEn + ' | Elite Maison'}</title>
  <style>
    ${LUXURY_CSS}
    .product-wrap {
      max-width: 1320px; margin: 3rem auto; padding: 0 1.5rem;
      display: grid; grid-template-columns: 1.1fr 1fr; gap: 4rem;
    }
    .gallery-container { display: flex; gap: 1rem; }
    .thumbnails { display: flex; flex-direction: column; gap: 1rem; width: 90px; }
    .thumb {
      width: 90px; height: 120px; object-fit: cover; cursor: pointer; border: 1px solid var(--lux-border);
      opacity: 0.7; transition: all 0.2s;
    }
    .thumb.active, .thumb:hover { opacity: 1; border-color: var(--lux-gold); }
    .main-image {
      flex-grow: 1; height: 600px; background: #eee; position: relative; overflow: hidden;
      border: 1px solid var(--lux-border);
    }
    .main-image img { width: 100%; height: 100%; object-fit: cover; }
    
    .product-details { display: flex; flex-direction: column; justify-content: center; }
    .breadcrumb { font-size: 0.8rem; color: var(--lux-muted); margin-bottom: 1rem; }
    .product-title {
      font-family: var(--font-serif); font-size: 2.4rem; font-weight: 700; line-height: 1.2;
      margin-bottom: 0.75rem; color: var(--lux-black);
    }
    .price-tag {
      font-size: 1.6rem; font-weight: 700; color: var(--lux-black); margin-bottom: 1.5rem;
      display: flex; align-items: baseline; gap: 0.5rem;
    }
    .vat-badge { font-size: 0.75rem; color: var(--lux-muted); font-weight: normal; }

    .installment-box {
      background: var(--lux-gold-light); border: 1px solid #E5D5B5; padding: 0.9rem 1.25rem;
      border-radius: 4px; margin-bottom: 2rem; font-size: 0.85rem; color: #5C4314; display: flex; align-items: center; justify-content: space-between;
    }
    
    .option-title { font-size: 0.82rem; text-transform: uppercase; font-weight: 600; margin-bottom: 0.6rem; }
    .size-pills { display: flex; gap: 0.75rem; margin-bottom: 2rem; }
    .pill {
      border: 1px solid var(--lux-border); padding: 0.5rem 1.25rem; font-size: 0.85rem;
      font-weight: 600; cursor: pointer; background: #fff; transition: all 0.2s;
    }
    .pill.active { border-color: var(--lux-black); background: var(--lux-black); color: #fff; }

    .actions-row { display: flex; gap: 1rem; margin-bottom: 2rem; }
    .btn-buy-now {
      flex-grow: 1; padding: 1.1rem; background: var(--lux-black); color: #fff; border: none;
      font-weight: 700; font-size: 0.9rem; text-transform: uppercase; letter-spacing: 0.08em;
      cursor: pointer; transition: background 0.2s;
    }
    .btn-buy-now:hover { background: #000; }
    .btn-apple-pay {
      background: #000; color: #fff; border: 1px solid #333; padding: 1.1rem 1.5rem;
      display: flex; align-items: center; justify-content: center; cursor: pointer; font-weight: 700;
    }

    .accordion-item { border-top: 1px solid var(--lux-border); padding: 1.25rem 0; }
    .accordion-btn {
      width: 100%; display: flex; justify-content: space-between; align-items: center;
      background: none; border: none; font-size: 0.95rem; font-weight: 600; cursor: pointer; text-align: start;
    }
    .accordion-content { font-size: 0.85rem; color: var(--lux-muted); line-height: 1.8; margin-top: 0.75rem; }

    @media (max-width: 900px) {
      .product-wrap { grid-template-columns: 1fr; gap: 2rem; }
      .gallery-container { flex-direction: column-reverse; }
      .thumbnails { flex-direction: row; width: 100%; }
      .main-image { height: 420px; }
    }
  </style>
</head>
<body>
  ${getHeader('prod', isRtl)}

  <main class="product-wrap" id="main">
    <div class="gallery-container">
      <div class="thumbnails">
        <img src="${pItem.img}" class="thumb active" onclick="switchImg(this.src)">
        <img src="${productsData[4].img}" class="thumb" onclick="switchImg(this.src)">
        <img src="${productsData[2].img}" class="thumb" onclick="switchImg(this.src)">
      </div>
      <div class="main-image">
        <img id="mainImg" src="${pItem.img}" alt="${isRtl ? pItem.titleAr : pItem.titleEn}">
      </div>
    </div>

    <div class="product-details">
      <div class="breadcrumb">
        ${isRtl ? 'الرئيسية / المجموعات الخاصة / الأزياء الفاخرة' : 'Home / Collections / Haute Couture'}
      </div>
      <h1 class="product-title">
        ${isRtl ? pItem.titleAr : pItem.titleEn}
      </h1>
      <span style="font-size:0.75rem; text-transform:uppercase; letter-spacing:0.1em; color:var(--lux-gold); font-weight:700; margin-bottom:1rem; display:block;">
        ${isRtl ? 'إصدار حصري محدود (مرقم 08 من 50)' : 'Limited Private Reserve (Numbered 08 of 50)'}
      </span>
      <div class="price-tag">
        1,850.00 SAR
        <span class="vat-badge">${isRtl ? '(شامل ضريبة القيمة المضافة والشحن الفاخر)' : '(VAT & Insured Shipping Included)'}</span>
      </div>

      <div class="installment-box">
        <span>${isRtl ? 'قسّم فاتورتك على 4 دفعات بقيمة 462.50 ر.س بدون فوائد عبر تمارا أو تابّي' : 'Or split in 4 interest-free payments of 462.50 SAR via Tamara or Tabby'}</span>
        <strong>Tamara / Tabby</strong>
      </div>

      <div class="option-title">${isRtl ? 'اختر المقاس الفاخر' : 'Select Tailored Size'}</div>
      <div class="size-pills">
        <button class="pill" onclick="selectPill(this)">52 S</button>
        <button class="pill active" onclick="selectPill(this)">54 M (${isRtl ? 'متبقي 2' : 'Only 2 Left'})</button>
        <button class="pill" onclick="selectPill(this)">56 L</button>
        <button class="pill" onclick="selectPill(this)">58 XL</button>
      </div>

      <div class="actions-row">
        <button class="btn-buy-now" onclick="openCart()">
          ${isRtl ? 'إضافة إلى سلة المقتنيات' : 'Add to Shopping Cart'}
        </button>
        <button class="btn-apple-pay" onclick="openCart()" aria-label="Apple Pay">
           Pay
        </button>
      </div>

      <div class="accordion-item">
        <button class="accordion-btn">
          <span>${isRtl ? 'تفاصيل الحرفية والخامات' : 'Craftsmanship & Materials'}</span>
          <span>+</span>
        </button>
        <div class="accordion-content">
          ${isRtl ? 'صيغت هذه القطعة من أجود أنواع المخمل الكشميري الطبيعي المنسوج في أعرق مصانع إيطاليا، مع تطريز خيوط الحرير الياباني بأسلوب الحياكة الدقيقة.' : 'Hand-tailored from Italian cashmere velvet and embroidered with pure Japanese silk thread.'}
        </div>
      </div>

      <div class="accordion-item">
        <button class="accordion-btn">
          <span>${isRtl ? 'الشحن الفاخر المجاني والتسليم' : 'Complimentary Insured Delivery'}</span>
          <span>+</span>
        </button>
        <div class="accordion-content">
          ${isRtl ? 'توصيل مصفح ومؤمن خلال 24-48 ساعة داخل المملكة العربية السعودية عبر أسطول سمسا إكسبريس الفاخر.' : 'Insured delivery within 24-48 hours across Saudi Arabia and the GCC.'}
        </div>
      </div>
    </div>
  </main>

  <script>
    function switchImg(src) {
      document.getElementById('mainImg').src = src;
      document.querySelectorAll('.thumb').forEach(t => t.classList.remove('active'));
      event.target.classList.add('active');
    }
    function selectPill(btn) {
      document.querySelectorAll('.pill').forEach(p => p.classList.remove('active'));
      btn.classList.add('active');
    }
  </script>

  ${getFooter(isRtl)}
  ${getDrawer(isRtl)}
  ${getMobileElements('prod', isRtl)}
</body>
</html>`;
}

// 4. Cart Page Builder
function buildCartPage(isRtl) {
  const p = getNavigationPaths('cart', isRtl);
  const p1 = productsData[0];
  const p2 = productsData[1];

  return `<!DOCTYPE html>
<html lang="${isRtl ? 'ar' : 'en'}" dir="${isRtl ? 'rtl' : 'ltr'}">
<head>
  <meta charset="UTF-8">
  <meta name="viewport" content="width=device-width, initial-scale=1.0">
  <title>${isRtl ? 'سلة المشتريات الفاخرة | دار النخبة' : 'Your Shopping Bag | Elite Maison'}</title>
  <style>
    ${LUXURY_CSS}
    .cart-page-wrap {
      max-width: 1200px; margin: 3.5rem auto; padding: 0 1.5rem;
      display: grid; grid-template-columns: 1.8fr 1fr; gap: 3.5rem;
    }
    .cart-title { font-family: var(--font-serif); font-size: 2.2rem; margin-bottom: 2rem; }
    .cart-table-item {
      display: flex; gap: 1.5rem; padding: 1.5rem 0; border-bottom: 1px solid var(--lux-border); align-items: center;
    }
    .cart-table-img { width: 90px; height: 120px; object-fit: cover; border: 1px solid var(--lux-border); }
    .order-summary-box {
      background: var(--lux-surface); border: 1px solid var(--lux-border); padding: 2rem;
      position: sticky; top: 90px; border-radius: 2px;
    }
    .summary-row { display: flex; justify-content: space-between; margin-bottom: 0.9rem; font-size: 0.9rem; }
    .summary-row.total { font-size: 1.25rem; font-weight: 700; border-top: 1px solid var(--lux-border); padding-top: 1rem; margin-top: 1rem; }
    .coupon-row { display: flex; gap: 0.5rem; margin: 1.5rem 0; }
    .coupon-input { flex-grow: 1; padding: 0.75rem; border: 1px solid var(--lux-border); font-size: 0.85rem; }
    .btn-apply { padding: 0.75rem 1.25rem; background: var(--lux-black); color: #fff; border: none; cursor: pointer; font-weight: 600; font-size: 0.8rem; }
    .btn-checkout {
      width: 100%; padding: 1.1rem; background: var(--lux-gold); color: #000; border: none;
      font-weight: 700; font-size: 0.95rem; text-transform: uppercase; letter-spacing: 0.08em; cursor: pointer;
    }
    @media (max-width: 800px) {
      .cart-page-wrap { grid-template-columns: 1fr; }
    }
  </style>
</head>
<body>
  ${getHeader('cart', isRtl)}

  <main class="cart-page-wrap" id="main">
    <div>
      <h1 class="cart-title">${isRtl ? 'سلة المشتريات الفاخرة' : 'Your Shopping Bag'}</h1>
      
      <div class="cart-table-item">
        <img src="${p1.img}" class="cart-table-img" alt="${isRtl ? p1.titleAr : p1.titleEn}">
        <div style="flex-grow:1;">
          <h3 style="font-size:1.05rem;">${isRtl ? p1.titleAr : p1.titleEn}</h3>
          <p style="font-size:0.8rem; color:var(--lux-muted); margin:0.3rem 0;">${isRtl ? 'المقاس: 54 M | اللون: أسود فاحم' : 'Size: 54 M | Color: Noir'}</p>
          <strong style="font-size:1.05rem;">1,850.00 SAR</strong>
        </div>
        <div class="qty-ctrl">
          <button onclick="updatePageCart(-1)">-</button>
          <span id="pageQty1">1</span>
          <button onclick="updatePageCart(1)">+</button>
        </div>
      </div>

      <div class="cart-table-item">
        <img src="${p2.img}" class="cart-table-img" alt="${isRtl ? p2.titleAr : p2.titleEn}">
        <div style="flex-grow:1;">
          <h3 style="font-size:1.05rem;">${isRtl ? p2.titleAr : p2.titleEn}</h3>
          <p style="font-size:0.8rem; color:var(--lux-muted); margin:0.3rem 0;">${isRtl ? 'إصدار الشتاء المعتّق' : 'Aged Winter Vintage'}</p>
          <strong style="font-size:1.05rem;">1,250.00 SAR</strong>
        </div>
        <div class="qty-ctrl">
          <button onclick="updatePageCart(-1)">-</button>
          <span id="pageQty2">1</span>
          <button onclick="updatePageCart(1)">+</button>
        </div>
      </div>
    </div>

    <aside class="order-summary-box">
      <h3 style="font-family:var(--font-serif); font-size:1.3rem; margin-bottom:1.5rem;">${isRtl ? 'ملخص الطلب' : 'Order Summary'}</h3>
      <div class="summary-row">
        <span>${isRtl ? 'المجموع الفرعي' : 'Subtotal'}</span>
        <span id="pageSubtotal">3,100.00 SAR</span>
      </div>
      <div class="summary-row">
        <span>${isRtl ? 'ضريبة القيمة المضافة (15%)' : 'VAT (15%)'}</span>
        <span>465.00 SAR</span>
      </div>
      <div class="summary-row">
        <span>${isRtl ? 'الشحن الفاخر السريع' : 'Insured Express Shipping'}</span>
        <span style="color:var(--lux-gold); font-weight:700;">${isRtl ? 'مجاني ومؤمن' : 'Complimentary'}</span>
      </div>

      <div class="coupon-row">
        <input type="text" class="coupon-input" placeholder="${isRtl ? 'رمز القسيمة (مثال: LUXURY10)' : 'Promo Code'}">
        <button class="btn-apply">${isRtl ? 'تطبيق' : 'Apply'}</button>
      </div>

      <div class="summary-row total">
        <span>${isRtl ? 'المجموع الكلي' : 'Estimated Total'}</span>
        <span id="pageTotal">3,100.00 SAR</span>
      </div>

      <a href="https://salla.sa" target="_blank" style="display:block; text-align:center; margin-top:1.5rem;" class="btn-checkout">
        ${isRtl ? 'المتابعة لإتمام الدفع في سلة برو' : 'Proceed to Salla Checkout'}
      </a>
    </aside>
  </main>

  <script>
    function updatePageCart(delta) {
      const q = document.getElementById('pageQty1');
      if (!q) return;
      let val = parseInt(q.innerText) + delta;
      if (val < 1) val = 1;
      q.innerText = val;
      const total = (1850 * val + 1250).toLocaleString('en-US', { minimumFractionDigits: 2 });
      document.getElementById('pageSubtotal').innerText = total + ' SAR';
      document.getElementById('pageTotal').innerText = total + ' SAR';
    }
  </script>

  ${getFooter(isRtl)}
  ${getDrawer(isRtl)}
  ${getMobileElements('cart', isRtl)}
</body>
</html>`;
}

// 5. Tracking Page Builder
function buildTrackingPage(isRtl) {
  const p = getNavigationPaths('track', isRtl);

  return `<!DOCTYPE html>
<html lang="${isRtl ? 'ar' : 'en'}" dir="${isRtl ? 'rtl' : 'ltr'}">
<head>
  <meta charset="UTF-8">
  <meta name="viewport" content="width=device-width, initial-scale=1.0">
  <title>${isRtl ? 'تتبع مسار الشحنة | دار النخبة' : 'Track Your Shipment | Elite Maison'}</title>
  <style>
    ${LUXURY_CSS}
    .track-wrap { max-width: 800px; margin: 4rem auto; padding: 0 1.5rem; }
    .track-card {
      background: var(--lux-surface); border: 1px solid var(--lux-border); padding: 2.5rem; border-radius: 2px;
    }
    .search-row { display: flex; gap: 0.75rem; margin-bottom: 2.5rem; }
    .search-input { flex-grow: 1; padding: 0.9rem; border: 1px solid var(--lux-border); font-size: 0.9rem; }
    .btn-search { padding: 0.9rem 2rem; background: var(--lux-black); color: #fff; border: none; font-weight: 600; cursor: pointer; }
    
    .timeline { position: relative; margin: 3rem 0; padding-inline-start: 2rem; }
    .timeline::before {
      content: ''; position: absolute; top: 0; bottom: 0; ${isRtl ? 'right' : 'left'}: 7px;
      width: 2px; background: var(--lux-border);
    }
    .step { position: relative; margin-bottom: 2rem; }
    .step::before {
      content: ''; position: absolute; ${isRtl ? 'right' : 'left'}: -29px; top: 4px;
      width: 14px; height: 14px; border-radius: 50%; background: #ccc; border: 3px solid #fff;
    }
    .step.done::before { background: var(--lux-gold); }
    .step.active::before { background: #000; box-shadow: 0 0 0 4px var(--lux-gold-light); }
  </style>
</head>
<body>
  ${getHeader('track', isRtl)}

  <main class="track-wrap" id="main">
    <div class="track-card">
      <h1 style="font-family:var(--font-serif); font-size:2rem; margin-bottom:0.5rem;">${isRtl ? 'تتبع شحنتك الفاخرة' : 'Track Your Consignment'}</h1>
      <p style="font-size:0.85rem; color:var(--lux-muted); margin-bottom:2rem;">
        ${isRtl ? 'أدخل رقم الشحنة أو رقم الطلب المسجل في منصة سلة' : 'Enter your Salla Order ID or SMSA Waybill Number'}
      </p>

      <div class="search-row">
        <input type="text" class="search-input" value="SL-884920" placeholder="e.g. SL-884920">
        <button class="btn-search">${isRtl ? 'استعلام فوري' : 'Track'}</button>
      </div>

      <div style="background:var(--lux-bg); padding:1.25rem; border:1px solid var(--lux-border); display:flex; justify-content:space-between; flex-wrap:wrap; gap:1.25rem; font-size:0.85rem; margin-bottom:1.5rem;">
        <div><strong style="color:var(--lux-muted);">${isRtl ? 'رقم الشحنة' : 'Waybill'}:</strong> <span style="font-weight:700;">SMSA-99201481</span></div>
        <div><strong style="color:var(--lux-muted);">${isRtl ? 'الناقل المعتمد' : 'Carrier'}:</strong> <span style="font-weight:700;">سمسا إكسبريس الفاخر</span></div>
        <div><strong style="color:var(--lux-muted);">${isRtl ? 'الموعد المتوقع' : 'ETA'}:</strong> <span style="font-weight:700; color:var(--lux-gold);">${isRtl ? 'خلال 24 ساعة' : 'Within 24 Hours'}</span></div>
      </div>

      <div class="timeline">
        <div class="step done">
          <h4>${isRtl ? 'تم اعتماد وتأكيد الطلب بنجاح' : 'Order Confirmed'}</h4>
          <span style="font-size:0.75rem; color:var(--lux-muted);">${isRtl ? '28 سبتمبر 2026 - 10:30 صباحاً' : '28 Sep 2026 - 10:30 AM'}</span>
        </div>
        <div class="step done">
          <h4>${isRtl ? 'التجهيز والتغليف الفاخر الحريري' : 'Bespoke Packaging Completed'}</h4>
          <span style="font-size:0.75rem; color:var(--lux-muted);">${isRtl ? '28 سبتمبر 2026 - 02:15 مساءً' : '28 Sep 2026 - 02:15 PM'}</span>
        </div>
        <div class="step active">
          <h4>${isRtl ? 'في الطريق مع مندوب التوصيل المباشر' : 'Out for Direct Delivery'}</h4>
          <span style="font-size:0.75rem; color:var(--lux-gold); font-weight:600;">${isRtl ? 'جاري التوصيل إلى الرياض، حي حطين' : 'En route in Riyadh, Hittin'}</span>
        </div>
        <div class="step">
          <h4>${isRtl ? 'تم التسليم للعميل' : 'Delivered'}</h4>
          <span style="font-size:0.75rem; color:var(--lux-muted);">${isRtl ? 'متوقع خلال ساعات اليوم' : 'Expected within hours'}</span>
        </div>
      </div>
    </div>
  </main>

  ${getFooter(isRtl)}
  ${getDrawer(isRtl)}
  ${getMobileElements('track', isRtl)}
</body>
</html>`;
}

// 6. Account Page Builder
function buildAccountPage(isRtl) {
  const p = getNavigationPaths('acc', isRtl);

  return `<!DOCTYPE html>
<html lang="${isRtl ? 'ar' : 'en'}" dir="${isRtl ? 'rtl' : 'ltr'}">
<head>
  <meta charset="UTF-8">
  <meta name="viewport" content="width=device-width, initial-scale=1.0">
  <title>${isRtl ? 'حساب العضوية الفاخرة | دار النخبة' : 'Private Client Portal | Elite Maison'}</title>
  <style>
    ${LUXURY_CSS}
    .acc-wrap { max-width: 900px; margin: 4rem auto; padding: 0 1.5rem; }
    .acc-card { background: var(--lux-surface); border: 1px solid var(--lux-border); padding: 2.5rem; }
    .tab-bar { display: flex; gap: 2rem; border-bottom: 1px solid var(--lux-border); margin-bottom: 2rem; }
    .tab-btn {
      background: none; border: none; font-size: 0.95rem; font-weight: 600; padding-bottom: 0.75rem;
      cursor: pointer; color: var(--lux-muted);
    }
    .tab-btn.active { color: var(--lux-black); border-bottom: 2px solid var(--lux-gold); }
    .order-card {
      border: 1px solid var(--lux-border); padding: 1.25rem; margin-bottom: 1rem;
      display: flex; justify-content: space-between; align-items: center;
    }
  </style>
</head>
<body>
  ${getHeader('acc', isRtl)}

  <main class="acc-wrap" id="main">
    <div class="acc-card">
      <div style="display:flex; align-items:center; gap:1.5rem; margin-bottom:2rem;">
        <div style="width:64px; height:64px; border-radius:50%; background:var(--lux-gold); color:#000; display:flex; align-items:center; justify-content:center; font-size:1.5rem; font-weight:700;">
          N
        </div>
        <div>
          <h1 style="font-family:var(--font-serif); font-size:1.6rem;">${isRtl ? 'الأستاذ نايف الحربي' : 'Client: Naif A.'}</h1>
          <span style="font-size:0.8rem; color:var(--lux-gold); font-weight:700; text-transform:uppercase;">
            ${isRtl ? 'عضوية النخبة الذهبية (VIP Reserve)' : 'VIP Reserve Tier'}
          </span>
        </div>
      </div>

      <div class="tab-bar">
        <button class="tab-btn active">${isRtl ? 'طلباتي السابقة' : 'Order History'}</button>
        <button class="tab-btn">${isRtl ? 'العناوين المحفوظة' : 'Saved Addresses'}</button>
        <button class="tab-btn">${isRtl ? 'قائمة الأمنيات (4)' : 'Wishlist (4)'}</button>
      </div>

      <div class="order-card">
        <div>
          <strong>#SL-884920</strong>
          <div style="font-size:0.8rem; color:var(--lux-muted);">${isRtl ? '2 قطعة: عباية مخمل + عود ملكي' : '2 items: Cashmere Abaya + Oud'}</div>
          <span style="font-size:0.75rem; color:var(--lux-gold); font-weight:600;">${isRtl ? 'قيد التوصيل الفوري' : 'Out for Delivery'}</span>
        </div>
        <div style="text-align:end;">
          <div style="font-weight:700;">3,100.00 SAR</div>
          <a href="${p.trackHref}" style="font-size:0.8rem; text-decoration:underline;">${isRtl ? 'تتبع الشحنة &larr;' : 'Track &rarr;'}</a>
        </div>
      </div>

      <div class="order-card">
        <div>
          <strong>#SL-771204</strong>
          <div style="font-size:0.8rem; color:var(--lux-muted);">${isRtl ? '1 قطعة: حقيبة يد هيرمس كلاسيك' : '1 item: Artisan Handcrafted Leather Tote'}</div>
          <span style="font-size:0.75rem; color:#2e7d32; font-weight:600;">${isRtl ? 'تم التوصيل بنجاح' : 'Delivered'}</span>
        </div>
        <div style="text-align:end;">
          <div style="font-weight:700;">3,400.00 SAR</div>
          <span style="font-size:0.75rem; color:var(--lux-muted);">14 Aug 2026</span>
        </div>
      </div>
    </div>
  </main>

  ${getFooter(isRtl)}
  ${getDrawer(isRtl)}
  ${getMobileElements('acc', isRtl)}
</body>
</html>`;
}

// ============================================================================
// 5. COMPILE AND WRITE ALL 13 ARTIFACTS
// ============================================================================

console.log('[1/2] Compiling multi-page Salla Twilight luxury storefront artifacts...');

// 1. Home Pages
const homeAr = buildHomePage(true);
const homeEn = buildHomePage(false);
fs.writeFileSync(path.join(DIST_DIR, 'index.html'), homeAr, 'utf8');
fs.writeFileSync(path.join(DIST_DIR, 'preview-ar.html'), homeAr, 'utf8');
fs.writeFileSync(path.join(DIST_DIR, 'preview-en.html'), homeEn, 'utf8');

// 2. Categories Pages
fs.writeFileSync(path.join(DIST_DIR, 'categories.html'), buildCategoriesPage(true), 'utf8');
fs.writeFileSync(path.join(DIST_DIR, 'categories-en.html'), buildCategoriesPage(false), 'utf8');

// 3. Product Single Pages
fs.writeFileSync(path.join(DIST_DIR, 'product.html'), buildProductPage(true), 'utf8');
fs.writeFileSync(path.join(DIST_DIR, 'product-en.html'), buildProductPage(false), 'utf8');

// 4. Cart Pages
fs.writeFileSync(path.join(DIST_DIR, 'cart.html'), buildCartPage(true), 'utf8');
fs.writeFileSync(path.join(DIST_DIR, 'cart-en.html'), buildCartPage(false), 'utf8');

// 5. Tracking Pages
fs.writeFileSync(path.join(DIST_DIR, 'tracking.html'), buildTrackingPage(true), 'utf8');
fs.writeFileSync(path.join(DIST_DIR, 'tracking-en.html'), buildTrackingPage(false), 'utf8');

// 6. VIP Account Pages
fs.writeFileSync(path.join(DIST_DIR, 'account.html'), buildAccountPage(true), 'utf8');
fs.writeFileSync(path.join(DIST_DIR, 'account-en.html'), buildAccountPage(false), 'utf8');

console.log('[2/2] Successfully generated all 13 artifacts in dist/:');
console.log('      - index.html & preview-ar.html (Home Arabic RTL)');
console.log('      - preview-en.html (Home English LTR)');
console.log('      - categories.html & categories-en.html (Collections Catalog)');
console.log('      - product.html & product-en.html (Single Product Details)');
console.log('      - cart.html & cart-en.html (Full Shopping Bag)');
console.log('      - tracking.html & tracking-en.html (Order Tracking & Waybill)');
console.log('      - account.html & account-en.html (VIP Client Portal)');
