#!/usr/bin/env python3
from __future__ import annotations

import argparse
import hashlib
import json
import re
import shutil
from collections import defaultdict
from pathlib import Path
from typing import Any

from validate import collect_records


def dump_json(path: Path, value: Any) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(
        json.dumps(value, ensure_ascii=False, indent=2, sort_keys=True) + "\n",
        encoding="utf-8",
    )


def safe_author_dir(author: str) -> str:
    base = re.sub(r"[^A-Za-z0-9._-]+", "-", author).strip("-") or "author"
    digest = hashlib.sha1(author.encode("utf-8")).hexdigest()[:8]
    return f"{base}--{digest}"


def date_partition(date: str) -> str:
    if date == "unknown":
        return "undated"
    if len(date) >= 7:
        return date[:7]
    return date[:4]


def normalize_record(root: Path, path: Path, meta: dict[str, Any], body: str) -> dict[str, Any]:
    row: dict[str, Any] = {
        "id": meta["id"],
        "author": meta["author"],
        "date": meta["date"],
        "place": meta["place"],
        "dishes": meta["dishes"],
        "experience_text": body,
        "source_path": path.relative_to(root).as_posix(),
    }
    for key in (
        "cost",
        "local_relation",
        "commercial_relationship",
        "attachments",
    ):
        if key in meta:
            row[key] = meta[key]
    return row


def write_group(
    index_root: Path,
    group_dir: Path,
    key_name: str,
    key_value: str,
    rows: list[dict[str, Any]],
) -> str:
    partitions: dict[str, list[dict[str, Any]]] = defaultdict(list)
    for row in rows:
        partitions[date_partition(row["date"])].append(row)

    manifest_parts = []
    for period in sorted(partitions):
        part_rows = sorted(
            partitions[period], key=lambda r: (r["date"], r["id"])
        )
        part_path = group_dir / f"{period}.jsonl"
        part_path.parent.mkdir(parents=True, exist_ok=True)
        with part_path.open("w", encoding="utf-8", newline="\n") as handle:
            for row in part_rows:
                handle.write(
                    json.dumps(row, ensure_ascii=False, sort_keys=True) + "\n"
                )

        manifest_parts.append(
            {
                "period": period,
                "count": len(part_rows),
                "path": part_path.relative_to(index_root.parent).as_posix(),
            }
        )

    manifest_path = group_dir / "manifest.json"
    dump_json(
        manifest_path,
        {
            "schema_version": 1,
            key_name: key_value,
            "record_count": len(rows),
            "partitions": manifest_parts,
        },
    )
    return manifest_path.relative_to(index_root.parent).as_posix()


def build(root: Path) -> dict[str, Any]:
    records = collect_records(root)
    index_root = root / "indexes"

    if index_root.exists():
        shutil.rmtree(index_root)
    index_root.mkdir(parents=True, exist_ok=True)

    by_author: dict[str, list[dict[str, Any]]] = defaultdict(list)
    by_place: dict[str, list[dict[str, Any]]] = defaultdict(list)

    for path, meta, body in records:
        row = normalize_record(root, path, meta, body)
        by_author[row["author"]].append(row)
        by_place[row["place"]["area"]].append(row)

    author_catalog = []
    for author in sorted(by_author):
        group_dir = index_root / "by-author" / safe_author_dir(author)
        manifest = write_group(
            index_root, group_dir, "author", author, by_author[author]
        )
        author_catalog.append(
            {
                "author": author,
                "record_count": len(by_author[author]),
                "manifest": manifest,
            }
        )

    place_catalog = []
    for area in sorted(by_place):
        segments = area.split("/")
        group_dir = index_root / "by-place"
        for segment in segments:
            group_dir = group_dir / segment
        manifest = write_group(
            index_root, group_dir, "area", area, by_place[area]
        )
        place_catalog.append(
            {
                "area": area,
                "record_count": len(by_place[area]),
                "manifest": manifest,
            }
        )

    catalog = {
        "schema_version": 1,
        "record_count": len(records),
        "authors": author_catalog,
        "places": place_catalog,
        "note": "Generated mechanically from data/. No AI summaries.",
    }
    dump_json(index_root / "catalog.json", catalog)
    return catalog


def main() -> int:
    parser = argparse.ArgumentParser(description="Rebuild AI-readable indexes")
    parser.add_argument(
        "--root",
        type=Path,
        default=Path(__file__).resolve().parents[1],
        help="repository root",
    )
    args = parser.parse_args()

    catalog = build(args.root)
    print(
        "INDEX BUILD PASSED: "
        f"{catalog['record_count']} record(s), "
        f"{len(catalog['authors'])} author(s), "
        f"{len(catalog['places'])} place area(s)"
    )
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
