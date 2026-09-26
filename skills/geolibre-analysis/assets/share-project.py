#!/usr/bin/env python3
import argparse, json, os, sys, urllib.request, urllib.error
from pathlib import Path
from urllib.parse import quote

MAX_BYTES = 50 * 1024 * 1024
DEFAULT_BASE = "https://share.geolibre.app"

def walk_strings(obj):
    if isinstance(obj, dict):
        for v in obj.values():
            yield from walk_strings(v)
    elif isinstance(obj, list):
        for v in obj:
            yield from walk_strings(v)
    elif isinstance(obj, str):
        yield obj

def preflight(project):
    raw = json.dumps(project, ensure_ascii=False, separators=(",", ":")).encode("utf-8")
    errors, warnings = [], []
    if len(raw) >= MAX_BYTES:
        errors.append(f"project too large: {len(raw)} bytes >= 50 MiB")
    layers = project.get("layers") or []
    if not layers:
        errors.append("project has no layers")
    visible = [l for l in layers if l.get("visible", True)]
    if not visible:
        errors.append("project has no visible layer")
    for i, layer in enumerate(layers):
        gj = layer.get("geojson")
        if gj is not None and (not isinstance(gj, dict) or gj.get("type") != "FeatureCollection"):
            errors.append(f"layer[{i}] inline geojson is not a FeatureCollection")
    for s in walk_strings(project):
        low = s.lower()
        if low.startswith("file://") or "localhost" in low or "127.0.0.1" in low:
            errors.append(f"local-only reference found: {s[:180]}")
        if (low.startswith("/") or (len(s) > 2 and s[1:3] in (":\\", ":/"))) and not low.startswith("//"):
            warnings.append(f"possible local path: {s[:180]}")
    return raw, sorted(set(errors)), sorted(set(warnings))

def request_json(url, method="GET", token=None, payload=None):
    body = None
    headers = {"Accept": "application/json"}
    if token:
        headers["Authorization"] = f"Bearer {token}"
    if payload is not None:
        body = json.dumps(payload, ensure_ascii=False).encode("utf-8")
        headers["Content-Type"] = "application/json"
    req = urllib.request.Request(url, data=body, method=method, headers=headers)
    with urllib.request.urlopen(req, timeout=60) as resp:
        return resp.status, json.loads(resp.read().decode("utf-8"))

def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("project")
    ap.add_argument("--visibility", default="unlisted", choices=["public","unlisted","private"])
    ap.add_argument("--base-url", default=DEFAULT_BASE)
    ap.add_argument("--preflight-only", action="store_true")
    args = ap.parse_args()

    path = Path(args.project)
    project = json.loads(path.read_text(encoding="utf-8"))
    raw, errors, warnings = preflight(project)
    result = {
        "project": str(path),
        "bytes": len(raw),
        "layerCount": len(project.get("layers") or []),
        "errors": errors,
        "warnings": warnings,
    }
    if errors or args.preflight_only:
        print(json.dumps(result, ensure_ascii=False, indent=2))
        sys.exit(2 if errors else 0)

    token = os.environ.get("GEOLIBRE_SHARE_TOKEN")
    if not token:
        result["upload"] = "blocked"
        result["reason"] = "GEOLIBRE_SHARE_TOKEN is not set"
        print(json.dumps(result, ensure_ascii=False, indent=2))
        sys.exit(3)

    payload = {
        "filename": path.name,
        "content": raw.decode("utf-8"),
        "visibility": args.visibility,
    }
    try:
        status, response = request_json(args.base_url.rstrip("/") + "/api/projects", "POST", token, payload)
    except urllib.error.HTTPError as e:
        body = e.read().decode("utf-8", "replace")
        print(json.dumps({**result,"upload":"failed","httpStatus":e.code,"response":body[:2000]},ensure_ascii=False,indent=2))
        sys.exit(4)

    project_info = response.get("project", response)
    raw_url = project_info.get("rawJsonUrl")
    viewer = None
    if raw_url:
        viewer = "https://web.geolibre.app/?url=" + quote(raw_url, safe="") + "&layout=viewer&loading=true&locale=zh-TW"
    print(json.dumps({
        **result,
        "upload":"success",
        "httpStatus":status,
        "id":project_info.get("id"),
        "slug":project_info.get("slug"),
        "visibility":project_info.get("visibility"),
        "rawJsonUrl":raw_url,
        "projectUrl":project_info.get("projectUrl"),
        "viewerUrl":viewer or project_info.get("viewerUrl"),
    },ensure_ascii=False,indent=2))

if __name__ == "__main__":
    main()
