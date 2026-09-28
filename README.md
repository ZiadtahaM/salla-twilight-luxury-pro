# Salla Twilight Luxury Pro Theme

Production-grade bespoke Salla Pro theme engineered with Salla Twilight Engine, Twig, and modern CSS architecture.

## Repository Overview
- `twilight.json`: Official theme configuration and merchant component registry.
- `src/views/layouts/master.twig`: Accessible, bilingual root layout with Salla header and footer lifecycle hooks.
- `src/views/pages/`: Page templates (home, products, collections, cart, checkout, customer profile).
- `src/views/components/`: Modular, isolated Twig components editable via Salla Theme Editor.
- `.github/workflows/twilight-ci.yml`: Deterministic validation pipeline for schema and markup invariants.
- `SPEC.md`: Architectural specification and acceptance criteria.
- `AUDIT_RUBRIC.md`: Technical triage methodology for reviewing existing code assets.

## Salla CLI Workflow
```bash
# Authenticate with Salla Partners
salla login

# Preview theme in demo store
salla theme preview

# Watch local changes
salla theme watch
```

## Quality Assurance & Verification
Run local validation checks:
```bash
node .github/workflows/twilight-ci.yml
```
