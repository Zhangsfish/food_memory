from __future__ import annotations

import sys
import tempfile
import unittest
from pathlib import Path

import yaml

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


class ContractTests(unittest.TestCase):
    def test_valid_record_builds_two_retrieval_axes(self) -> None:
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp)
            path = root / "data" / "2026" / "sample.md"
            path.parent.mkdir(parents=True)
            path.write_text(SAMPLE, encoding="utf-8")

            records = collect_records(root)
            self.assertEqual(len(records), 1)

            catalog = build(root)
            self.assertEqual(catalog["record_count"], 1)
            self.assertEqual(catalog["authors"][0]["author"], "github:example")
            self.assertEqual(catalog["places"][0]["area"], "CN/石家庄")

            author_manifest = root / catalog["authors"][0]["manifest"]
            place_manifest = root / catalog["places"][0]["manifest"]
            self.assertTrue(author_manifest.exists())
            self.assertTrue(place_manifest.exists())

            text = (root / "indexes").read_text if False else None
            author_part = yaml.safe_load(author_manifest.read_text(encoding="utf-8"))
            part_path = root / author_part["partitions"][0]["path"]
            row = part_path.read_text(encoding="utf-8")
            self.assertIn("sweeter than I prefer", row)
            self.assertIn('"source_path": "data/2026/sample.md"', row)

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
