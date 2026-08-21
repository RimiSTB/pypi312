"""
Verify wheel integrity before pushing to GitHub.
Run: python verify_wheel_integrity.py
Checks: underscore folders, BOM in WHEEL, RECORD hash mismatches, folder naming, Generator tag.
"""
import os, zipfile, hashlib, base64, glob, sys, re

WHEEL_DIR = os.path.join(os.path.dirname(__file__), 'wheels')
errors = []

# Check 1: No underscore folders with android wheels
print('=== CHECK 1: Underscore folders ===')
underscore_folders = []
for f in os.listdir(WHEEL_DIR):
    full = os.path.join(WHEEL_DIR, f)
    if not os.path.isdir(full) or '_' not in f:
        continue
    whls = [x for x in os.listdir(full) if x.endswith('.whl') and 'android' in x]
    if whls:
        underscore_folders.append(f)
if underscore_folders:
    errors.append(f'Underscore folders: {underscore_folders}')
    print(f'  FAIL: {underscore_folders}')
else:
    print('  ALL CLEAR')

# Check 2: No BOM in WHEEL files
print('=== CHECK 2: BOM in WHEEL files ===')
bom_count = 0
for whl_path in glob.glob(os.path.join(WHEEL_DIR, '**', '*.whl'), recursive=True):
    if 'android' not in os.path.basename(whl_path):
        continue
    try:
        with zipfile.ZipFile(whl_path) as z:
            for name in z.namelist():
                if name.endswith('.dist-info/WHEEL'):
                    if z.read(name)[:3] == b'\xef\xbb\xbf':
                        bom_count += 1
                        print(f'  BOM: {os.path.relpath(whl_path, WHEEL_DIR)}')
    except Exception:
        pass
if bom_count:
    errors.append(f'BOM found in {bom_count} WHEELS')
else:
    print('  ALL CLEAR')

# Check 3: All WHEEL hashes in RECORD match
print('=== CHECK 3: WHEEL hash mismatches ===')
bad_hash = 0
for whl_path in glob.glob(os.path.join(WHEEL_DIR, '**', '*.whl'), recursive=True):
    if 'android' not in os.path.basename(whl_path):
        continue
    try:
        with zipfile.ZipFile(whl_path) as z:
            record_name = [n for n in z.namelist() if n.endswith('.dist-info/RECORD')][0]
            wheel_name = [n for n in z.namelist() if n.endswith('.dist-info/WHEEL')][0]
            record_lines = z.read(record_name).decode('utf-8').strip().splitlines()
            correct_hash = 'sha256=' + base64.urlsafe_b64encode(
                hashlib.sha256(z.read(wheel_name)).digest()
            ).rstrip(b'=').decode()
            for line in record_lines:
                parts = line.rsplit(',', 2)
                if len(parts) == 3 and 'WHEEL' in parts[0] and parts[1].startswith('sha256='):
                    if parts[1] != correct_hash:
                        bad_hash += 1
                        print(f'  MISMATCH: {os.path.relpath(whl_path, WHEEL_DIR)}')
    except Exception as e:
        bad_hash += 1
        print(f'  ERROR: {os.path.basename(whl_path)}: {e}')
if bad_hash:
    errors.append(f'WHEEL hash mismatch in {bad_hash} wheels')
else:
    print('  ALL CLEAR')

# Check 4: All folder names match pip normalization
print('=== CHECK 4: Folder naming ===')
bad_names = []
for f in os.listdir(WHEEL_DIR):
    full = os.path.join(WHEEL_DIR, f)
    if not os.path.isdir(full):
        continue
    normalized = f.lower().replace('_', '-').replace('.', '-')
    if normalized != f:
        bad_names.append(f)
if bad_names:
    errors.append(f'Folders need renaming: {bad_names}')
    print(f'  FAIL: {bad_names}')
else:
    print('  ALL CLEAR')

# Check 5: Generator tag is PythonSTB-RIMI-Build (no opencode/pynacl/other banned values)
print('=== CHECK 5: Generator tag ===')
ALLOWED_GENERATOR = 'PythonSTB-RIMI-Build'
bad_gen = 0
for whl_path in glob.glob(os.path.join(WHEEL_DIR, '**', '*.whl'), recursive=True):
    if 'android' not in os.path.basename(whl_path):
        continue
    try:
        with zipfile.ZipFile(whl_path) as z:
            for name in z.namelist():
                if name.endswith('.dist-info/WHEEL'):
                    content = z.read(name).decode('utf-8')
                    for line in content.splitlines():
                        if line.lower().startswith('generator:'):
                            gen_val = line.split(':', 1)[1].strip()
                            if gen_val != ALLOWED_GENERATOR:
                                bad_gen += 1
                                print(f'  BAD: {os.path.relpath(whl_path, WHEEL_DIR)} -> Generator: {gen_val}')
                            break
    except Exception as e:
        bad_gen += 1
        print(f'  ERROR: {os.path.basename(whl_path)}: {e}')
if bad_gen:
    errors.append(f'Wrong Generator tag in {bad_gen} wheels (must be {ALLOWED_GENERATOR})')
else:
    print(f'  ALL CLEAR — all use {ALLOWED_GENERATOR}')

# Summary
print()
if errors:
    print(f'FAILED: {len(errors)} check(s) failed')
    for e in errors:
        print(f'  - {e}')
    sys.exit(1)
else:
    print('ALL CHECKS PASSED - safe to push')
    sys.exit(0)
