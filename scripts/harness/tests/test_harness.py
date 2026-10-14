#!/usr/bin/env python3
"""
Unit tests for Salla Twilight Verification Harness
"""

import sys
import json
import shutil
import tempfile
import unittest
from pathlib import Path

# Add scripts/harness to sys.path
HARNESS_DIR = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(HARNESS_DIR))

from validate_theme import ThemeValidator
from inspect_env import EnvironmentInspector
from salla_harness import SallaHarness


class TestSallaHarness(unittest.TestCase):
    def setUp(self):
        self.theme_root = HARNESS_DIR.parent.parent

    def test_validator_on_active_theme(self):
        validator = ThemeValidator(self.theme_root)
        valid, summary = validator.run()
        self.assertTrue(valid, f"Active theme validation failed: {summary.get('errors')}")
        self.assertEqual(len(summary.get("errors", [])), 0)
        self.assertGreaterEqual(len(summary.get("passed_checks", [])), 10)

    def test_validator_detects_missing_twilight_json(self):
        with tempfile.TemporaryDirectory() as tmpdir:
            tmp_path = Path(tmpdir)
            validator = ThemeValidator(tmp_path)
            valid, summary = validator.run()
            self.assertFalse(valid)
            self.assertTrue(any("twilight.json not found" in err for err in summary.get("errors", [])))

    def test_validator_detects_missing_component_file(self):
        with tempfile.TemporaryDirectory() as tmpdir:
            tmp_path = Path(tmpdir)
            # Create minimal twilight.json with missing component
            tj = {
                "name": {"ar": "تجربة", "en": "Test"},
                "author_email": "test@example.com",
                "components": [
                    {"name": "ghost_component", "path": "home.non_existent_file"}
                ]
            }
            (tmp_path / "twilight.json").write_text(json.dumps(tj), encoding="utf-8")
            views_dir = tmp_path / "src" / "views" / "pages"
            views_dir.mkdir(parents=True)
            (views_dir / "index.twig").write_text("{% component home %}", encoding="utf-8")
            layout_dir = tmp_path / "src" / "views" / "layouts"
            layout_dir.mkdir(parents=True)
            (layout_dir / "master.twig").write_text("{% hook head %}{% hook 'body:end' %}{{ 'app.css' | asset }}", encoding="utf-8")

            validator = ThemeValidator(tmp_path)
            valid, summary = validator.run()
            self.assertFalse(valid)
            self.assertTrue(any("physical file missing" in err for err in summary.get("errors", [])))

    def test_validator_detects_banned_functions(self):
        with tempfile.TemporaryDirectory() as tmpdir:
            tmp_path = Path(tmpdir)
            tj = {
                "name": {"ar": "تجربة", "en": "Test"},
                "author_email": "test@example.com",
                "components": []
            }
            (tmp_path / "twilight.json").write_text(json.dumps(tj), encoding="utf-8")
            views_dir = tmp_path / "src" / "views" / "pages"
            views_dir.mkdir(parents=True)
            (views_dir / "index.twig").write_text("{% component home %}{{ salla_header() }}", encoding="utf-8")
            layout_dir = tmp_path / "src" / "views" / "layouts"
            layout_dir.mkdir(parents=True)
            (layout_dir / "master.twig").write_text("{% hook head %}{% hook 'body:end' %}{{ 'app.css' | asset }}", encoding="utf-8")

            validator = ThemeValidator(tmp_path)
            valid, summary = validator.run()
            self.assertFalse(valid)
            self.assertTrue(any("Banned Twig function 'salla_header()'" in err for err in summary.get("errors", [])))

    def test_env_inspector_finds_cli(self):
        inspector = EnvironmentInspector(self.theme_root)
        inspector.inspect_cli()
        self.assertIsNotNone(inspector.details.get("cli_version"))
        self.assertNotEqual(inspector.details.get("cli_version"), "unknown")

    def test_matrix_evaluation_states(self):
        harness = SallaHarness(self.theme_root)
        val_pass = {"valid": True, "errors": [], "passed_checks": []}
        build_pass = {"valid": True, "errors": [], "passed_checks": []}
        env_pass = {
            "valid": True,
            "errors": [],
            "details": {
                "authenticated": True,
                "registered_themes": [{"id": "123", "name": "Theme", "status": "dev"}],
                "preview_daemon_active": False,
            }
        }
        git_pass = {"valid": True, "errors": [], "warnings": []}

        report = harness.evaluate_matrix(val_pass, build_pass, env_pass, git_pass)
        self.assertEqual(report["overall_status"], "READY_FOR_PREVIEW")
        self.assertEqual(report["matrix"]["1_SYNTAX_VALID"]["status"], "PASS")
        self.assertEqual(report["matrix"]["7_STORE_VERIFIED"]["status"], "PENDING_CONFIRMATION")


if __name__ == "__main__":
    unittest.main()
