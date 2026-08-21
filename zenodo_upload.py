"""
Zenodo Upload Script for PythonSTB Wheels - FINAL VERSION
Uses CURL for file uploads (Python requests fails for >100MB files).
Rules:
  - ONE record at a time, title "PythonSTB Wheels (Part X)"
  - Upload ALL wheels FIRST, then publish at the END
  - Max 100 files per record
  - 2 wheels per package (arm64_v8a + x86_64), no duplicates
  - After record is full (100/100), publish, then create Part 2

PROVEN WORKFLOW:
  1. python - create record via legacy API (/api/deposit/depositions)
     - upload_type: "dataset" (NOT resource_type)
     - creators, title, description, etc.
  2. python - get bucket_url from record
  3. curl --upload-file <path> -H "Authorization: Bearer <token>" <bucket_url>/<filename>
     - timeout: --max-time 300 for large files
     - retry: --retry 3
  4. python - list files to verify count
  5. python - publish: POST /api/deposit/depositions/{id}/actions/publish
"""

import glob, os, sys, subprocess, time, requests

TOKEN = "OgLJ7moYCzQB9HF8Osqqwo8zqRRWwH11dYY095JG7Y6FLsXzPWbQs9VKS3wf"
HEADERS_JSON = {"Authorization": f"Bearer {TOKEN}", "Content-Type": "application/json"}
HEADERS_AUTH = {"Authorization": f"Bearer {TOKEN}"}
BASE = "https://zenodo.org/api"
WHEELS_DIR = r"C:\Users\RiMi\AndroidStudioProjects\backups_external\wheel_build_NoRERLO"
MAX_FILES = 100

RECORD_DESC = (
    "Cross-compiled Python 3.12.14 native wheels for Android "
    "(arm64_v8a + x86_64). Built with noRERLO, max-page-size=16384, "
    "common-page-size=16384. For use with PipManager on Android devices."
)


def collect_wheels():
    """Collect 2 wheels per package (arm64 + x86_64), no duplicates."""
    pattern = os.path.join(WHEELS_DIR, "*", "wheels", "STANDALONE", "*.whl")
    all_w = sorted(glob.glob(pattern), key=lambda x: os.path.basename(x).lower())

    by_pkg = {}
    for w in all_w:
        name = os.path.basename(w)
        parts = name.split("-")
        pkg_key = parts[0].lower()
        if pkg_key not in by_pkg:
            by_pkg[pkg_key] = {}
        if "arm64" in name:
            by_pkg[pkg_key]["arm64"] = w
        elif "x86_64" in name:
            by_pkg[pkg_key]["x86_64"] = w
        else:
            by_pkg[pkg_key]["pure"] = w

    deduped = []
    for pkg_key in sorted(by_pkg.keys()):
        archs = by_pkg[pkg_key]
        if "arm64" in archs and "x86_64" in archs:
            deduped.append(archs["arm64"])
            deduped.append(archs["x86_64"])
        elif "pure" in archs:
            deduped.append(archs["pure"])
        else:
            for v in archs.values():
                deduped.append(v)

    return deduped


def create_record(title):
    data = {
        "metadata": {
            "title": title,
            "upload_type": "dataset",
            "creators": [{"name": "RIMI", "affiliation": "PythonSTB"}],
            "description": RECORD_DESC,
            "publication_date": "2026-08-21",
            "access_right": "open",
            "license": "MIT",
            "keywords": ["python", "android", "wheels", "arm64", "x86_64", "native", "pip", "cpython-3.12"],
            "notes": "Generator: PythonSTB-RIMI-Build. BOM-free WHEEL metadata.",
            "version": "3.12.14"
        }
    }
    r = requests.post(f"{BASE}/deposit/depositions", headers=HEADERS_JSON, json=data)
    if r.status_code not in (200, 201):
        print(f"  Create FAILED: {r.status_code} {r.text[:300]}")
        return None
    d = r.json()
    return d["id"], d["links"]["bucket"]


def list_files(rec_id):
    r = requests.get(f"{BASE}/deposit/depositions/{rec_id}/files", headers=HEADERS_AUTH)
    return r.json() if r.status_code == 200 else []


def upload_whl_curl(bucket_url, filepath):
    """Upload wheel using CURL (works for >100MB files)."""
    filename = os.path.basename(filepath)
    size = os.path.getsize(filepath)
    cmd = [
        "curl", "--upload-file", filepath,
        "-H", f"Authorization: Bearer {TOKEN}",
        "--max-time", "300",
        "--retry", "3",
        "-s", "-o", "NUL", "-w", "%{http_code}",
        f"{bucket_url}/{filename}"
    ]
    result = subprocess.run(cmd, capture_output=True, text=True, timeout=600)
    status = result.stdout.strip()
    if status in ("200", "201"):
        return True
    print(f"  FAILED: {filename} (HTTP {status})")
    if result.stderr:
        print(f"    stderr: {result.stderr[:200]}")
    return False


def publish(rec_id):
    r = requests.post(f"{BASE}/deposit/depositions/{rec_id}/actions/publish", headers=HEADERS_JSON)
    if r.status_code in (200, 201, 202):
        doi = r.json().get("metadata", {}).get("prereserve_doi", {}).get("doi", "")
        return True, doi
    print(f"  Publish FAILED: {r.status_code} {r.text[:300]}")
    return False, ""


# ============================================================
# MAIN
# ============================================================
if __name__ == "__main__":
    print("=" * 60)
    print("PYTHONSTB WHEELS - ZENODO UPLOAD (curl method)")
    print("=" * 60)

    all_wheels = collect_wheels()
    print(f"Total wheels (2 per package): {len(all_wheels)}")
    print(f"Records needed: {(len(all_wheels) + MAX_FILES - 1) // MAX_FILES}")

    print()
    for i, w in enumerate(all_wheels, 1):
        size = os.path.getsize(w)
        print(f"  {i:3d}. {os.path.basename(w)} ({size:,} bytes)")

    print(f"\nProceed with upload? (y/n)")
    answer = input("> ").strip().lower()
    if answer != "y":
        print("Aborted.")
        sys.exit(0)

    batches = []
    for i in range(0, len(all_wheels), MAX_FILES):
        batches.append(all_wheels[i:i + MAX_FILES])

    for batch_idx, batch in enumerate(batches):
        part = batch_idx + 1
        title = f"PythonSTB Wheels (Part {part})"

        print(f"\n{'=' * 60}")
        print(f"PART {part}: {title}")
        print(f"Wheels: {len(batch)}")
        print(f"{'=' * 60}")

        result = create_record(title)
        if not result:
            print("FAILED. Aborting.")
            sys.exit(1)
        rec_id, bucket_url = result
        print(f"  Record ID: {rec_id}")
        print(f"  Bucket: {bucket_url}")

        ok = 0
        fail = 0
        for i, whl in enumerate(batch):
            name = os.path.basename(whl)
            size = os.path.getsize(whl)
            print(f"  [{i+1}/{len(batch)}] {name} ({size:,})...", end=" ", flush=True)
            if upload_whl_curl(bucket_url, whl):
                ok += 1
                print("OK")
            else:
                fail += 1
                print("FAILED")

        files = list_files(rec_id)
        print(f"\n  Files in record: {len(files)}")

        print(f"  Publishing...")
        ok_pub, doi = publish(rec_id)
        if ok_pub:
            print(f"  DOI: {doi}")
            print(f"  URL: https://zenodo.org/records/{rec_id}")
        else:
            print(f"  FAILED to publish!")

    print(f"\n{'=' * 60}")
    print("ALL DONE!")
    print(f"{'=' * 60}")
