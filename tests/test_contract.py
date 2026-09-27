from __future__ import annotations

import json
import sys
import tempfile
import unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "scripts"))

from build_indexes import build
from validate import RecordError, collect_records


SAMPLE = """---
schema_version: 1
id: exp_20260924_test_example_01
author: github:example
date: "2026-09-24"
place:
  id: place_example_noodles
  name: Example Noodle Shop
  area: CN/石家庄
  hint: Example mall
dishes:
  - Beef noodles
cost:
  amount: 28
  currency: CNY
  basis: my_share
local_relation: visitor
commercial_relationship: none_declared
---

The noodles were good, but the broth was sweeter than I prefer.
"""

SECOND_VISIT = SAMPLE.replace(
    "exp_20260924_test_example_01",
    "exp_20261001_test_example_02",
).replace(
    'date: "2026-09-24"',
    'date: "2026-10-01"',
)


class ContractTests(unittest.TestCase):
    def test_repeated_place_builds_place_time_and_area_indexes(self) -> None:
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp)
            data = root / "data" / "2026"
            data.mkdir(parents=True)

            (data / "a.md").write_text(SAMPLE, encoding="utf-8")
            (data / "b.md").write_text(SECOND_VISIT, encoding="utf-8")

            records = collect_records(root)
            self.assertEqual(len(records), 2)

            catalog = build(root)

            self.assertEqual(catalog["record_count"], 2)
            self.assertEqual(len(catalog["places"]), 1)
            self.assertEqual(catalog["places"][0]["record_count"], 2)
            self.assertEqual(catalog["areas"][0]["area"], "CN/石家庄")
            self.assertEqual(len(catalog["time"]["partitions"]), 2)

            place_manifest_path = root / catalog["places"][0]["manifest"]
            place_manifest = json.loads(
                place_manifest_path.read_text(encoding="utf-8")
            )

            self.assertEqual(place_manifest["place_id"], "place_example_noodles")
            self.assertEqual(place_manifest["record_count"], 2)
            self.assertEqual(len(place_manifest["partitions"]), 2)

            first_partition = root / place_manifest["partitions"][0]["path"]
            text = first_partition.read_text(encoding="utf-8")
            self.assertIn("sweeter than I prefer", text)
            self.assertIn('"source_path": "data/2026/a.md"', text)

    def test_place_id_is_optional_and_fallback_key_is_generated(self) -> None:
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp)
            path = root / "data" / "2026" / "sample.md"
            path.parent.mkdir(parents=True)

            without_id = SAMPLE.replace("  id: place_example_noodles\n", "")
            path.write_text(without_id, encoding="utf-8")

            catalog = build(root)

            self.assertEqual(len(catalog["places"]), 1)
            self.assertTrue(catalog["places"][0]["place_key"].startswith("auto-"))
            self.assertIsNone(catalog["places"][0]["place_id"])

    def test_duplicate_ids_are_rejected(self) -> None:
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp)
            data = root / "data" / "2026"
            data.mkdir(parents=True)

            (data / "a.md").write_text(SAMPLE, encoding="utf-8")
            (data / "b.md").write_text(SAMPLE, encoding="utf-8")

            with self.assertRaises(RecordError):
                collect_records(root)


if __name__ == "__main__":
    unittest.main()
