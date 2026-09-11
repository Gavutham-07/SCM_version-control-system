import os
import json
import hashlib
from datetime import datetime
from utils.fossil_utils import fossil_commit

DATASETS_ROOT = os.path.abspath("datasets")

def _next_version(dataset_root: str) -> str:
    if not os.path.exists(dataset_root):
        return "v1"

    versions = [
        d for d in os.listdir(dataset_root)
        if d.startswith("v") and d[1:].isdigit()
    ]
    if not versions:
        return "v1"

    nums = [int(v[1:]) for v in versions]
    return f"v{max(nums) + 1}"

def _checksum(path: str) -> str:
    h = hashlib.sha256()
    with open(path, "rb") as f:
        for chunk in iter(lambda: f.read(8192), b""):
            h.update(chunk)
    return h.hexdigest()

def upload_dataset(dataset_name: str, file_name: str, file_bytes: bytes):
    dataset_root = os.path.join(DATASETS_ROOT, dataset_name)
    version = _next_version(dataset_root)

    version_dir = os.path.join(dataset_root, version)
    os.makedirs(version_dir, exist_ok=False)

    data_path = os.path.join(version_dir, file_name)
    with open(data_path, "wb") as f:
        f.write(file_bytes)

    checksum = _checksum(data_path)

    meta = {
        "dataset": dataset_name,
        "version": version,
        "file": file_name,
        "checksum": checksum,
        "created_at": datetime.utcnow().isoformat()
    }

    with open(os.path.join(version_dir, "meta.json"), "w") as f:
        json.dump(meta, f, indent=2)

    fossil_commit(
        f"[DATASET] {dataset_name}:{version}",
        version_dir
    )

    return meta

def list_datasets():
    if not os.path.exists(DATASETS_ROOT):
        return []

    out = []
    for name in sorted(os.listdir(DATASETS_ROOT)):
        root = os.path.join(DATASETS_ROOT, name)
        if not os.path.isdir(root):
            continue
        versions = sorted(
            d for d in os.listdir(root)
            if d.startswith("v")
        )
        out.append({
            "dataset": name,
            "versions": versions
        })
    return out
