import unittest

import importlib.util
from pathlib import Path


spec = importlib.util.spec_from_file_location("app", Path(__file__).resolve().parents[1] / "app.py")
app = importlib.util.module_from_spec(spec)
spec.loader.exec_module(app)


class GameFlowTests(unittest.TestCase):
    def test_next_question_avoids_repeats_until_deck_is_exhausted(self):
        pool = ["Q1", "Q2", "Q3"]
        used = []

        first = app.get_next_question(pool, used)
        second = app.get_next_question(pool, used)
        third = app.get_next_question(pool, used)
        fourth = app.get_next_question(pool, used)

        self.assertEqual(first, "Q1")
        self.assertEqual(second, "Q2")
        self.assertEqual(third, "Q3")
        self.assertEqual(fourth, "Q1")
        self.assertEqual(used, ["Q1", "Q2", "Q3", "Q1"])

    def test_spinner_markup_contains_fallback_wildcard(self):
        html = app.build_wildcard_spinner_html("Wild Card")

        self.assertIn("Wild Card", html)
        self.assertIn("spinner", html.lower())
        self.assertNotIn("src=\"/static/", html)


if __name__ == "__main__":
    unittest.main()
