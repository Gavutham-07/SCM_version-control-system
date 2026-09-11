import os
import json
import joblib

PROJECT_ROOT = os.path.abspath(
    os.path.join(os.path.dirname(__file__), "..")
)

EXPERIMENTS_ROOT = os.path.join(PROJECT_ROOT, "experiments")
MODELS_ROOT = os.path.join(PROJECT_ROOT, "models")


def run_inference(experiment_id, input_data: dict):
    exp_dir = os.path.join(EXPERIMENTS_ROOT, experiment_id)

    if not os.path.exists(exp_dir):
        raise FileNotFoundError("Experiment not found")

    # Load config
    with open(os.path.join(exp_dir, "config.json")) as f:
        config = json.load(f)

    model_info = config["model"]

    model_dir = os.path.join(
        MODELS_ROOT,
        model_info["name"],
        model_info["version"]
    )

    model_path = os.path.join(model_dir, "model.bin")

    if not os.path.exists(model_path):
        raise FileNotFoundError("Trained model artifact not found")

    model = joblib.load(model_path)

    # Convert input dict to ordered list
    X = [list(input_data.values())]

    prediction = model.predict(X)

    return {
        "prediction": prediction.tolist(),
        "model": f"{model_info['name']}:{model_info['version']}",
        "experiment_id": experiment_id
    }
