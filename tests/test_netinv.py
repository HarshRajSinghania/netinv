"""Unit tests for netinv. Standard library only: run with `python -m unittest`.

These tests never touch the network.
"""

from __future__ import annotations

import csv
import io
import json
import sys
import unittest
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent.parent / "app"))

from netinv.arp import normalize_mac, parse_arp_a, parse_proc_net_arp  # noqa: E402
from netinv.cli import build_parser  # noqa: E402
from netinv.exporters import EXPORTERS, format_from_path  # noqa: E402
from netinv.i18n import Translator, available_languages  # noqa: E402
from netinv.models import HOST_FIELDS, Host  # noqa: E402
from netinv.ports import parse_ports, service_name  # noqa: E402
from netinv.scanner import expand_targets  # noqa: E402
from netinv.vendor import (  # noqa: E402
    _parse_oui_lines,
    is_locally_administered,
    load_oui_table,
    lookup_vendor,
)

LOCALES = Path(__file__).resolve().parent.parent / "app" / "netinv" / "locales"


class TestPorts(unittest.TestCase):
    def test_single_and_ranges(self):
        self.assertEqual(parse_ports("22, 80,8000-8002"), [22, 80, 8000, 8001, 8002])

    def test_duplicates_and_empty_chunks(self):
        self.assertEqual(parse_ports("80,,80,22"), [22, 80])

    def test_invalid(self):
        for bad in ("0", "65536", "90-80", "abc"):
            with self.subTest(bad=bad), self.assertRaises(ValueError):
                parse_ports(bad)

    def test_service_name(self):
        self.assertEqual(service_name(22), "ssh")
        self.assertEqual(service_name(12345), "?")


class TestTargets(unittest.TestCase):
    def test_cidr(self):
        ips = expand_targets("192.168.1.0/30")
        self.assertEqual(ips, ["192.168.1.1", "192.168.1.2"])

    def test_single_and_range(self):
        self.assertEqual(
            expand_targets("10.0.0.5,10.0.0.1-3"),
            ["10.0.0.5", "10.0.0.1", "10.0.0.2", "10.0.0.3"],
        )

    def test_duplicates_removed(self):
        self.assertEqual(expand_targets("10.0.0.1,10.0.0.1"), ["10.0.0.1"])

    def test_max_hosts(self):
        with self.assertRaises(ValueError):
            expand_targets("10.0.0.0/16", max_hosts=100)

    def test_invalid(self):
        for bad in ("10.0.0.300", "10.0.0.50-10", "fe80::/64"):
            with self.subTest(bad=bad), self.assertRaises(ValueError):
                expand_targets(bad)


class TestArp(unittest.TestCase):
    def test_normalize_mac(self):
        self.assertEqual(normalize_mac("AA-B-0C-1-2-3"), "aa:0b:0c:01:02:03")
        with self.assertRaises(ValueError):
            normalize_mac("aa:bb")

    def test_proc_net_arp(self):
        text = (
            "IP address       HW type     Flags       HW address            Mask     Device\n"
            "192.168.1.1      0x1         0x2         aa:bb:cc:dd:ee:01     *        eth0\n"
            "192.168.1.9      0x1         0x0         00:00:00:00:00:00     *        eth0\n"
        )
        self.assertEqual(parse_proc_net_arp(text), {"192.168.1.1": "aa:bb:cc:dd:ee:01"})

    def test_arp_a_windows(self):
        text = (
            "Interface: 192.168.1.20 --- 0x5\n"
            "  192.168.1.1           aa-bb-cc-dd-ee-01     dynamic\n"
            "  192.168.1.255         ff-ff-ff-ff-ff-ff     static\n"
        )
        self.assertEqual(parse_arp_a(text), {"192.168.1.1": "aa:bb:cc:dd:ee:01"})

    def test_arp_a_macos(self):
        text = "? (192.168.1.1) at aa:bb:cc:d:e:1 on en0 ifscope [ethernet]\n"
        self.assertEqual(parse_arp_a(text), {"192.168.1.1": "aa:bb:cc:0d:0e:01"})


class TestVendor(unittest.TestCase):
    def test_builtin_table_is_valid(self):
        table = load_oui_table()
        self.assertGreater(len(table), 0)
        for prefix in table:
            self.assertRegex(prefix, r"^[0-9A-F]{2}(:[0-9A-F]{2}){2}$")

    def test_lookup(self):
        table = _parse_oui_lines(["# comment", "", "B8:27:EB\tRaspberry Pi"])
        self.assertEqual(lookup_vendor("b8:27:eb:00:11:22", table), "Raspberry Pi")
        self.assertIsNone(lookup_vendor(None, table))
        self.assertIsNone(lookup_vendor("00:00:01:00:00:00", table))

    def test_random_mac(self):
        self.assertTrue(is_locally_administered("da:a1:19:00:00:01"))
        self.assertFalse(is_locally_administered("b8:27:eb:00:00:01"))
        self.assertEqual(lookup_vendor("da:a1:19:00:00:01", {}), "(random / private MAC)")


class TestI18n(unittest.TestCase):
    def test_all_locales_have_same_keys(self):
        reference = set(json.loads((LOCALES / "en.json").read_text(encoding="utf-8")))
        for path in LOCALES.glob("*.json"):
            with self.subTest(locale=path.name):
                keys = set(json.loads(path.read_text(encoding="utf-8")))
                self.assertEqual(keys, reference)

    def test_languages(self):
        self.assertIn("en", available_languages())
        self.assertIn("fr", available_languages())

    def test_translate_and_fallback(self):
        t = Translator("fr")
        self.assertEqual(t("col_ip"), "Adresse IP")
        self.assertEqual(t("does_not_exist"), "does_not_exist")
        self.assertEqual(Translator("xx").lang, "en")


class TestExporters(unittest.TestCase):
    def setUp(self):
        self.t = Translator("en")
        self.hosts = [
            Host(
                ip="192.168.1.1",
                alive=True,
                hostname="router.lan",
                mac="aa:bb:cc:dd:ee:01",
                vendor="Example <Corp>",
                open_ports=[22, 80],
                latency_ms=1.2,
            ),
            Host(ip="192.168.1.2", alive=True),
        ]

    def test_every_format_runs(self):
        for name, fn in EXPORTERS.items():
            with self.subTest(fmt=name):
                self.assertIn("192.168.1.1", fn(self.hosts, self.t))

    def test_csv(self):
        rows = list(csv.reader(io.StringIO(EXPORTERS["csv"](self.hosts, self.t))))
        self.assertEqual(rows[0], HOST_FIELDS)
        self.assertEqual(rows[1][HOST_FIELDS.index("open_ports")], "22 80")

    def test_json(self):
        data = json.loads(EXPORTERS["json"](self.hosts, self.t))
        self.assertEqual(len(data["hosts"]), 2)
        self.assertEqual(data["hosts"][0]["open_ports"], [22, 80])

    def test_html_is_escaped(self):
        out = EXPORTERS["html"](self.hosts, self.t)
        self.assertIn("Example &lt;Corp&gt;", out)
        self.assertNotIn("<Corp>", out)

    def test_format_from_path(self):
        self.assertEqual(format_from_path("a/report.HTM"), "html")
        self.assertEqual(format_from_path("out.txt"), "table")
        self.assertIsNone(format_from_path("noext"))


class TestCli(unittest.TestCase):
    def test_parser(self):
        args = build_parser().parse_args(["scan", "10.0.0.0/24", "-p", "22", "--no-dns"])
        self.assertEqual(args.target, "10.0.0.0/24")
        self.assertTrue(args.no_dns)


if __name__ == "__main__":
    unittest.main()
