#!/usr/bin/env python3
"""Download one tightly scoped NLSC PHOTO2 mosaic and warp it to TWD97/TM2 121.

The script intentionally does not create a reusable tile cache.  It requests only
the tiles needed by the project extent, builds the output in memory, and writes a
georeferenced JPEG plus provenance metadata for internal project QA.
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
SERVICE_ROOT = "https://wmts.nlsc.gov.tw/wmts"
SERVICE_INFO = "https://maps.nlsc.gov.tw/S09SOA/pro/Wmts_ajax_main.jsp"


def mercator_to_global_pixel(mx: np.ndarray, my: np.ndarray, zoom: int) -> tuple[np.ndarray, np.ndarray]:
    span = TILE_SIZE * (2**zoom)
    px = (mx + ORIGIN_SHIFT) / (2 * ORIGIN_SHIFT) * span
    py = (ORIGIN_SHIFT - my) / (2 * ORIGIN_SHIFT) * span
    return px, py


def extent_tile_range(extent: tuple[float, float, float, float], zoom: int) -> tuple[int, int, int, int]:
    xmin, ymin, xmax, ymax = extent
    to_merc = Transformer.from_crs("EPSG:3826", "EPSG:3857", always_xy=True)
    corners = [
        to_merc.transform(xmin, ymin),
        to_merc.transform(xmin, ymax),
        to_merc.transform(xmax, ymin),
        to_merc.transform(xmax, ymax),
    ]
    mx = np.array([p[0] for p in corners], dtype=np.float64)
    my = np.array([p[1] for p in corners], dtype=np.float64)
    px, py = mercator_to_global_pixel(mx, my, zoom)
    return (
        int(math.floor(px.min() / TILE_SIZE)),
        int(math.floor(py.min() / TILE_SIZE)),
        int(math.floor(px.max() / TILE_SIZE)),
        int(math.floor(py.max() / TILE_SIZE)),
    )


def get_tile(session: requests.Session, layer: str, zoom: int, x: int, y: int) -> Image.Image:
    url = f"{SERVICE_ROOT}/{layer}/default/GoogleMapsCompatible/{zoom}/{y}/{x}"
    response = session.get(url, timeout=30)
    response.raise_for_status()
    image = Image.open(io.BytesIO(response.content)).convert("RGB")
    if image.size != (TILE_SIZE, TILE_SIZE):
        raise RuntimeError(f"Unexpected tile size {image.size}: {url}")
    return image


def write_world_file(path: Path, extent: tuple[float, float, float, float], width: int, height: int) -> None:
    xmin, ymin, xmax, ymax = extent
    px = (xmax - xmin) / width
    py = (ymax - ymin) / height
    values = [px, 0.0, 0.0, -py, xmin + px / 2, ymax - py / 2]
    path.write_text("\n".join(f"{v:.12f}" for v in values) + "\n", encoding="ascii")


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--extent", nargs=4, type=float, metavar=("XMIN", "YMIN", "XMAX", "YMAX"), required=True)
    parser.add_argument("--zoom", type=int, default=19)
    parser.add_argument("--size", type=int, default=4096)
    parser.add_argument("--layer", default="PHOTO2")
    parser.add_argument("--output", type=Path, required=True)
    parser.add_argument("--metadata", type=Path, required=True)
    parser.add_argument("--delay", type=float, default=0.08)
    args = parser.parse_args()

    extent = tuple(args.extent)
    xmin_tile, ymin_tile, xmax_tile, ymax_tile = extent_tile_range(extent, args.zoom)
    cols = xmax_tile - xmin_tile + 1
    rows = ymax_tile - ymin_tile + 1
    count = cols * rows
    if count > 256:
        raise RuntimeError(f"Refusing broad request of {count} tiles; narrow the project extent.")

    mosaic = Image.new("RGB", (cols * TILE_SIZE, rows * TILE_SIZE))
    session = requests.Session()
    session.headers["User-Agent"] = "WujieFloodModel/1.0 internal-government-GIS-QA"
    tile_urls: list[str] = []
    for row, y in enumerate(range(ymin_tile, ymax_tile + 1)):
        for col, x in enumerate(range(xmin_tile, xmax_tile + 1)):
            tile = get_tile(session, args.layer, args.zoom, x, y)
            mosaic.paste(tile, (col * TILE_SIZE, row * TILE_SIZE))
            tile_urls.append(f"{SERVICE_ROOT}/{args.layer}/default/GoogleMapsCompatible/{args.zoom}/{y}/{x}")
            time.sleep(args.delay)

    # Build an exact EPSG:3826 north-up raster by sampling the Web-Mercator mosaic.
    size = args.size
    xmin, ymin, xmax, ymax = extent
    xs = np.linspace(xmin + (xmax - xmin) / (2 * size), xmax - (xmax - xmin) / (2 * size), size)
    ys = np.linspace(ymax - (ymax - ymin) / (2 * size), ymin + (ymax - ymin) / (2 * size), size)
    grid_x, grid_y = np.meshgrid(xs, ys)
    to_merc = Transformer.from_crs("EPSG:3826", "EPSG:3857", always_xy=True)
    mx, my = to_merc.transform(grid_x, grid_y)
    global_x, global_y = mercator_to_global_pixel(mx, my, args.zoom)
    map_x = (global_x - xmin_tile * TILE_SIZE).astype(np.float32)
    map_y = (global_y - ymin_tile * TILE_SIZE).astype(np.float32)
    mosaic_bgr = cv2.cvtColor(np.asarray(mosaic), cv2.COLOR_RGB2BGR)
    warped = cv2.remap(mosaic_bgr, map_x, map_y, interpolation=cv2.INTER_LANCZOS4, borderMode=cv2.BORDER_REFLECT)

    args.output.parent.mkdir(parents=True, exist_ok=True)
    if not cv2.imwrite(str(args.output), warped, [cv2.IMWRITE_JPEG_QUALITY, 94]):
        raise RuntimeError(f"Unable to write {args.output}")
    write_world_file(args.output.with_suffix(".jgw"), extent, size, size)

    retrieved = datetime.now(timezone.utc).astimezone().isoformat(timespec="seconds")
    metadata = {
        "status": "SOURCE_ACQUIRED_NOT_YET_ART_APPROVED",
        "title": "臺灣通用正射影像（最新服務合成）",
        "agency": "內政部國土測繪中心",
        "layer": args.layer,
        "service": SERVICE_ROOT,
        "serviceInfo": SERVICE_INFO,
        "retrievedAt": retrieved,
        "crs": "EPSG:3826",
        "extent": {"xmin": xmin, "ymin": ymin, "xmax": xmax, "ymax": ymax},
        "zoom": args.zoom,
        "outputPixels": [size, size],
        "groundPixelSizeM": [(xmax - xmin) / size, (ymax - ymin) / size],
        "tileRange": {"xmin": xmin_tile, "ymin": ymin_tile, "xmax": xmax_tile, "ymax": ymax_tile},
        "tileCount": count,
        "tileUrls": tile_urls,
        "labels": "none; PHOTO2 is imagery only",
        "imageryDateCaveat": "PHOTO2 is the latest composite exposed by NLSC at retrieval time; local capture year must be checked against the official coverage/year layer and is not inferred from appearance.",
        "usage": "Tightly scoped internal project visualization/QA; no bulk cache or onward tile service.",
        "referenceOnly": "Orthophoto is the visual base; legal boundaries and building records remain separate government layers."
    }
    args.metadata.parent.mkdir(parents=True, exist_ok=True)
    args.metadata.write_text(json.dumps(metadata, ensure_ascii=False, indent=2), encoding="utf-8")
    print(json.dumps({"output": str(args.output), "tileCount": count, "tileRange": metadata["tileRange"]}, ensure_ascii=False))


if __name__ == "__main__":
    main()
