#!/usr/bin/env python3
"""Acquire a tightly scoped transparent NLSC WMTS overlay in EPSG:3826.

Supported use cases in this project include BUILDX building frames and the
public-view DMAPS cadastral reference.  Raster overlays are QA/reference layers;
they are not silently promoted to legal parcel geometry or surveyed footprints.
"""

from __future__ import annotations

import argparse
import io
import json
import math
import time
from datetime import datetime, timezone
from pathlib import Path

import cv2
import numpy as np
import requests
from PIL import Image
from pyproj import Transformer


ORIGIN_SHIFT = 20037508.342789244
TILE_SIZE = 256


def global_pixel(mx: np.ndarray, my: np.ndarray, zoom: int) -> tuple[np.ndarray, np.ndarray]:
    span = TILE_SIZE * (2**zoom)
    return (
        (mx + ORIGIN_SHIFT) / (2 * ORIGIN_SHIFT) * span,
        (ORIGIN_SHIFT - my) / (2 * ORIGIN_SHIFT) * span,
    )


def tile_range(extent: tuple[float, float, float, float], zoom: int) -> tuple[int, int, int, int]:
    xmin, ymin, xmax, ymax = extent
    t = Transformer.from_crs("EPSG:3826", "EPSG:3857", always_xy=True)
    points = [t.transform(x, y) for x in (xmin, xmax) for y in (ymin, ymax)]
    mx = np.array([p[0] for p in points])
    my = np.array([p[1] for p in points])
    px, py = global_pixel(mx, my, zoom)
    return int(px.min() // 256), int(py.min() // 256), int(px.max() // 256), int(py.max() // 256)


def world_file(path: Path, extent: tuple[float, float, float, float], width: int, height: int) -> None:
    xmin, ymin, xmax, ymax = extent
    sx = (xmax - xmin) / width
    sy = (ymax - ymin) / height
    path.write_text(
        "\n".join(f"{v:.12f}" for v in (sx, 0, 0, -sy, xmin + sx / 2, ymax - sy / 2)) + "\n",
        encoding="ascii",
    )


def main() -> None:
    p = argparse.ArgumentParser()
    p.add_argument("--extent", nargs=4, type=float, required=True)
    p.add_argument("--layer", required=True)
    p.add_argument("--zoom", type=int, default=20)
    p.add_argument("--size", type=int, default=4096)
    p.add_argument("--service", default="https://wmts.nlsc.gov.tw/wmts")
    p.add_argument("--output", type=Path, required=True)
    p.add_argument("--metadata", type=Path, required=True)
    p.add_argument("--delay", type=float, default=0.06)
    args = p.parse_args()

    extent = tuple(args.extent)
    x0, y0, x1, y1 = tile_range(extent, args.zoom)
    cols, rows = x1 - x0 + 1, y1 - y0 + 1
    count = cols * rows
    if count > 256:
        raise RuntimeError(f"Refusing broad request of {count} tiles; use a smaller QA extent.")

    mosaic = Image.new("RGBA", (cols * 256, rows * 256), (0, 0, 0, 0))
    session = requests.Session()
    session.headers["User-Agent"] = "WujieFloodModel/1.0 internal-government-GIS-QA"
    urls = []
    for row, y in enumerate(range(y0, y1 + 1)):
        for col, x in enumerate(range(x0, x1 + 1)):
            url = f"{args.service}/{args.layer}/default/EPSG:3857/{args.zoom}/{y}/{x}"
            response = session.get(url, timeout=30)
            response.raise_for_status()
            tile = Image.open(io.BytesIO(response.content)).convert("RGBA")
            mosaic.paste(tile, (col * 256, row * 256), tile)
            urls.append(url)
            time.sleep(args.delay)

    size = args.size
    xmin, ymin, xmax, ymax = extent
    xs = np.linspace(xmin + (xmax - xmin) / (2 * size), xmax - (xmax - xmin) / (2 * size), size)
    ys = np.linspace(ymax - (ymax - ymin) / (2 * size), ymin + (ymax - ymin) / (2 * size), size)
    gx, gy = np.meshgrid(xs, ys)
    t = Transformer.from_crs("EPSG:3826", "EPSG:3857", always_xy=True)
    mx, my = t.transform(gx, gy)
    px, py = global_pixel(mx, my, args.zoom)
    map_x = (px - x0 * 256).astype(np.float32)
    map_y = (py - y0 * 256).astype(np.float32)
    rgba = np.asarray(mosaic)
    warped = cv2.remap(rgba, map_x, map_y, cv2.INTER_LINEAR, borderMode=cv2.BORDER_CONSTANT)

    args.output.parent.mkdir(parents=True, exist_ok=True)
    Image.fromarray(warped, "RGBA").save(args.output, optimize=True)
    world_file(args.output.with_suffix(".pgw"), extent, size, size)
    meta = {
        "status": "REFERENCE_RASTER_NOT_LEGAL_GEOMETRY",
        "agency": "內政部國土測繪中心",
        "layer": args.layer,
        "service": args.service,
        "retrievedAt": datetime.now(timezone.utc).astimezone().isoformat(timespec="seconds"),
        "crs": "EPSG:3826",
        "extent": {"xmin": xmin, "ymin": ymin, "xmax": xmax, "ymax": ymax},
        "zoom": args.zoom,
        "outputPixels": [size, size],
        "tileCount": count,
        "tileRange": {"xmin": x0, "ymin": y0, "xmax": x1, "ymax": y1},
        "tileUrls": urls,
        "limitations": "Public visualization raster used for alignment/reference only; legal cadastral boundaries and surveyed building geometry require the competent authority's formal data."
    }
    args.metadata.write_text(json.dumps(meta, ensure_ascii=False, indent=2), encoding="utf-8")
    print(json.dumps({"layer": args.layer, "tileCount": count, "output": str(args.output)}, ensure_ascii=False))


if __name__ == "__main__":
    main()
