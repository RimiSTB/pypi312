"""
Zenodo Upload Script for PythonSTB Wheels - FINAL VERSION
Rules:
  - ONE record at a time, title "PythonSTB Wheels (Part X)"
  - Upload ALL wheels FIRST, then publish at the END
  - Max 100 files per record
  - 2 wheels per package (arm64_v8a + x86_64), no duplicates
  - After record is full (100/100), publish, then create Part 2
"""

import glob, os, sys, time, requests

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

    # Group by normalized package name (first part before version)
    by_pkg = {}
    for w in all_w:
        name = os.path.basename(w)
        # Package name = everything before the first digit in the version
        # e.g. numpy-2.5.2-... -> numpy
        parts = name.split("-")
        pkg_key = parts[0].lower()  # normalize case
        if pkg_key not in by_pkg:
            by_pkg[pkg_key] = {}
        if "arm64" in name:
            by_pkg[pkg_key]["arm64"] = w
        elif "x86_64" in name:
            by_pkg[pkg_key]["x86_64"] = w
        else:
            # pure python (no arch)
            by_pkg[pkg_key]["pure"] = w

    # Build final list: 2 per package
    deduped = []
    for pkg_key in sorted(by_pkg.keys()):
        archs = by_pkg[pkg_key]
        if "arm64" in archs and "x86_64" in archs:
            deduped.append(archs["arm64"])
            deduped.append(archs["x86_64"])
        elif "pure" in archs:
            deduped.append(archs["pure"])
        else:
            # Only one arch available, add it
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
            "notes": "Generator: PythonSTB-RIMI-Build",
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


def upload_whl(bucket_url, filepath):
    filename = os.path.basename(filepath)
    size = os.path.getsize(filepath)
    with open(filepath, "rb") as f:
        r = requests.put(f"{bucket_url}/{filename}", headers=HEADERS_AUTH, data=f)
    if r.status_code in (200, 201):
        return True
    print(f"  FAILED: {filename} ({r.status_code})")
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
    print("PYTHONSTB WHEELS - ZENODO UPLOAD")
    print("=" * 60)

    all_wheels = collect_wheels()
    print(f"Total wheels (2 per package): {len(all_wheels)}")
    print(f"Records needed: {(len(all_wheels) + MAX_FILES - 1) // MAX_FILES}")

    # Show what we'll upload
    print()
    for i, w in enumerate(all_wheels, 1):
        print(f"  {i:3d}. {os.path.basename(w)}")

    # Ask confirmation
    print(f"\nProceed with upload? (y/n)")
    answer = input("> ").strip().lower()
    if answer != "y":
        print("Aborted.")
        sys.exit(0)

    # Split into batches
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

        # Create record
        result = create_record(title)
        if not result:
            print("FAILED. Aborting.")
            sys.exit(1)
        rec_id, bucket_url = result
        print(f"  Record ID: {rec_id}")

        # Upload ALL wheels (NO PUBLISH YET)
        ok = 0
        fail = 0
        for i, whl in enumerate(batch):
            if upload_whl(bucket_url, whl):
                ok += 1
            else:
                fail += 1
            if (i + 1) % 10 == 0 or (i + 1) == len(batch):
                print(f"  Progress: {i + 1}/{len(batch)} (OK:{ok} FAIL:{fail})")

        # Verify
        files = list_files(rec_id)
        print(f"\n  Files in record: {len(files)}")

        # NOW publish
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
