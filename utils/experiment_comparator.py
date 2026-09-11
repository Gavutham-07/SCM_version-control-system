import os
import json
from datetime import datetime

PROJECT_ROOT = os.path.abspath(
    os.path.join(os.path.dirname(__file__), "..")
)

EXPERIMENTS_ROOT = os.path.join(PROJECT_ROOT, "experiments")


def compare_experiments(selected_experiments=None):
    """
    Dynamically compares experiments.
    If selected_experiments is None → compare all.
    """

    if not os.path.exists(EXPERIMENTS_ROOT):
        raise FileNotFoundError("experiments directory not found")

    experiment_ids = selected_experiments

    if not experiment_ids:
        experiment_ids = [
            d for d in os.listdir(EXPERIMENTS_ROOT)
            if d.startswith("exp-")
        ]

    comparison_results = []

    for exp_id in experiment_ids:
        exp_dir = os.path.join(EXPERIMENTS_ROOT, exp_id)

        config_path = os.path.join(exp_dir, "config.json")
        metrics_path = os.path.join(exp_dir, "output", "metrics.json")
        status_path = os.path.join(exp_dir, "output", "run_status.json")

        if not os.path.exists(config_path):
            continue

        with open(config_path) as f:
            config = json.load(f)

        metrics = {}
        if os.path.exists(metrics_path):
            with open(metrics_path) as mf:
                metrics = json.load(mf)

        status = {}
        if os.path.exists(status_path):
            with open(status_path) as sf:
                status = json.load(sf)

        comparison_entry = {
            "experiment_id": exp_id,
            "dataset": f"{config['dataset']['name']}:{config['dataset']['version']}",
            "model": f"{config['model']['name']}:{config['model']['version']}",
            "status": status.get("status", "unknown"),
            "metrics": metrics  # dynamic metrics
        }

        comparison_results.append(comparison_entry)

    return {
        "generated_at": datetime.utcnow().isoformat(),
        "experiments": comparison_results
    }
