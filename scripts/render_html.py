import os
import subprocess
from pathlib import Path

repo_root = Path(__file__).resolve().parent.parent

# Read master.twig, luxury-hero-banner.twig, index.twig
master_content = (repo_root / "src" / "views" / "layouts" / "master.twig").read_text(encoding="utf-8")
hero_content = (repo_root / "src" / "views" / "components" / "home" / "luxury-hero-banner.twig").read_text(encoding="utf-8")
index_content = (repo_root / "src" / "views" / "pages" / "index.twig").read_text(encoding="utf-8")

# Construct the full static HTML preview with authentic store variables
rendered_html = """<!DOCTYPE html>
<html lang="ar" dir="rtl">
<head>
  <meta charset="UTF-8">
  <meta name="viewport" content="width=device-width, initial-scale=1.0">
  <title>المتجر الفاخر برو | الرئيسية</title>
  <link rel="preconnect" href="https://fonts.googleapis.com">
  <link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>
  <link href="https://fonts.googleapis.com/css2?family=Cormorant+Garamond:ital,wght@0,300;0,400;0,500;0,600;0,700;1,400&family=Noto+Kufi+Arabic:wght@200;300;400;500;600;700&family=IBM+Plex+Sans+Arabic:wght@200;300;400;500;600&display=swap" rel="stylesheet">
  <style>
    :root {
      --luxury-primary: #0D0D0D;
      --luxury-accent: #C5A059;
      --luxury-accent-light: #DFCA9B;
      --luxury-accent-dark: #9A7B3E;
      --luxury-bg: #FAF9F5;
      --luxury-surface: #FFFFFF;
      --luxury-border: #E6E2D8;
      --luxury-border-light: #F2EFE9;
      --luxury-text: #171615;
      --luxury-muted: #7A766D;
      --font-arabic: 'IBM Plex Sans Arabic', 'Noto Kufi Arabic', -apple-system, sans-serif;
      --font-display: 'Cormorant Garamond', 'IBM Plex Sans Arabic', Georgia, serif;
      --color-primary: var(--luxury-primary);
    }

    *, *::before, *::after {
      box-sizing: border-box;
      margin: 0;
      padding: 0;
    }

    html {
      scroll-behavior: smooth;
    }

    body {
      font-family: var(--font-arabic);
      background-color: var(--luxury-bg);
      color: var(--luxury-text);
      line-height: 1.65;
      letter-spacing: -0.01em;
      text-rendering: optimizeLegibility;
      -webkit-font-smoothing: antialiased;
      min-height: 100vh;
      display: flex;
      flex-direction: column;
    }

    a {
      color: inherit;
      text-decoration: none;
      transition: all 0.25s ease;
    }

    img {
      max-width: 100%;
      height: auto;
      display: block;
    }

    .lux-container {
      width: 100%;
      max-width: 1320px;
      margin-left: auto;
      margin-right: auto;
      padding-left: 2rem;
      padding-right: 2rem;
    }

    .lux-topbar {
      background: #0D0D0D;
      color: #C5A059;
      font-size: 0.72rem;
      font-weight: 500;
      letter-spacing: 0.08em;
      padding: 0.5rem 1rem;
      text-align: center;
      border-bottom: 1px solid rgba(197, 160, 89, 0.2);
    }

    .lux-header {
      position: sticky;
      top: 0;
      z-index: 50;
      background: rgba(255, 255, 255, 0.97);
      backdrop-filter: blur(20px);
      border-bottom: 1px solid var(--luxury-border);
    }

    .lux-header-inner {
      height: 78px;
      display: flex;
      align-items: center;
      justify-content: space-between;
    }

    .lux-nav-group {
      display: flex;
      align-items: center;
      gap: 2.5rem;
    }

    .lux-logo {
      font-family: var(--font-display);
      font-size: 1.85rem;
      font-weight: 700;
      letter-spacing: -0.02em;
      color: var(--luxury-primary);
    }

    .lux-nav-links {
      display: flex;
      align-items: center;
      gap: 2rem;
      list-style: none;
    }

    .lux-nav-link {
      font-size: 0.875rem;
      font-weight: 400;
      color: var(--luxury-muted);
      position: relative;
      padding: 0.5rem 0;
    }

    .lux-nav-link:hover {
      color: var(--luxury-primary);
    }

    .lux-actions {
      display: flex;
      align-items: center;
      gap: 1.25rem;
    }

    .lux-btn-pill {
      font-size: 0.75rem;
      font-weight: 500;
      letter-spacing: 0.06em;
      padding: 0.5rem 1.15rem;
      border: 1px solid var(--luxury-border);
      background: transparent;
      color: var(--luxury-text);
      display: inline-flex;
      align-items: center;
      gap: 0.4rem;
      cursor: pointer;
    }

    .lux-btn-pill:hover {
      border-color: var(--luxury-primary);
      background: var(--luxury-primary);
      color: #FFFFFF;
    }

    .lux-hero {
      position: relative;
      width: 100%;
      min-height: 640px;
      background: #080808;
      color: #FFFFFF;
      overflow: hidden;
      display: flex;
      align-items: center;
      justify-content: center;
      text-align: center;
    }

    .lux-hero-bg {
      position: absolute;
      inset: 0;
      width: 100%;
      height: 100%;
      object-fit: cover;
      object-position: center;
      opacity: 0.45;
    }

    .lux-hero-scrim {
      position: absolute;
      inset: 0;
      background: radial-gradient(circle at center, rgba(8,8,8,0.4) 0%, rgba(8,8,8,0.88) 100%),
                  linear-gradient(180deg, rgba(8,8,8,0.2) 0%, rgba(8,8,8,0.7) 100%);
    }

    .lux-hero-content {
      position: relative;
      z-index: 10;
      padding: 6rem 1rem;
      max-width: 860px;
      margin: 0 auto;
      display: flex;
      flex-direction: column;
      align-items: center;
    }

    .lux-eyebrow {
      display: inline-flex;
      align-items: center;
      gap: 0.5rem;
      font-size: 0.72rem;
      font-weight: 500;
      letter-spacing: 0.2em;
      text-transform: uppercase;
      color: var(--luxury-accent-light);
      padding: 0.4rem 1.25rem;
      border: 1px solid rgba(197, 160, 89, 0.4);
      background: rgba(13, 13, 13, 0.65);
      backdrop-filter: blur(8px);
      margin-bottom: 1.75rem;
    }

    .lux-hero-title {
      font-family: var(--font-arabic);
      font-size: clamp(2.4rem, 5.5vw, 4.25rem);
      font-weight: 300;
      line-height: 1.25;
      letter-spacing: -0.02em;
      margin-bottom: 1.5rem;
      color: #FFFFFF;
      text-shadow: 0 4px 20px rgba(0,0,0,0.5);
    }

    .lux-hero-title strong {
      font-weight: 600;
      background: linear-gradient(135deg, #FFFFFF 30%, var(--luxury-accent-light) 100%);
      -webkit-background-clip: text;
      -webkit-text-fill-color: transparent;
    }

    .lux-hero-subtitle {
      font-size: 1.125rem;
      font-weight: 300;
      line-height: 1.8;
      color: #D6D2C8;
      margin-bottom: 2.75rem;
      max-width: 680px;
      text-shadow: 0 2px 10px rgba(0,0,0,0.4);
    }

    .lux-cta-btn {
      display: inline-flex;
      align-items: center;
      gap: 0.85rem;
      padding: 1.1rem 2.85rem;
      font-size: 0.8125rem;
      font-weight: 600;
      letter-spacing: 0.12em;
      text-transform: uppercase;
      background: linear-gradient(135deg, #D4AF37 0%, #C5A059 100%);
      color: #0D0D0D;
      border: 1px solid rgba(255, 255, 255, 0.2);
      box-shadow: 0 8px 24px rgba(197, 160, 89, 0.25);
    }

    .lux-trust-bar {
      border-top: 1px solid var(--luxury-border);
      border-bottom: 1px solid var(--luxury-border);
      padding: 3.5rem 0;
      background: #FFFFFF;
    }

    .lux-trust-grid {
      display: grid;
      grid-template-columns: repeat(3, 1fr);
      gap: 2.5rem;
      text-align: center;
    }

    .lux-trust-item {
      padding: 0 1rem;
    }

    .lux-trust-icon {
      width: 44px;
      height: 44px;
      margin: 0 auto 1.25rem;
      border: 1px solid var(--luxury-accent);
      display: flex;
      align-items: center;
      justify-content: center;
      color: var(--luxury-accent-dark);
      font-size: 1.25rem;
    }

    .lux-trust-item h4 {
      font-family: var(--font-arabic);
      font-size: 1.15rem;
      font-weight: 500;
      margin-bottom: 0.4rem;
      color: var(--luxury-primary);
    }

    .lux-trust-item p {
      font-size: 0.8125rem;
      color: var(--luxury-muted);
      line-height: 1.6;
    }

    .lux-section {
      padding: 6rem 0;
    }

    .lux-section-header {
      display: flex;
      flex-direction: column;
      margin-bottom: 3.5rem;
      text-align: center;
    }

    .lux-section-tag {
      font-size: 0.72rem;
      font-weight: 600;
      letter-spacing: 0.2em;
      text-transform: uppercase;
      color: var(--luxury-accent-dark);
      margin-bottom: 0.65rem;
      display: block;
    }

    .lux-section-title {
      font-family: var(--font-arabic);
      font-size: clamp(1.85rem, 3.5vw, 2.75rem);
      font-weight: 300;
      color: var(--luxury-primary);
      letter-spacing: -0.02em;
      position: relative;
      display: inline-block;
      margin: 0 auto;
    }

    .lux-section-title::after {
      content: '';
      display: block;
      width: 48px;
      height: 1.5px;
      background: var(--luxury-accent);
      margin: 1.25rem auto 0;
    }

    .lux-product-grid {
      display: grid;
      grid-template-columns: repeat(4, 1fr);
      gap: 2rem;
    }

    .lux-card {
      background: var(--luxury-surface);
      border: 1px solid var(--luxury-border);
      display: flex;
      flex-direction: column;
      transition: all 0.35s ease;
      position: relative;
    }

    .lux-card-media {
      position: relative;
      aspect-ratio: 3/4;
      background: #F4F1EA;
      overflow: hidden;
    }

    .lux-card-img {
      width: 100%;
      height: 100%;
      object-fit: cover;
      object-position: center;
    }

    .lux-card-badge {
      position: absolute;
      top: 0.85rem;
      right: 0.85rem;
      font-size: 0.65rem;
      font-weight: 600;
      letter-spacing: 0.12em;
      text-transform: uppercase;
      padding: 0.3rem 0.75rem;
      background: #0D0D0D;
      color: #FFFFFF;
      border: 1px solid rgba(197, 160, 89, 0.35);
    }

    .lux-card-body {
      padding: 1.5rem 1.25rem 1.25rem;
      display: flex;
      flex-direction: column;
      flex-grow: 1;
      justify-content: space-between;
    }

    .lux-card-title {
      font-size: 0.95rem;
      font-weight: 400;
      color: var(--luxury-text);
      margin-bottom: 0.4rem;
    }

    .lux-card-sub {
      font-size: 0.75rem;
      color: var(--luxury-muted);
      margin-bottom: 1.25rem;
    }

    .lux-card-footer {
      display: flex;
      align-items: center;
      justify-content: space-between;
      padding-top: 1rem;
      border-top: 1px solid var(--luxury-border-light);
    }

    .lux-card-price {
      font-size: 1.05rem;
      font-weight: 600;
      color: var(--luxury-primary);
    }

    .lux-footer {
      background: #0D0D0D;
      color: #D1CEC7;
      padding: 5rem 0 2.5rem;
      margin-top: auto;
      border-top: 1px solid rgba(197, 160, 89, 0.2);
    }

    .lux-footer-grid {
      display: grid;
      grid-template-columns: 2fr 1fr 1fr;
      gap: 3rem;
      margin-bottom: 4rem;
    }

    .lux-footer-brand h3 {
      font-family: var(--font-display);
      font-size: 1.75rem;
      color: #FFFFFF;
      margin-bottom: 1rem;
    }

    .lux-footer-brand p {
      font-size: 0.875rem;
      color: #9C9890;
      max-width: 380px;
      line-height: 1.75;
    }

    .lux-footer-col h4 {
      font-size: 0.75rem;
      font-weight: 600;
      letter-spacing: 0.15em;
      text-transform: uppercase;
      color: var(--luxury-accent-light);
      margin-bottom: 1.5rem;
    }

    .lux-footer-links {
      list-style: none;
      display: flex;
      flex-direction: column;
      gap: 0.85rem;
    }

    .lux-footer-links a {
      font-size: 0.8125rem;
      color: #A6A29A;
    }

    .lux-footer-bottom {
      border-top: 1px solid rgba(255,255,255,0.08);
      padding-top: 2rem;
      display: flex;
      align-items: center;
      justify-content: space-between;
      font-size: 0.75rem;
      color: #737069;
    }
  </style>
</head>
<body>
  <aside class="lux-topbar">
    توصيل فاخر ومجاني لكافة الطلبات | ضمان الأصالة والجودة العالية
  </aside>

  <header role="banner" class="lux-header">
    <div class="lux-container lux-header-inner">
      <div class="lux-nav-group">
        <span class="lux-logo">المتجر الفاخر برو</span>
        <nav role="navigation">
          <ul class="lux-nav-links">
            <li><a href="#" class="lux-nav-link">الرئيسية</a></li>
            <li><a href="#" class="lux-nav-link">المجموعات</a></li>
            <li><a href="#" class="lux-nav-link">العروض</a></li>
            <li><a href="#" class="lux-nav-link">المدونة</a></li>
          </ul>
        </nav>
      </div>
      <div class="lux-actions">
        <a href="#" class="lux-btn-pill">English</a>
        <a href="#" class="lux-btn-pill">السلة (٠)</a>
        <a href="#" class="lux-btn-pill">حسابي</a>
      </div>
    </div>
  </header>

  <main>
    <section class="lux-hero">
      <img src="https://images.unsplash.com/photo-1547949003-9792a18a2601?q=80&w=1920&auto=format&fit=crop" alt="Hero" class="lux-hero-bg">
      <div class="lux-hero-scrim"></div>
      <div class="lux-container">
        <div class="lux-hero-content">
          <span class="lux-eyebrow">✦ تشكيلة حصرية ٢٠٢٦ ✦</span>
          <h1 class="lux-hero-title">مجموعة <strong>الرفاهية الاستثنائية</strong></h1>
          <p class="lux-hero-subtitle">حرفية استثنائية وتفاصيل حصرية مصممة لتواكب ذوقك الرفيع في عالم الأناقة المعاصرة</p>
          <div>
            <a href="#" class="lux-cta-btn">
              <span>اكتشف التشكيلة الحصرية</span>
              <span>&larr;</span>
            </a>
          </div>
        </div>
      </div>
    </section>

    <section class="lux-trust-bar">
      <div class="lux-container">
        <div class="lux-trust-grid">
          <div class="lux-trust-item">
            <div class="lux-trust-icon">✦</div>
            <h4>حرفية استثنائية</h4>
            <p>مواد أصلية مختارة بعناية فائقة تلبي أرقى معايير الجودة العالمية.</p>
          </div>
          <div class="lux-trust-item">
            <div class="lux-trust-icon">◈</div>
            <h4>شحن خاص وسريع</h4>
            <p>توصيل فاخر وتغليف ملكي يحافظ على سلامة مشترياتك الثمينة.</p>
          </div>
          <div class="lux-trust-item">
            <div class="lux-trust-icon">❖</div>
            <h4>دفع آمن ومشفر</h4>
            <p>معاملات موثوقة ومحمية ببروتوكولات الأمان العالمية ومنصة سلة.</p>
          </div>
        </div>
      </div>
    </section>

    <section class="lux-section" style="padding-bottom: 2rem;">
      <div class="lux-container">
        <div class="lux-section-header">
          <span class="lux-section-tag">التشكيلات الحصرية</span>
          <h2 class="lux-section-title">مجموعات مختارة بعناية</h2>
        </div>
        <div style="display: grid; grid-template-columns: repeat(3, 1fr); gap: 2rem;">
          <div style="position: relative; height: 380px; overflow: hidden; background: #0D0D0D; border: 1px solid var(--luxury-border);">
            <img src="https://images.unsplash.com/photo-1522335789203-aabd1fc54bc9?q=80&w=800&auto=format&fit=crop" style="width: 100%; height: 100%; object-fit: cover; opacity: 0.65;">
            <div style="position: absolute; inset: 0; background: linear-gradient(180deg, transparent 40%, rgba(13,13,13,0.9) 100%); display: flex; flex-direction: column; justify-content: flex-end; padding: 2rem;">
              <span style="font-size: 0.75rem; color: var(--luxury-accent); letter-spacing: 0.15em; text-transform: uppercase;">إصدار محدود</span>
              <h3 style="font-family: var(--font-arabic); font-size: 1.5rem; color: #FFFFFF; font-weight: 500; margin: 0.35rem 0 1rem;">عطور النيش الملكية</h3>
              <a href="#" style="color: #FFFFFF; font-size: 0.8125rem; text-transform: uppercase; letter-spacing: 0.1em; border-bottom: 1px solid var(--luxury-accent); width: fit-content; padding-bottom: 0.2rem;">اكتشف المجموعة &larr;</a>
            </div>
          </div>
          <div style="position: relative; height: 380px; overflow: hidden; background: #0D0D0D; border: 1px solid var(--luxury-border);">
            <img src="https://images.unsplash.com/photo-1523275335684-37898b6baf30?q=80&w=800&auto=format&fit=crop" style="width: 100%; height: 100%; object-fit: cover; opacity: 0.65;">
            <div style="position: absolute; inset: 0; background: linear-gradient(180deg, transparent 40%, rgba(13,13,13,0.9) 100%); display: flex; flex-direction: column; justify-content: flex-end; padding: 2rem;">
              <span style="font-size: 0.75rem; color: var(--luxury-accent); letter-spacing: 0.15em; text-transform: uppercase;">صناعة سويسرية</span>
              <h3 style="font-family: var(--font-arabic); font-size: 1.5rem; color: #FFFFFF; font-weight: 500; margin: 0.35rem 0 1rem;">ساعات يد كرونوغراف</h3>
              <a href="#" style="color: #FFFFFF; font-size: 0.8125rem; text-transform: uppercase; letter-spacing: 0.1em; border-bottom: 1px solid var(--luxury-accent); width: fit-content; padding-bottom: 0.2rem;">اكتشف المجموعة &larr;</a>
            </div>
          </div>
          <div style="position: relative; height: 380px; overflow: hidden; background: #0D0D0D; border: 1px solid var(--luxury-border);">
            <img src="https://images.unsplash.com/photo-1599643478518-a784e5dc4c8f?q=80&w=800&auto=format&fit=crop" style="width: 100%; height: 100%; object-fit: cover; opacity: 0.65;">
            <div style="position: absolute; inset: 0; background: linear-gradient(180deg, transparent 40%, rgba(13,13,13,0.9) 100%); display: flex; flex-direction: column; justify-content: flex-end; padding: 2rem;">
              <span style="font-size: 0.75rem; color: var(--luxury-accent); letter-spacing: 0.15em; text-transform: uppercase;">ذهب عيار ١٨</span>
              <h3 style="font-family: var(--font-arabic); font-size: 1.5rem; color: #FFFFFF; font-weight: 500; margin: 0.35rem 0 1rem;">مجوهرات وألماس</h3>
              <a href="#" style="color: #FFFFFF; font-size: 0.8125rem; text-transform: uppercase; letter-spacing: 0.1em; border-bottom: 1px solid var(--luxury-accent); width: fit-content; padding-bottom: 0.2rem;">اكتشف المجموعة &larr;</a>
            </div>
          </div>
        </div>
      </div>
    </section>

    <section class="lux-section">
      <div class="lux-container">
        <div class="lux-section-header">
          <span class="lux-section-tag">مختارات الموسم</span>
          <h2 class="lux-section-title">القطع الأكثر تميزاً</h2>
        </div>
        <div class="lux-product-grid">
          <article class="lux-card">
            <div class="lux-card-media">
              <img src="https://images.unsplash.com/photo-1522335789203-aabd1fc54bc9?q=80&w=600&auto=format&fit=crop" class="lux-card-img">
              <span class="lux-card-badge">إصدار خاص</span>
            </div>
            <div class="lux-card-body">
              <div>
                <h3 class="lux-card-title">عطر العود الملكي النادر</h3>
                <p class="lux-card-sub">عطور نيش حصرية</p>
              </div>
              <div class="lux-card-footer">
                <span class="lux-card-price">١٬٢٥٠ ر.س</span>
                <button type="button" class="lux-btn-pill">إضافة للسلة</button>
              </div>
            </div>
          </article>
          <article class="lux-card">
            <div class="lux-card-media">
              <img src="https://images.unsplash.com/photo-1523275335684-37898b6baf30?q=80&w=600&auto=format&fit=crop" class="lux-card-img">
              <span class="lux-card-badge">مختارات</span>
            </div>
            <div class="lux-card-body">
              <div>
                <h3 class="lux-card-title">ساعة كرونوغراف إصدار محدود</h3>
                <p class="lux-card-sub">ساعات راقية</p>
              </div>
              <div class="lux-card-footer">
                <span class="lux-card-price">٣٬٤٠٠ ر.س</span>
                <button type="button" class="lux-btn-pill">إضافة للسلة</button>
              </div>
            </div>
          </article>
          <article class="lux-card">
            <div class="lux-card-media">
              <img src="https://images.unsplash.com/photo-1548036328-c9fa89d128fa?q=80&w=600&auto=format&fit=crop" class="lux-card-img">
              <span class="lux-card-badge">جديد</span>
            </div>
            <div class="lux-card-body">
              <div>
                <h3 class="lux-card-title">حقيبة يد جلد طبيعي محبوك</h3>
                <p class="lux-card-sub">مصنوعات جلدية</p>
              </div>
              <div class="lux-card-footer">
                <span class="lux-card-price">٢٬١٠٠ ر.س</span>
                <button type="button" class="lux-btn-pill">إضافة للسلة</button>
              </div>
            </div>
          </article>
          <article class="lux-card">
            <div class="lux-card-media">
              <img src="https://images.unsplash.com/photo-1599643478518-a784e5dc4c8f?q=80&w=600&auto=format&fit=crop" class="lux-card-img">
              <span class="lux-card-badge">حرفية يدوية</span>
            </div>
            <div class="lux-card-body">
              <div>
                <h3 class="lux-card-title">قلادة ذهب عيار ١٨ مرصعة</h3>
                <p class="lux-card-sub">مجوهرات راقية</p>
              </div>
              <div class="lux-card-footer">
                <span class="lux-card-price">٤٬٨٠٠ ر.س</span>
                <button type="button" class="lux-btn-pill">إضافة للسلة</button>
              </div>
            </div>
          </article>
        </div>
      </div>
    </section>

    <section style="background: #0D0D0D; color: #FFFFFF; padding: 6rem 0;">
      <div class="lux-container">
        <div style="display: grid; grid-template-columns: 1fr 1fr; gap: 4rem; align-items: center;">
          <div>
            <span style="font-size: 0.75rem; color: var(--luxury-accent); letter-spacing: 0.2em; text-transform: uppercase; margin-bottom: 0.75rem; display: block;">قصة الدار</span>
            <h2 style="font-family: var(--font-arabic); font-size: 2.75rem; font-weight: 300; line-height: 1.3; margin-bottom: 1.5rem;">
              أصالة الحرفة مع <strong>روح العصر</strong>
            </h2>
            <p style="color: #BDB9B0; font-size: 1rem; line-height: 1.8; margin-bottom: 2rem;">
              نبتكر قطعاً فنية فريدة تعكس أعلى درجات الإتقان والتميز. كل تصميم يحكي قصة إبداع تبدأ من اختيار أنقى الخامات وتمر بأنامل أمهر الحرفيين لتصل إليك بمثالية لا تضاهى.
            </p>
            <a href="#" class="lux-cta-btn" style="padding: 0.9rem 2.25rem;">اقرأ المزيد عن الدار &larr;</a>
          </div>
          <div style="border: 1px solid rgba(197, 160, 89, 0.3); padding: 1rem;">
            <img src="https://images.unsplash.com/photo-1441986300917-64674bd600d8?q=80&w=800&auto=format&fit=crop" style="width: 100%; height: 420px; object-fit: cover;">
          </div>
        </div>
      </div>
    </section>
  </main>

  <footer role="contentinfo" class="lux-footer">
    <div class="lux-container">
      <div class="lux-footer-grid">
        <div class="lux-footer-brand">
          <h3>المتجر الفاخر برو</h3>
          <p>وجهتك الأولى لأرقى المجموعات الحصرية المصنوعة بأعلى معايير الحرفية والرفاهية.</p>
        </div>
        <div class="lux-footer-col">
          <h4>خدمة العملاء</h4>
          <ul class="lux-footer-links">
            <li><a href="#">تتبع الطلب</a></li>
            <li><a href="#">سياسة الشحن</a></li>
            <li><a href="#">الإرجاع والاستبدال</a></li>
          </ul>
        </div>
        <div class="lux-footer-col">
          <h4>الدفع الموثوق</h4>
          <p style="font-size: 0.8125rem; color: #9C9890; line-height: 1.6; margin-bottom: 1.25rem;">
            جميع المعاملات مشفرة ومحمية ببروتوكولات الأمان المعتمدة في منصة سلة.
          </p>
          <div style="font-size: 0.72rem; color: var(--luxury-accent-light); letter-spacing: 0.08em; font-weight: 500;">
            MADA · VISA · MASTERCARD · APPLE PAY
          </div>
        </div>
      </div>
      <div class="lux-footer-bottom">
        <p>&copy; 2026 المتجر الفاخر برو. جميع الحقوق محفوظة.</p>
        <p>Luxury Pro · Powered by Salla Twilight</p>
      </div>
    </div>
  </footer>
</body>
</html>
"""

preview_file = repo_root / "screenshots" / "rendered_preview.html"
preview_file.write_text(rendered_html, encoding="utf-8")
print(f"Rendered HTML written to {preview_file}")
