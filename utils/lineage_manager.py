import json
import os
from datetime import datetime

PROJECT_ROOT = os.path.abspath(
    os.path.join(os.path.dirname(__file__), "..")
)

LINEAGE_FILE = os.path.join(PROJECT_ROOT, "lineage", "lineage.json")


def load_lineage():
    if not os.path.exists(LINEAGE_FILE):
        return {}
    with open(LINEAGE_FILE) as f:
        return json.load(f)


def save_lineage(data):
    os.makedirs(os.path.dirname(LINEAGE_FILE), exist_ok=True)
    with open(LINEAGE_FILE, "w") as f:
        json.dump(data, f, indent=2)


def record_lineage(experiment_id, dataset, model, status):
    lineage = load_lineage()

    lineage[experiment_id] = {
        "dataset": f"{dataset['name']}:{dataset['version']}",
        "model": f"{model['name']}:{model['version']}",
        "config_path": f"experiments/{experiment_id}/config.json",
        "executed_at": datetime.utcnow().isoformat(),
        "status": status
    }

    save_lineage(lineage)
