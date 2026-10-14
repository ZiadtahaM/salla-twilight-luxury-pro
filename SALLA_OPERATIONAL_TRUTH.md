# Salla Twilight Theme Architecture and Operational Truth

## 1. Executive Grounding

Salla is not an open static site host or standard fullstack web service where an automated agent can unilaterally push code, restart a service, and verify live storefront changes. Salla is an enterprise cloud commerce platform. The platform enforces strict authentication, proprietary template parsing, server-side component registration, and private merchant database state.

AI coding assistants can generate Twig templates, write SCSS, configure Webpack, and validate JSON schemas. However, an AI agent cannot directly manipulate Salla cloud databases, install themes onto private demo stores without partner credentials, or interact with the browser-based Salla visual customizer unless authenticated human confirmation is provided.

Claiming that local file creation or local webpack compilation represents a completed Salla theme deployment is false. Every development step must be evaluated against physical platform boundaries.

## 2. Unidirectional Architectural Model

The platform enforces a unidirectional dependency hierarchy:

```text
+--------------------------------------------------------+
| 1. Salla Partners Portal                               |
|    - Theme Registration (Theme ID)                     |
|    - Demo Store Association                            |
|    - Component Metadata Registration                   |
|    - Theme Version and Marketplace Publishing          |
+---------------------------+----------------------------+
                            |
                            v
+--------------------------------------------------------+
| 2. GitHub Remote Repository                            |
|    - Canonical Version Control                         |
|    - Public Assets Branch (public/ committed)          |
|    - Webhook Sync to Salla Partners                    |
+---------------------------+----------------------------+
                            |
                            v
+--------------------------------------------------------+
| 3. Local Theme Workspace                               |
|    - twilight.json Specification                       |
|    - Twig Templates (src/views/)                       |
|    - SCSS and JavaScript Source (src/assets/)          |
|    - Webpack Compilation into public/                  |
+---------------------------+----------------------------+
                            |
                            v
+--------------------------------------------------------+
| 4. Salla CLI Streaming Preview                         |
|    - Draft Creation (salla theme preview)              |
|    - Local Asset Server (localhost:8000)               |
|    - WebSocket Reload Relay (localhost:8001)           |
+---------------------------+----------------------------+
                            |
                            v
+--------------------------------------------------------+
| 5. Demo Store Visual Customizer and Storefront         |
|    - Merchant Cloud Database                           |
|    - Section Customizer (Add Section Sidebar)          |
|    - Twilight Server-Side Twig Rendering Engine        |
|    - Salla Web Components (<salla-product-card>, etc.) |
+--------------------------------------------------------+
```

Local code edits at level 3 have zero effect on level 5 until level 2 and level 1 are synchronized and the demo store database updates its active schema.

## 3. The Five Verification Layers

Every theme deliverable must be verified through five independent layers:

### Layer 1: Code and Syntax Integrity
All local files must strictly conform to Salla Twilight specifications. The `twilight.json` file must parse without syntax errors. Every component path declared in `twilight.json` must map to a physical `.twig` template on disk. Twig templates must use valid Salla tags. Banned functions such as `salla_header()` or `salla_footer()` are prohibited. Master layouts must declare mandatory lifecycle hooks including `{% hook head %}` and `{% hook 'body:end' %}`. The homepage `index.twig` must contain only `{% component home %}` within its content block to avoid breaking the customizer injection pipeline.

### Layer 2: Asset Build and Packaging
The build system must execute in production mode with zero errors. Webpack must compile SCSS into `public/app.css` and JavaScript into `public/app.js` and `public/home.js`. The `public/` directory must never be added to `.gitignore`, because Salla servers pull precompiled assets directly from git.

### Layer 3: Remote Repository Synchronization
Because Salla Partners integrates with GitHub to fetch theme releases and components, local commits must be pushed to `origin/main`. If local changes remain unpushed, Salla cloud infrastructure cannot detect them regardless of local CLI preview activity.

### Layer 4: Salla Cloud Registration and Database State
The theme ID must be verified in the Salla Partners account. The active demo store must have the theme installed. When new components or settings are introduced into `twilight.json`, the merchant or developer must trigger an update on the demo store through the Salla Partners Portal so the cloud database reflects the new schema.

### Layer 5: Visual Customizer and Runtime Storefront
The Salla Theme Editor must load without critical console errors. The left sidebar must display the section list and the add section button. Adding a custom component must render the preview iframe without crashing. Salla web components must load their live attributes.

## 4. Absolute Operational Prohibitions

1. Never report a theme as deployed, installed, or functioning on Salla based solely on local compilation or passing unit tests.
2. Never assume that editing `twilight.json` immediately alters the Salla editor UI without checking whether the demo store database has reloaded the schema.
3. Never insert hardcoded layout sections into `index.twig` alongside `{% component home %}`. This conflicts with Salla's visual editor parser.
4. Never place `public/` inside `.gitignore`. Salla does not run build scripts on its servers.
5. Never commit credentials, OAuth tokens, or live auto-login URLs containing access tokens to public repositories or logs.

## 5. Ubiquitous Language Glossary

- Twilight Engine: Salla proprietary server-side rendering environment executing Twig templates and serving web components.
- Theme ID: The unique numeric identifier assigned by Salla Partners upon theme creation.
- twilight.json: The declarative configuration file defining theme metadata, global settings, and merchant-customizable components.
- Component Path: The dot-separated reference in twilight.json mapping to a file under `src/views/components/`. For example, `home.luxury-hero-banner` maps to `src/views/components/home/luxury-hero-banner.twig`.
- Demo Store: An ephemeral or permanent test store assigned to a partner account for development and visual customizer testing.
- Preview Session: A temporary authenticated draft session established by Salla CLI combining local asset proxying with remote Twilight rendering.
- Visual Customizer: The browser-based theme customizer where merchants arrange sections, edit typography, and configure colors.
