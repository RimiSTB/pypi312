<div align="center">

# PythonSTB PyPI 3.12

### Cross-Compiled Python Wheels for Android

[![Python 3.12](https://img.shields.io/badge/Python-3.12-blue?logo=python&logoColor=white)](https://www.python.org/)
[![Android](https://img.shields.io/badge/Android-24+-green?logo=android&logoColor=white)](https://developer.android.com)
[![License](https://img.shields.io/badge/License-MIT-yellow.svg)](LICENSE)
[![PEP 503](https://img.shields.io/badge/PEP-503-compliant-brightgreen)](https://peps.python.org/pep-0503/)

</div>

---

## Overview

A **PEP 503 compliant** simple repository hosting **cross-compiled Python 3.12 wheels** for Android devices.

All wheels are built with:
- **16KB page alignment** (required for Android)
- **noRELRO** flag (required for dynamic loading)
- **Android API 24+** minimum
- **Dual architecture**: `arm64_v8a` (real devices) + `x86_64` (emulators)

---

## Quick Start

### Install via pip

```bash
pip install --extra-index-url https://rimistb.github.io/pypi312/wheels/ <package>
```

### Example: Install numpy

```bash
pip install --extra-index-url https://rimistb.github.io/pypi312/wheels/ numpy
```

---

## Available Packages

| Package | Version | Architectures | Description |
|---------|---------|---------------|-------------|
| aiohttp | 3.14.3 | arm64_v8a, x86_64 | Async HTTP client/server |
| bcrypt | 4.3.0 | arm64_v8a, x86_64 | Password hashing |
| blosc | 1.21.6 | arm64_v8a, x86_64 | Compression |
| cffi | 2.1.1 | arm64_v8a, x86_64 | C FFI |
| cryptography | 50.0.0 | arm64_v8a, x86_64 | Crypto primitives |
| duckdb | 1.5.5 | arm64_v8a, x86_64 | Analytical database |
| greenlet | 3.3.1 | arm64_v8a, x86_64 | Lightweight coroutines |
| lxml | 6.1.1 | arm64_v8a, x86_64 | XML/HTML parsing |
| matplotlib | 3.11.1 | arm64_v8a, x86_64 | Plotting library |
| numpy | 2.5.2 | arm64_v8a, x86_64 | Numerical computing |
| opencv-python | 4.12.0 | arm64_v8a, x86_64 | Computer vision |
| pandas | 2.3.3 | arm64_v8a, x86_64 | Data analysis |
| pillow | 12.3.0 | arm64_v8a, x86_64 | Image processing |
| psutil | 7.0.0 | arm64_v8a, x86_64 | System monitoring |
| pycryptodome | 3.23.0 | arm64_v8a, x86_64 | Crypto library |
| pydantic | 2.12.5 | arm64_v8a, x86_64 | Data validation |
| pydantic_core | 2.48.0 | arm64_v8a, x86_64 | Pydantic core |
| PyNaCl | 1.5.0 | arm64_v8a, x86_64 | Networking crypto |
| PyYAML | 6.0.3 | arm64_v8a, x86_64 | YAML parser |
| scikit-image | 0.26.0 | arm64_v8a, x86_64 | Image algorithms |
| scipy | 1.16.1 | arm64_v8a, x86_64 | Scientific computing |
| + 46 more | | | See full list below |

<details>
<summary><strong>Full Package List (68 packages)</strong></summary>

| Package | Architectures |
|---------|---------------|
| aiohappyeyeballs | pure Python |
| aiohttp | arm64_v8a, x86_64 |
| aiosignal | pure Python |
| annotated-types | pure Python |
| argon2-cffi-bindings | arm64_v8a, x86_64 |
| attrs | pure Python |
| bcrypt | arm64_v8a, x86_64 |
| blosc | arm64_v8a, x86_64 |
| bottleneck | arm64_v8a, x86_64 |
| brotli | arm64_v8a, x86_64 |
| cbor2 | arm64_v8a, x86_64 |
| cchardet | arm64_v8a, x86_64 |
| cffi | arm64_v8a, x86_64 |
| contourpy | arm64_v8a, x86_64 |
| cryptography | arm64_v8a, x86_64 |
| curl-cffi | arm64_v8a, x86_64 |
| duckdb | arm64_v8a, x86_64 |
| frozenlist | arm64_v8a, x86_64 |
| greenlet | arm64_v8a, x86_64 |
| hiredis | arm64_v8a, x86_64 |
| idna | pure Python |
| kiwisolver | arm64_v8a, x86_64 |
| lightgbm | arm64_v8a, x86_64 |
| lxml | arm64_v8a, x86_64 |
| lxml-html-clean | pure Python |
| lz4 | arm64_v8a, x86_64 |
| markupsafe | arm64_v8a, x86_64 |
| matplotlib | arm64_v8a, x86_64 |
| msgpack | arm64_v8a, x86_64 |
| multidict | arm64_v8a, x86_64 |
| numpy | arm64_v8a, x86_64 |
| opencv-python | arm64_v8a, x86_64 |
| orjson | arm64_v8a, x86_64 |
| pandas | arm64_v8a, x86_64 |
| pillow | arm64_v8a, x86_64 |
| pillow-simd | arm64_v8a, x86_64 |
| propcache | arm64_v8a, x86_64 |
| psutil | arm64_v8a, x86_64 |
| psycopg2 | arm64_v8a, x86_64 |
| pyarrow | arm64_v8a, x86_64 |
| pyaudio | arm64_v8a, x86_64 |
| pycares | arm64_v8a, x86_64 |
| pycparser | pure Python |
| pycryptodome | arm64_v8a, x86_64 |
| pycurl | arm64_v8a, x86_64 |
| pydantic | pure Python |
| pydantic-core | arm64_v8a, x86_64 |
| PyNaCl | arm64_v8a, x86_64 |
| python-dateutil | pure Python |
| pytz | pure Python |
| PyYAML | arm64_v8a, x86_64 |
| pyzmq | arm64_v8a, x86_64 |
| regex | arm64_v8a, x86_64 |
| rpds-py | arm64_v8a, x86_64 |
| scikit-image | arm64_v8a, x86_64 |
| scipy | arm64_v8a, x86_64 |
| six | pure Python |
| typing-extensions | pure Python |
| tzdata | pure Python |
| ujson | arm64_v8a, x86_64 |
| uvloop | arm64_v8a, x86_64 |
| wrapt | arm64_v8a, x86_64 |
| xgboost | arm64_v8a, x86_64 |
| yarl | arm64_v8a, x86_64 |
| zstandard | arm64_v8a, x86_64 |

</details>

---

## Repository Structure

```
pypi312/
└── wheels/                          ← PEP 503 index root
    ├── index.html                   ← lists ALL packages (alphabetical)
    ├── numpy/
    │   ├── index.html               ← lists all numpy wheels
    │   ├── numpy-2.5.2-cp312-cp312-android_24_arm64_v8a.whl
    │   └── numpy-2.5.2-cp312-cp312-android_24_x86_64.whl
    ├── pandas/
    │   ├── index.html
    │   ├── pandas-2.3.3-cp312-cp312-android_24_arm64_v8a.whl
    │   └── pandas-2.3.3-cp312-cp312-android_24_x86_64.whl
    └── <package>/
        ├── index.html
        ├── <package>-<version>-<tags>.whl
        └── USER_GUIDE.txt
```

---

## Installation Guide

### Option A: Extra Index URL (Recommended)

pip checks this repo FIRST, then falls back to PyPI:

```bash
pip install --extra-index-url https://rimistb.github.io/pypi312/wheels/ <package>
```

### Option B: Find-Links (Per Package)

```bash
pip install --find-links https://rimistb.github.io/pypi312/wheels/<package>/ <package>
```

### Option C: Global pip Configuration

**Windows** (`%APPDATA%\pip\pip.ini`):
```ini
[global]
extra-index-url = https://rimistb.github.io/pypi312/wheels/
```

**Linux/macOS** (`~/.pip/pip.conf`):
```ini
[global]
extra-index-url = https://rimistb.github.io/pypi312/wheels/
```

Then use plain `pip install <package>`.

---

## Android App Integration

### Python Code Example

```python
import subprocess
import sys

GITHUB_INDEX = "https://rimistb.github.io/pypi312/wheels/"

subprocess.check_call([
    sys.executable, "-m", "pip", "install",
    "--extra-index-url", GITHUB_INDEX,
    "numpy",
    "pandas",
    "duckdb",
])
```

### PipManager (PythonSTB)

PipManager is a built-in package manager for installing Python packages on Android.

**How to use:**

1. Open PipManager from the home screen
2. Type package name(s) in the text field — **space separated** for multiple packages
3. Click **INSTALL**

**Examples:**

| Input | What it does |
|-------|--------------|
| `requests` | Install requests |
| `numpy pandas duckdb` | Install 3 packages at once |
| `requests[socks]` | Install with extras |
| `colorama pyyaml six` | Install multiple small packages |

**Options:**
- **Upgrade** — upgrade to latest version
- **Reinstall** — force reinstall
- **Uninstall** — remove a package

**Features:**
- Live pip output in built-in terminal
- Smart detection — skips install if already installed
- Auto-logs: `✅` success, `❌` failure, `💡` hints for common issues
- Supports version specifiers: `numpy==2.5.2`, `pandas>=2.0`

---

## Package Naming (PEP 503)

| Rule | Example |
|------|---------|
| Folder name: **lowercase** | `PyNaCl` → `pynacl` |
| Replace `[_.,]` with `-` | `my_package` → `my-package` |
| Wheel filename: **keep original case** | `PyNaCl-1.5.0-...whl` |

---

## License

MIT

---

<div align="center">

**Built with care for the Android Python community**<br>
**Creator and Coder by RIMI**

[Python](https://www.python.org/) • [Android](https://developer.android.com) • [PEP 503](https://peps.python.org/pep-0503/)

</div>
