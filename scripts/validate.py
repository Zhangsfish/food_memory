#!/usr/bin/env python3
from __future__ import annotations

import argparse
import re
import sys
from pathlib import Path
from typing import Any

import yaml

DATE_RE = re.compile(r"^\d{4}(?:-\d{2}(?:-\d{2})?)?$")
COUNTRY_RE = re.compile(r"^[A-Z]{2}$")
CURRENCY_RE = re.compile(r"^[A-Z]{3}$")

LOCAL_RELATIONS = {
    "resident",
    "former_resident",
    "frequent_visitor",
    "visitor",
    "unknown",
}

COMMERCIAL_RELATIONSHIPS = {
    "none_declared",
    "invited",
    "discounted",
    "sponsored",
    "employee",
    "owner",
    "other",
    "not_provided",
}

COST_BASES = {
    "bill_total",
    "my_share",
    "per_person",
    "itemized",
    "unknown",
}


class RecordError(ValueError):
    pass


def parse_markdown_record(path: Path) -> tuple[dict[str, Any], str]:
    text = path.read_text(encoding="utf-8")
    if not text.startswith("---"):
        raise RecordError("missing YAML front matter")

    lines = text.splitlines()
    if not lines or lines[0].strip() != "---":
        raise RecordError("front matter must start with a line containing only ---")

    try:
        end = next(i for i in range(1, len(lines)) if lines[i].strip() == "---")
    except StopIteration as exc:
        raise RecordError("front matter is not closed with ---") from exc

    front = "\n".join(lines[1:end])
    body = "\n".join(lines[end + 1 :]).strip()

    try:
        meta = yaml.safe_load(front)
    except yaml.YAMLError as exc:
        raise RecordError(f"invalid YAML: {exc}") from exc

    if not isinstance(meta, dict):
        raise RecordError("front matter must be a mapping")
    if not body:
        raise RecordError("experience body must not be empty")
    return meta, body


def _nonempty_string(value: Any, label: str) -> str:
    if not isinstance(value, str) or not value.strip():
        raise RecordError(f"{label} must be a non-empty string")
    return value.strip()


def validate_meta(meta: dict[str, Any], path: Path | None = None) -> None:
    where = f" in {path}" if path else ""

    if meta.get("schema_version") != 1:
        raise RecordError(f"schema_version must be 1{where}")

    record_id = _nonempty_string(meta.get("id"), "id")
    if not record_id.startswith("exp_"):
        raise RecordError("id must begin with exp_")

    _nonempty_string(meta.get("author"), "author")

    date = _nonempty_string(meta.get("date"), "date")
    if date != "unknown" and not DATE_RE.fullmatch(date):
        raise RecordError("date must be YYYY, YYYY-MM, YYYY-MM-DD, or unknown")

    place = meta.get("place")
    if not isinstance(place, dict):
        raise RecordError("place must be a mapping")
    _nonempty_string(place.get("name"), "place.name")
    area = _nonempty_string(place.get("area"), "place.area")
    segments = [s for s in area.split("/") if s]
    if len(segments) < 2:
        raise RecordError("place.area must contain at least COUNTRY/LOCALITY")
    if not COUNTRY_RE.fullmatch(segments[0]):
        raise RecordError("place.area must start with a two-letter uppercase country code")
    if any(s in {".", ".."} for s in segments):
        raise RecordError("place.area contains an invalid path segment")
    if "hint" in place:
        _nonempty_string(place.get("hint"), "place.hint")

    dishes = meta.get("dishes")
    if not isinstance(dishes, list) or not dishes:
        raise RecordError("dishes must be a non-empty list")
    for i, dish in enumerate(dishes):
        _nonempty_string(dish, f"dishes[{i}]")

    cost = meta.get("cost")
    if cost is not None:
        if not isinstance(cost, dict):
            raise RecordError("cost must be a mapping")
        amount = cost.get("amount")
        if not isinstance(amount, (int, float)) or isinstance(amount, bool) or amount < 0:
            raise RecordError("cost.amount must be a non-negative number")
        currency = _nonempty_string(cost.get("currency"), "cost.currency")
        if not CURRENCY_RE.fullmatch(currency):
            raise RecordError("cost.currency must be a three-letter uppercase code")
        if cost.get("basis") not in COST_BASES:
            raise RecordError(f"cost.basis must be one of {sorted(COST_BASES)}")

    if "local_relation" in meta and meta.get("local_relation") not in LOCAL_RELATIONS:
        raise RecordError(
            f"local_relation must be one of {sorted(LOCAL_RELATIONS)}"
        )

    if (
        "commercial_relationship" in meta
        and meta.get("commercial_relationship") not in COMMERCIAL_RELATIONSHIPS
    ):
        raise RecordError(
            "commercial_relationship must be one of "
            f"{sorted(COMMERCIAL_RELATIONSHIPS)}"
        )

    attachments = meta.get("attachments")
    if attachments is not None:
        if not isinstance(attachments, list):
            raise RecordError("attachments must be a list")
        for i, attachment in enumerate(attachments):
            a = _nonempty_string(attachment, f"attachments[{i}]")
            if not a.startswith("media/"):
                raise RecordError("attachment paths must begin with media/")


def collect_records(root: Path) -> list[tuple[Path, dict[str, Any], str]]:
    data_dir = root / "data"
    records: list[tuple[Path, dict[str, Any], str]] = []
    ids: dict[str, Path] = {}

    if not data_dir.exists():
        return records

    for path in sorted(data_dir.rglob("*.md")):
        meta, body = parse_markdown_record(path)
        validate_meta(meta, path)
        record_id = meta["id"]
        if record_id in ids:
            raise RecordError(
                f"duplicate id {record_id!r}: {ids[record_id]} and {path}"
            )
        ids[record_id] = path
        records.append((path, meta, body))

    return records


def main() -> int:
    parser = argparse.ArgumentParser(description="Validate food_memory canonical records")
    parser.add_argument(
        "--root",
        type=Path,
        default=Path(__file__).resolve().parents[1],
        help="repository root",
    )
    args = parser.parse_args()

    try:
        records = collect_records(args.root)
    except (OSError, RecordError) as exc:
        print(f"VALIDATION FAILED: {exc}", file=sys.stderr)
        return 1

    print(f"VALIDATION PASSED: {len(records)} canonical record(s)")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
