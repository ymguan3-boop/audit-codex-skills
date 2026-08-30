"""Validate the minimum provenance and QA fields of a GIS 3D project.

Usage:
    python validate_project_manifest.py <asset-registry.json>
"""

from __future__ import annotations

import json
import sys
from pathlib import Path


REQUIRED_ASSET_FIELDS = {
    "id",
    "title",
    "agency",
    "sourceUrl",
    "retrievedAt",
    "crs",
    "extent",
    "usage",
    "limitations",
    "status",
}

ALLOWED_STATUS = {
    "SOURCE_ACQUIRED",
    "GEOREFERENCED",
    "SPATIAL_QA_PASS",
    "SPATIAL_QA_FAIL",
    "ATTRIBUTE_QA_PASS",
    "USER_APPROVED",
    "REJECTED_ART_QUALITY",
    "NOT_PUBLIC_OR_REQUIRES_APPLICATION",
}


def main() -> int:
    if len(sys.argv) != 2:
        print("usage: validate_project_manifest.py <asset-registry.json>")
        return 2

    path = Path(sys.argv[1])
    payload = json.loads(path.read_text(encoding="utf-8"))
    assets = payload.get("assets")
    if not isinstance(assets, list) or not assets:
        print("ERROR: manifest.assets must be a non-empty list")
        return 1

    errors: list[str] = []
    seen: set[str] = set()
    for index, asset in enumerate(assets):
        missing = sorted(REQUIRED_ASSET_FIELDS - set(asset))
        if missing:
            errors.append(f"assets[{index}] missing: {', '.join(missing)}")
        asset_id = asset.get("id")
        if asset_id in seen:
            errors.append(f"duplicate asset id: {asset_id}")
        seen.add(asset_id)
        status = asset.get("status")
        if status not in ALLOWED_STATUS:
            errors.append(f"assets[{index}] invalid status: {status}")

    if errors:
        for error in errors:
            print(f"ERROR: {error}")
        return 1

    print(f"OK: {len(assets)} assets have minimum provenance fields")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
