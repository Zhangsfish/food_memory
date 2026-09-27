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


def safe_segment(value: str, fallback: str = "item") -> str:
    base = re.sub(r"[^A-Za-z0-9._-]+", "-", value).strip("-") or fallback
    digest = hashlib.sha1(value.encode("utf-8")).hexdigest()[:8]
    return f"{base[:80]}--{digest}"


def date_partition(date: str) -> str:
    if date == "unknown":
        return "undated"
    if len(date) >= 7:
        return date[:7]
    return date[:4]


def place_key(place: dict[str, Any]) -> str:
    explicit = place.get("id")
    if isinstance(explicit, str) and explicit.strip():
        return explicit.strip()

    identity = f'{place["area"]}\0{place["name"]}'
    return f"auto-{safe_segment(identity, 'place')}"


def normalize_record(
    root: Path,
    path: Path,
    meta: dict[str, Any],
    body: str,
) -> dict[str, Any]:
    place = dict(meta["place"])
    row: dict[str, Any] = {
        "id": meta["id"],
        "author": meta["author"],
        "date": meta["date"],
        "place": place,
        "place_key": place_key(place),
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
    root: Path,
    group_dir: Path,
    metadata: dict[str, Any],
    rows: list[dict[str, Any]],
) -> str:
    partitions: dict[str, list[dict[str, Any]]] = defaultdict(list)

    for row in rows:
        partitions[date_partition(row["date"])].append(row)

    manifest_parts = []

    for period in sorted(partitions):
        part_rows = sorted(
            partitions[period],
            key=lambda row: (row["date"], row["id"]),
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
                "path": part_path.relative_to(root).as_posix(),
            }
        )

    manifest_path = group_dir / "manifest.json"
    dump_json(
        manifest_path,
        {
            "schema_version": 2,
            **metadata,
            "record_count": len(rows),
            "partitions": manifest_parts,
        },
    )

    return manifest_path.relative_to(root).as_posix()


def write_time_index(
    root: Path,
    index_root: Path,
    rows: list[dict[str, Any]],
) -> dict[str, Any]:
    partitions: dict[str, list[dict[str, Any]]] = defaultdict(list)

    for row in rows:
        partitions[date_partition(row["date"])].append(row)

    result = []

    for period in sorted(partitions):
        part_rows = sorted(
            partitions[period],
            key=lambda row: (row["date"], row["id"]),
        )
        part_path = index_root / "by-time" / f"{period}.jsonl"
        part_path.parent.mkdir(parents=True, exist_ok=True)

        with part_path.open("w", encoding="utf-8", newline="\n") as handle:
            for row in part_rows:
                handle.write(
                    json.dumps(row, ensure_ascii=False, sort_keys=True) + "\n"
                )

        result.append(
            {
                "period": period,
                "count": len(part_rows),
                "path": part_path.relative_to(root).as_posix(),
            }
        )

    return {"partitions": result}


def build(root: Path) -> dict[str, Any]:
    records = collect_records(root)
    index_root = root / "indexes"

    if index_root.exists():
        shutil.rmtree(index_root)
    index_root.mkdir(parents=True, exist_ok=True)

    rows = [
        normalize_record(root, path, meta, body)
        for path, meta, body in records
    ]

    by_author: dict[str, list[dict[str, Any]]] = defaultdict(list)
    by_area: dict[str, list[dict[str, Any]]] = defaultdict(list)
    by_place: dict[str, list[dict[str, Any]]] = defaultdict(list)

    for row in rows:
        by_author[row["author"]].append(row)
        by_area[row["place"]["area"]].append(row)
        by_place[row["place_key"]].append(row)

    author_catalog = []
    for author in sorted(by_author):
        group_dir = index_root / "by-author" / safe_segment(author, "author")
        manifest = write_group(
            root,
            group_dir,
            {"author": author},
            by_author[author],
        )
        author_catalog.append(
            {
                "author": author,
                "record_count": len(by_author[author]),
                "manifest": manifest,
            }
        )

    area_catalog = []
    for area in sorted(by_area):
        group_dir = index_root / "by-area"
        for segment in area.split("/"):
            group_dir = group_dir / segment

        manifest = write_group(
            root,
            group_dir,
            {"area": area},
            by_area[area],
        )
        area_catalog.append(
            {
                "area": area,
                "record_count": len(by_area[area]),
                "manifest": manifest,
            }
        )

    place_catalog = []
    for key in sorted(by_place):
        place_rows = by_place[key]
        first_place = place_rows[0]["place"]
        group_dir = index_root / "by-place" / safe_segment(key, "place")

        manifest = write_group(
            root,
            group_dir,
            {
                "place_key": key,
                "place_id": first_place.get("id"),
                "place_name": first_place["name"],
                "area": first_place["area"],
            },
            place_rows,
        )

        place_catalog.append(
            {
                "place_key": key,
                "place_id": first_place.get("id"),
                "place_name": first_place["name"],
                "area": first_place["area"],
                "record_count": len(place_rows),
                "manifest": manifest,
            }
        )

    dates = sorted(
        row["date"]
        for row in rows
        if row["date"] != "unknown"
    )

    catalog = {
        "schema_version": 2,
        "record_count": len(rows),
        "date_range": {
            "first": dates[0] if dates else None,
            "last": dates[-1] if dates else None,
        },
        "authors": author_catalog,
        "areas": area_catalog,
        "places": place_catalog,
        "time": write_time_index(root, index_root, rows),
        "note": (
            "Generated mechanically from canonical experience files under data/. "
            "No AI profile or recommendation is stored in these indexes."
        ),
    }

    dump_json(index_root / "catalog.json", catalog)
    return catalog


def main() -> int:
    parser = argparse.ArgumentParser(
        description="Rebuild AI-readable food-memory indexes"
    )
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
        f"{len(catalog['places'])} place(s), "
        f"{len(catalog['areas'])} area(s)"
    )

    return 0


if __name__ == "__main__":
    raise SystemExit(main())
