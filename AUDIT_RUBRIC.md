# Salla Twilight Legacy Code Triage & Audit Rubric

## Purpose
This document governs the technical assessment of existing files and prototypes provided by the store owner (Naif A.) to prevent regressions and determine what can be reused versus rebuilt.

## Triage Assessment Matrix

| Layer | Inspection Criteria | Decision Rule: Retain | Decision Rule: Refactor | Decision Rule: Rebuild |
| :--- | :--- | :--- | :--- | :--- |
| **Twig Layouts** | Presence of Salla hooks (`salla_header`, `salla_footer`), semantic tags | Uses official Salla Twig filters (`money`, `trans`) and clean block inheritance | Missing localization or hardcoded strings, but structure is sound | Omits Salla core hooks or breaks platform scripts |
| **Web Components** | `<salla-product-card>`, `<salla-cart-summary>`, button triggers | Custom styling applied via CSS variables or wrapper classes without touching internal DOM | Component events attached correctly, but styling lacks luxury polish | Native components replaced with brittle custom jQuery or vanilla JS AJAX calls |
| **twilight.json** | Root keys, component schema declarations, field stability | Clean typed schema with proper default values and localization | Minor key naming inconsistencies or missing required validation | Corrupted JSON or unstructured configuration lacking merchant editor mapping |
| **CSS / Styling** | Design system tokens, RTL logical properties (`padding-inline`, `margin-inline`) | Clean scoped CSS or utility classes using CSS variables | Hardcoded `left`/`right` properties requiring conversion to logical properties | Massive unminified monolithic CSS with hundreds of `!important` overrides |
| **Performance** | Asset sizes, image loading attributes (`loading="lazy"`), render-blocking resources | Modern WebP/AVIF images with explicit width and height attributes | Images lack responsive breakpoints, easily patchable with `<picture>` tags | Massive client-side JS libraries injected directly into theme head |

## Action Protocol
1. **Cataloging**: Every legacy file is cloned into a quarantined audit branch (`audit/legacy-baseline`).
2. **Deterministic Run**: Execute `node` invariant checks against existing Twig and JSON files.
3. **Written Report**: Deliver a 1-page triage ledger to the store owner listing:
   - Green (100% reusable as-is)
   - Yellow (Refactored to meet Twilight standards)
   - Red (Rebuilt from scratch due to architectural violation)
