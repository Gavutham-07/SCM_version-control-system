import os
import json
import subprocess
from datetime import datetime

PROJECT_ROOT = os.path.abspath(
    os.path.join(os.path.dirname(__file__), "..")
)

DATASETS_ROOT = os.path.join(PROJECT_ROOT, "datasets")
MODELS_ROOT = os.path.join(PROJECT_ROOT, "models")
EXPERIMENTS_ROOT = os.path.join(PROJECT_ROOT, "experiments")


def run_experiment(experiment_id):
    exp_dir = os.path.join(EXPERIMENTS_ROOT, experiment_id)

    if not os.path.exists(exp_dir):
        raise FileNotFoundError("Experiment not found")

    # Load experiment config
    with open(os.path.join(exp_dir, "config.json")) as f:
        config = json.load(f)

    dataset = config["dataset"]
    model = config["model"]
    hyperparams = config.get("hyperparameters", {})

    dataset_dir = os.path.join(
        DATASETS_ROOT,
        dataset["name"],
        dataset["version"]
    )

    model_dir = os.path.join(
        MODELS_ROOT,
        model["name"],
        model["version"]
    )

    train_script = os.path.join(model_dir, "train.py")

    if not os.path.exists(dataset_dir):
        raise FileNotFoundError("Dataset version not found")

    if not os.path.exists(train_script):
        raise FileNotFoundError("train.py not found in model version")

    # Prepare output directory
    output_dir = os.path.join(exp_dir, "output")
    os.makedirs(output_dir, exist_ok=True)

    log_path = os.path.join(output_dir, "training.log")

    # Execute training
    with open(log_path, "w") as logf:
        result = subprocess.run(
            [
                "python",
                train_script,
                dataset_dir,
                output_dir,
                json.dumps(hyperparams)
            ],
            stdout=logf,
            stderr=subprocess.STDOUT,
            cwd=PROJECT_ROOT
        )

    metrics = {
        "status": "success" if result.returncode == 0 else "failed",
        "return_code": result.returncode,
        "finished_at": datetime.utcnow().isoformat()
    }

    with open(os.path.join(output_dir, "run_status.json"), "w") as f:
        json.dump(metrics, f, indent=2)

    return metrics
