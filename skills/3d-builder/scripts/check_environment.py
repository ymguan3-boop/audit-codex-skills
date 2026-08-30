#!/usr/bin/env python3
"""Read-only local diagnostics for the 3d-builder skill."""

from __future__ import annotations

import argparse
import json
import os
import platform
import shutil
import subprocess
from datetime import datetime, timezone
from pathlib import Path
from typing import Any


COMMANDS = ("blender", "python", "node", "npm", "git", "nvidia-smi")


def command_record(name: str) -> dict[str, Any]:
    path = shutil.which(name)
    return {
        "available": path is not None,
        "path": str(Path(path).resolve()) if path else None,
    }


def discover_windows_blender() -> str | None:
    if platform.system() != "Windows":
        return None
    program_files = os.environ.get("ProgramFiles")
    if not program_files:
        return None
    root = Path(program_files) / "Blender Foundation"
    if not root.is_dir():
        return None
    candidates = sorted(root.glob("Blender */blender.exe"), reverse=True)
    return str(candidates[0].resolve()) if candidates else None


def detect_nvidia_gpus(nvidia_smi: str | None) -> list[dict[str, Any]]:
    if not nvidia_smi:
        return []
    try:
        completed = subprocess.run(
            [
                nvidia_smi,
                "--query-gpu=name,memory.total,driver_version",
                "--format=csv,noheader,nounits",
            ],
            check=True,
            capture_output=True,
            text=True,
            timeout=10,
        )
    except (OSError, subprocess.SubprocessError) as exc:
        return [{"error": str(exc)}]

    records: list[dict[str, Any]] = []
    for row in completed.stdout.splitlines():
        parts = [part.strip() for part in row.split(",")]
        if len(parts) >= 3:
            try:
                memory_mib: int | str = int(parts[1])
            except ValueError:
                memory_mib = parts[1]
            records.append(
                {
                    "name": parts[0],
                    "memoryMiB": memory_mib,
                    "driverVersion": parts[2],
                }
            )
    return records


def build_report() -> dict[str, Any]:
    commands = {name: command_record(name) for name in COMMANDS}
    if not commands["blender"]["available"]:
        discovered = discover_windows_blender()
        if discovered:
            commands["blender"] = {"available": True, "path": discovered}

    gpu = detect_nvidia_gpus(commands["nvidia-smi"]["path"])
    warnings: list[str] = []
    if not commands["blender"]["available"]:
        warnings.append(
            "Blender was not found on PATH or in the standard Windows installation folder."
        )
    if not gpu:
        warnings.append(
            "No NVIDIA GPU details were detected; this does not prove that no compatible GPU exists."
        )

    return {
        "schemaVersion": 1,
        "checkedAtUtc": datetime.now(timezone.utc).isoformat(),
        "operatingSystem": platform.platform(),
        "processArchitecture": platform.machine(),
        "commands": commands,
        "gpu": gpu,
        "mcpInspection": {
            "performedByScript": False,
            "requiredAction": (
                "Inspect the live Codex tool catalog for Blender and AI 3D capabilities."
            ),
        },
        "warnings": warnings,
    }


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--pretty", action="store_true", help="Indent JSON output.")
    args = parser.parse_args()
    print(
        json.dumps(
            build_report(),
            ensure_ascii=False,
            indent=2 if args.pretty else None,
            separators=None if args.pretty else (",", ":"),
        )
    )
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
