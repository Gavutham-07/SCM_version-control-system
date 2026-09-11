import os
import json
from datetime import datetime

from utils.experiments_id import generate_experiment_id

PROJECT_ROOT = os.path.abspath(
    os.path.join(os.path.dirname(__file__), "..")
)

EXPERIMENTS_ROOT = os.path.join(PROJECT_ROOT, "experiments")


def create_experiment(dataset, model, hyperparameters):
    if not dataset or not model:
        raise ValueError("dataset and model required")

    # 🔹 NEW: semantic experiment ID
    exp_id = generate_experiment_id(dataset, model)

    exp_dir = os.path.join(EXPERIMENTS_ROOT, exp_id)
    os.makedirs(exp_dir, exist_ok=False)

    config = {
        "dataset": dataset,
        "model": model,
        "hyperparameters": hyperparameters or {}
    }

    meta = {
        "experiment_id": exp_id,
        "created_at": datetime.utcnow().isoformat()
    }

    with open(os.path.join(exp_dir, "config.json"), "w") as f:
        json.dump(config, f, indent=2)

    with open(os.path.join(exp_dir, "experiment_meta.json"), "w") as f:
        json.dump(meta, f, indent=2)

    return exp_id
