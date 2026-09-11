import os
import json
from datetime import datetime
from utils.fossil_utils import fossil_commit

MODELS_ROOT = os.path.abspath("models")

def _next_version(model_root: str) -> str:
    if not os.path.exists(model_root):
        return "v1"

    versions = [
        d for d in os.listdir(model_root)
        if d.startswith("v") and d[1:].isdigit()
    ]
    if not versions:
        return "v1"

    nums = [int(v[1:]) for v in versions]
    return f"v{max(nums) + 1}"

def register_model(model_name: str, script_name: str, script_bytes: bytes):
    model_root = os.path.join(MODELS_ROOT, model_name)
    version = _next_version(model_root)

    version_dir = os.path.join(model_root, version)
    os.makedirs(version_dir, exist_ok=False)

    script_path = os.path.join(version_dir, script_name)
    with open(script_path, "wb") as f:
        f.write(script_bytes)

    meta = {
        "model": model_name,
        "version": version,
        "script": script_name,
        "created_at": datetime.utcnow().isoformat()
    }

    with open(os.path.join(version_dir, "model_meta.json"), "w") as f:
        json.dump(meta, f, indent=2)

    fossil_commit(
        f"[MODEL] {model_name}:{version}",
        version_dir
    )

    return meta

def list_models():
    if not os.path.exists(MODELS_ROOT):
        return []

    out = []
    for name in sorted(os.listdir(MODELS_ROOT)):
        root = os.path.join(MODELS_ROOT, name)
        if not os.path.isdir(root):
            continue

        versions = sorted(
            d for d in os.listdir(root)
            if d.startswith("v")
        )

        out.append({
            "model": name,
            "versions": versions
        })

    return out
