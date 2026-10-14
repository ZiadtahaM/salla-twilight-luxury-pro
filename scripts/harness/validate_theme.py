#!/usr/bin/env python3
"""
Salla Twilight Static Theme Validator
Verifies twilight.json schema, component paths, Twig hooks, and banned functions.
"""

import sys
import json
from pathlib import Path
from typing import Dict, List, Any, Tuple


class ThemeValidator:
    def __init__(self, theme_root: Path):
        self.theme_root = theme_root.resolve()
        self.errors: List[str] = []
        self.warnings: List[str] = []
        self.checks_passed: List[str] = []

    def validate_twilight_json(self) -> Dict[str, Any]:
        twilight_path = self.theme_root / "twilight.json"
        if not twilight_path.exists():
            self.errors.append("twilight.json not found at theme root")
            return {}

        try:
            with open(twilight_path, "r", encoding="utf-8") as f:
                data = json.load(f)
        except json.JSONDecodeError as exc:
            self.errors.append(f"twilight.json invalid JSON: {exc}")
            return {}

        self.checks_passed.append("twilight.json is valid JSON")

        # Required fields
        if "name" not in data:
            self.errors.append("twilight.json missing required root field: 'name'")
        else:
            self.checks_passed.append("twilight.json contains 'name'")

        if "author" not in data and "author_email" not in data:
            self.errors.append("twilight.json missing required root field: 'author' or 'author_email'")
        else:
            self.checks_passed.append("twilight.json contains author information")

        if "name" in data and isinstance(data["name"], dict):
            if not data["name"].get("ar") or not data["name"].get("en"):
                self.warnings.append("twilight.json name should have both 'ar' and 'en' keys")

        # Validate components
        components = data.get("components", [])
        if not isinstance(components, list):
            self.errors.append("twilight.json 'components' must be an array")
        else:
            self.checks_passed.append(f"twilight.json declares {len(components)} components")
            for idx, comp in enumerate(components):
                comp_name = comp.get("name") or comp.get("key") or f"component_{idx}"
                path_str = comp.get("path")
                if not path_str:
                    self.errors.append(f"Component '{comp_name}' missing required 'path'")
                    continue

                # Map dot path to physical file
                rel_file = path_str.replace(".", "/") + ".twig"
                phys_path = self.theme_root / "src" / "views" / "components" / rel_file
                if not phys_path.exists():
                    self.errors.append(
                        f"Component '{comp_name}' declares path '{path_str}', but physical file missing: {phys_path.relative_to(self.theme_root)}"
                    )
                else:
                    self.checks_passed.append(f"Component '{path_str}' verified at {phys_path.name}")

        return data

    def validate_twig_templates(self) -> None:
        views_dir = self.theme_root / "src" / "views"
        if not views_dir.exists():
            self.errors.append("src/views directory not found")
            return

        # Check index.twig
        index_twig = views_dir / "pages" / "index.twig"
        if not index_twig.exists():
            self.errors.append("src/views/pages/index.twig not found")
        else:
            content = index_twig.read_text(encoding="utf-8", errors="ignore")
            if "{% component home %}" not in content and "{% component 'home' %}" not in content:
                self.errors.append("src/views/pages/index.twig missing mandatory '{% component home %}' tag")
            else:
                self.checks_passed.append("index.twig contains '{% component home %}' tag")

        # Check master.twig hooks
        master_twig = views_dir / "layouts" / "master.twig"
        if not master_twig.exists():
            self.errors.append("src/views/layouts/master.twig not found")
        else:
            m_content = master_twig.read_text(encoding="utf-8", errors="ignore")
            if "{% hook head %}" not in m_content and "{% hook 'head" not in m_content:
                self.errors.append("master.twig missing '{% hook head %}' or '{% hook head:start %}'")
            else:
                self.checks_passed.append("master.twig declares head hooks")

            if "{% hook 'body:end' %}" not in m_content and "{% hook body:end %}" not in m_content:
                self.warnings.append("master.twig should declare '{% hook body:end %}' for Salla web components")
            else:
                self.checks_passed.append("master.twig declares body:end hook")

            if "'app.css' | asset" not in m_content and '"app.css" | asset' not in m_content:
                self.warnings.append("master.twig should reference 'app.css' | asset")
            else:
                self.checks_passed.append("master.twig references app.css asset")

        # Scan for banned functions in all twig files
        banned_funcs = [
            "salla_header()",
            "salla_footer()",
            "salla_checkout_url()",
            "salla_cart_url()",
            "salla_login_url()",
        ]

        twig_files = list(views_dir.rglob("*.twig"))
        for tf in twig_files:
            text = tf.read_text(encoding="utf-8", errors="ignore")
            for banned in banned_funcs:
                if banned in text:
                    self.errors.append(f"Banned Twig function '{banned}' detected in {tf.relative_to(self.theme_root)}")

    def validate_public_directory(self) -> None:
        public_dir = self.theme_root / "public"
        if not public_dir.exists():
            self.warnings.append("public/ directory does not exist. Run build before deployment.")
            return

        # Check gitignore
        gitignore_path = self.theme_root / ".gitignore"
        if gitignore_path.exists():
            gi_content = gitignore_path.read_text(encoding="utf-8", errors="ignore")
            for line in gi_content.splitlines():
                stripped = line.strip()
                if stripped in ["public", "public/", "/public", "/public/"]:
                    self.errors.append("CRITICAL: public/ is gitignored in .gitignore. Salla requires public/ committed to git.")

    def run(self) -> Tuple[bool, Dict[str, Any]]:
        self.validate_twilight_json()
        self.validate_twig_templates()
        self.validate_public_directory()

        is_valid = len(self.errors) == 0
        summary = {
            "valid": is_valid,
            "errors": self.errors,
            "warnings": self.warnings,
            "passed_checks": self.checks_passed,
        }
        return is_valid, summary


def main():
    root = Path.cwd()
    if len(sys.argv) > 1:
        root = Path(sys.argv[1])

    validator = ThemeValidator(root)
    valid, summary = validator.run()

    print("=" * 60)
    print(" SALLA TWILIGHT STATIC THEME VALIDATOR")
    print("=" * 60)
    print(f"Target Theme Root: {validator.theme_root}")
    print()

    if summary["passed_checks"]:
        print(f"Passed Checks ({len(summary['passed_checks'])}):")
        for check in summary["passed_checks"]:
            print(f"  [PASS] {check}")
        print()

    if summary["warnings"]:
        print(f"Warnings ({len(summary['warnings'])}):")
        for w in summary["warnings"]:
            print(f"  [WARN] {w}")
        print()

    if summary["errors"]:
        print(f"Errors ({len(summary['errors'])}):")
        for err in summary["errors"]:
            print(f"  [FAIL] {err}")
        print()
        print("Verdict: REJECTED (Static validation failed)")
        sys.exit(1)
    else:
        print("Verdict: PASSED (Static validation succeeded)")
        sys.exit(0)


if __name__ == "__main__":
    main()
