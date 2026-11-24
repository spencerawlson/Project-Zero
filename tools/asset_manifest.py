"""Asset manifest and private backup for Project Zero source assets.

The owner's source models (Meshy GLBs, zips, concept sheets, baked Roblox_Import files) live OUTSIDE this
repository and are proprietary: they are never committed or published. This tool records what they are
(path, size, SHA-256) in a versioned manifest that IS committed, and copies them into a private backup
folder the owner chooses, so a clean clone can tell exactly which files it needs and verify them.

Roots (no machine-specific defaults beyond "the folder that contains this repo"):
  PZ_ASSET_ROOT   folder holding the source assets   (default: parent of the repository)
  PZ_BACKUP_ROOT  private backup folder               (required for backup/restore-test; never inside the repo)
  PZ_MANIFEST     manifest path                       (default: docs/ASSET_MANIFEST.csv; used by the self-test)

Usage:
  python tools/asset_manifest.py build            # (re)write docs/ASSET_MANIFEST.csv
  python tools/asset_manifest.py verify           # compare the files on disk with the manifest
  python tools/asset_manifest.py backup           # copy every manifest file into PZ_BACKUP_ROOT (content-addressed)
  python tools/asset_manifest.py restore-test DIR # restore the backup into DIR and check every hash
"""
from __future__ import annotations

import csv
import hashlib
import os
import shutil
import sys
from pathlib import Path

REPO = Path(__file__).resolve().parents[1]
MANIFEST = Path(os.environ.get("PZ_MANIFEST", REPO / "docs" / "ASSET_MANIFEST.csv")).resolve()
ASSET_EXT = {".glb", ".gltf", ".fbx", ".stl", ".zip", ".png", ".jpg", ".pdf", ".json", ".rbxl", ".rbxm"}
SKIP_DIRS = {REPO.name, "Backups", "__pycache__", ".git"}


def asset_root() -> Path:
    return Path(os.environ.get("PZ_ASSET_ROOT", REPO.parent)).resolve()


def backup_root() -> Path:
    value = os.environ.get("PZ_BACKUP_ROOT")
    if not value:
        sys.exit("PZ_BACKUP_ROOT is not set: choose a private folder (an external drive or a private cloud-synced folder).")
    root = Path(value).resolve()
    if REPO in root.parents or root == REPO:
        sys.exit("PZ_BACKUP_ROOT must not be inside the repository (source assets are never committed).")
    return root


def sha256(path: Path) -> str:
    h = hashlib.sha256()
    with path.open("rb") as f:
        for chunk in iter(lambda: f.read(1 << 20), b""):
            h.update(chunk)
    return h.hexdigest()


def scan(root: Path):
    for dirpath, dirnames, filenames in os.walk(root):
        dirnames[:] = sorted(d for d in dirnames if d not in SKIP_DIRS)
        for name in sorted(filenames):
            p = Path(dirpath) / name
            if p.suffix.lower() in ASSET_EXT:
                yield p


def read_manifest():
    with MANIFEST.open(newline="", encoding="utf-8") as f:
        return list(csv.DictReader(f))


def build():
    root = asset_root()
    rows = []
    for p in scan(root):
        rows.append({"path": p.relative_to(root).as_posix(), "bytes": p.stat().st_size, "sha256": sha256(p)})
    MANIFEST.parent.mkdir(parents=True, exist_ok=True)
    with MANIFEST.open("w", newline="", encoding="utf-8") as f:
        w = csv.DictWriter(f, fieldnames=["path", "bytes", "sha256"], lineterminator="\n")
        w.writeheader()
        w.writerows(rows)
    total = sum(int(r["bytes"]) for r in rows)
    print(f"manifest: {len(rows)} files, {total / 1e6:.1f} MB -> {MANIFEST.name}")


def verify(root: Path | None = None) -> int:
    root = root or asset_root()
    missing = changed = 0
    for row in read_manifest():
        p = root / row["path"]
        if not p.exists():
            missing += 1
            print("MISSING ", row["path"])
        elif p.stat().st_size != int(row["bytes"]) or sha256(p) != row["sha256"]:
            changed += 1
            print("CHANGED ", row["path"])
    rows = len(read_manifest())
    print(f"verify: {rows} listed, {missing} missing, {changed} changed")
    return 1 if (missing or changed) else 0


def backup():
    src, dst = asset_root(), backup_root()
    store = dst / "objects"
    copied = 0
    for row in read_manifest():
        obj = store / row["sha256"][:2] / row["sha256"]
        if obj.exists():
            continue
        obj.parent.mkdir(parents=True, exist_ok=True)
        tmp = obj.with_suffix(".part")
        shutil.copyfile(src / row["path"], tmp)
        if sha256(tmp) != row["sha256"]:
            tmp.unlink()
            sys.exit(f"hash mismatch while copying {row['path']}: run 'build' first if the file changed on purpose")
        tmp.replace(obj)
        copied += 1
    snap = dst / "manifests"
    snap.mkdir(parents=True, exist_ok=True)
    stamp = hashlib.sha256(MANIFEST.read_bytes()).hexdigest()[:12]
    shutil.copyfile(MANIFEST, snap / f"ASSET_MANIFEST_{stamp}.csv")
    print(f"backup: {copied} new objects copied, manifest snapshot {stamp}")


def restore_test(target: str):
    src, out = backup_root() / "objects", Path(target).resolve()
    for row in read_manifest():
        dest = out / row["path"]
        dest.parent.mkdir(parents=True, exist_ok=True)
        shutil.copyfile(src / row["sha256"][:2] / row["sha256"], dest)
    sys.exit(verify(out))


if __name__ == "__main__":
    cmd = sys.argv[1] if len(sys.argv) > 1 else ""
    if cmd == "build":
        build()
    elif cmd == "verify":
        sys.exit(verify())
    elif cmd == "backup":
        backup()
    elif cmd == "restore-test" and len(sys.argv) > 2:
        restore_test(sys.argv[2])
    else:
        sys.exit(__doc__)
