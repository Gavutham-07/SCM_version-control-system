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
REPLAY_ROOT = os.path.join(PROJECT_ROOT, "replay")


def replay_experiment(experiment_id):
    exp_dir = os.path.join(EXPERIMENTS_ROOT, experiment_id)
    if not os.path.exists(exp_dir):
        raise FileNotFoundError("Original experiment not found")

    # Load original config
    with open(os.path.join(exp_dir, "config.json")) as f:
        config = json.load(f)

    dataset = config["dataset"]
    model = config["model"]
    params = config.get("hyperparameters", {})

    dataset_dir = os.path.join(
        DATASETS_ROOT, dataset["name"], dataset["version"]
    )

    model_dir = os.path.join(
        MODELS_ROOT, model["name"], model["version"]
    )

    train_script = os.path.join(model_dir, "train.py")
    if not os.path.exists(train_script):
        raise FileNotFoundError("train.py not found for model version")

    # Prepare replay directory
    replay_dir = os.path.join(REPLAY_ROOT, experiment_id)
    logs_dir = os.path.join(replay_dir, "logs")
    os.makedirs(logs_dir, exist_ok=True)

    log_path = os.path.join(logs_dir, "replay_training.log")

    # Execute training (same contract as Feature 4)
    with open(log_path, "w") as logf:
        result = subprocess.run(
            [
                "python",
                train_script,
                dataset_dir,
                json.dumps(params)
            ],
            stdout=logf,
            stderr=subprocess.STDOUT,
            cwd=PROJECT_ROOT
        )

    metrics = {
        "status": "success" if result.returncode == 0 else "failed",
        "return_code": result.returncode,
        "replayed_at": datetime.utcnow().isoformat()
    }

    with open(os.path.join(replay_dir, "metrics.json"), "w") as f:
        json.dump(metrics, f, indent=2)

    meta = {
        "original_experiment_id": experiment_id,
        "replayed_at": metrics["replayed_at"],
        "replay_type": "deterministic"
    }

    with open(os.path.join(replay_dir, "replay_meta.json"), "w") as f:
        json.dump(meta, f, indent=2)

    return metrics
