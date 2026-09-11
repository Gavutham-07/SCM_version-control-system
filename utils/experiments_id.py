import os
import re

PROJECT_ROOT = os.path.abspath(
    os.path.join(os.path.dirname(__file__), "..")
)

EXPERIMENTS_ROOT = os.path.join(PROJECT_ROOT, "experiments")


def generate_experiment_id(dataset, model):
    dataset_name = dataset["name"]
    dataset_version = dataset["version"].lstrip("v")

    model_name = model["name"]
    model_version = model["version"].lstrip("v")

    base = f"exp-{dataset_name}-{model_name}-d{dataset_version}-m{model_version}"

    existing_runs = []

    if os.path.exists(EXPERIMENTS_ROOT):
        for name in os.listdir(EXPERIMENTS_ROOT):
            if name.startswith(base):
                match = re.search(r"-r(\d+)$", name)
                if match:
                    existing_runs.append(int(match.group(1)))

    next_run = max(existing_runs, default=0) + 1
    return f"{base}-r{next_run}"
