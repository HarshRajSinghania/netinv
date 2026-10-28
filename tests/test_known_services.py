"""Focused tests for well-known service names outside the default scan list."""

from __future__ import annotations

import sys
import unittest
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent.parent / "app"))

from netinv.ports import service_name  # noqa: E402


class TestKnownServices(unittest.TestCase):
    def test_well_known_non_default_ports(self):
        self.assertEqual(service_name(3306), "mysql")
        self.assertEqual(service_name(5900), "vnc")
        self.assertEqual(service_name(6379), "redis")
        self.assertEqual(service_name(5432), "postgresql")
        self.assertEqual(service_name(1883), "mqtt")
        self.assertEqual(service_name(25), "smtp")

    def test_unknown_still_question_mark(self):
        self.assertEqual(service_name(12345), "?")


if __name__ == "__main__":
    unittest.main()
