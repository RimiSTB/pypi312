#!/usr/bin/env python3
"""
update_index.py - Regenerate PEP 503 Simple Repository index files.

Run this script every time you add, remove, or update .whl files
inside the 'wheels/' directory.

Also generates Zenodo index for large wheels (>100MB).

Usage:
    python update_index.py
"""

import hashlib
import html
import os
import json
from pathlib import Path

SIMPLE_DIR = Path(__file__).resolve().parent / "wheels"
ZENODO_RECORDS = {
    "record_1": {
        "record_id": "22036206",
        "doi": "10.5281/zenodo.22036206"
    },
    "record_2": {
        "record_id": "22036272",
        "doi": "10.5281/zenodo.22036272"
    }
}

# Wheels that are NOT on GitHub (>100MB) - these need Zenodo URLs
# Record 22036206 is full (100/100), use 22036272 for new uploads
ZENODO_ONLY_WHEELS = {
    "duckdb-1.5.5-cp312-abi3-android_24_arm64_v8a.whl": "22036206",
    "duckdb-1.5.5-cp312-abi3-android_24_x86_64.whl": "22036206",
}

def get_wheel_url(filename: str) -> str:
    """Get download URL for a wheel file."""
    if filename in ZENODO_ONLY_WHEELS:
        # Large wheel - use Zenodo (without ?download=1 for better CDN performance)
        record_id = ZENODO_ONLY_WHEELS[filename]
        return f"https://zenodo.org/records/{record_id}/files/{filename}"
    else:
        # Small wheel - use GitHub
        return filename


def sha256_of_file(filepath: Path) -> str:
    h = hashlib.sha256()
    with open(filepath, "rb") as f:
        for chunk in iter(lambda: f.read(8192), b""):
            h.update(chunk)
    return h.hexdigest()


def normalize_name(name: str) -> str:
    """PEP 503: replace [-_.] with single hyphen, lowercase."""
    import re
    return re.sub(r"[-_.]+", "-", name).lower()


def build_package_index(pkg_dir: Path) -> None:
    """Generate index.html for a single package directory."""
    wheels = sorted(pkg_dir.glob("*.whl"))
    if not wheels:
        return

    pkg_name = pkg_dir.name
    lines = [
        "<!DOCTYPE html>",
        "<html>",
        f"<head><title>{html.escape(pkg_name)}</title></head>",
        "<body>",
        f"<h1>{html.escape(pkg_name)}</h1>",
    ]

    for whl in wheels:
        escaped = html.escape(whl.name)
        url = get_wheel_url(whl.name)
        lines.append(
            f'<a href="{url}">{escaped}</a><br>'
        )

    lines += ["</body>", "</html>"]

    index_path = pkg_dir / "index.html"
    index_path.write_text("\n".join(lines) + "\n", encoding="utf-8")
    print(f"  [OK] {pkg_dir.name}/index.html  ({len(wheels)} wheel(s))")


def build_root_index(simple_dir: Path, package_dirs: list[Path]) -> None:
    """Generate the root simple/index.html listing all packages."""
    lines = [
        "<!DOCTYPE html>",
        "<html>",
        "<head><title>PythonSTB PyPI 3.12 Index</title></head>",
        "<body>",
        "<h1>PythonSTB PyPI 3.12 Index</h1>",
    ]

    for pkg_dir in sorted(package_dirs, key=lambda p: p.name.lower()):
        name = pkg_dir.name
        lines.append(f'<a href="{html.escape(name)}/">{html.escape(name)}</a><br>')

    lines += ["</body>", "</html>"]

    root_index = simple_dir / "index.html"
    root_index.write_text("\n".join(lines) + "\n", encoding="utf-8")
    print(f"  [OK] wheels/index.html  ({len(package_dirs)} package(s))")


def main() -> None:
    if not SIMPLE_DIR.is_dir():
        print(f"ERROR: {SIMPLE_DIR} not found.")
        return

    print("Scanning wheels/ for packages...\n")

    package_dirs = []
    for entry in sorted(SIMPLE_DIR.iterdir()):
        if entry.is_dir() and not entry.name.startswith((".", "_")):
            has_whl = any(entry.glob("*.whl"))
            if has_whl:
                package_dirs.append(entry)
                build_package_index(entry)

    print()
    build_root_index(SIMPLE_DIR, package_dirs)
    
    print("\nDone. All index.html files regenerated.")


if __name__ == "__main__":
    main()
