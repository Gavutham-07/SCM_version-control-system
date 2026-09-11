from flask import Blueprint, request, jsonify
from utils.experiment_manager import create_experiment
import os
from utils.experiment_executor import run_experiment
from utils.inference_engine import run_inference
import json
import joblib
import numpy as np

experiments_bp = Blueprint("experiments", __name__)


@experiments_bp.route("/", methods=["POST"])
def create():
    data = request.get_json()
    if not data:
        return {"error": "JSON body required"}, 400

    try:
        exp_id = create_experiment(
            dataset=data.get("dataset"),
            model=data.get("model"),
            hyperparameters=data.get("hyperparameters")
        )
        return {
            "experiment_id": exp_id,
            "status": "created"
        }, 201

    except Exception as e:
        return {"error": str(e)}, 400


@experiments_bp.route("/", methods=["GET"])
def list_all():
    root = os.path.abspath("experiments")
    if not os.path.exists(root):
        return []
    return sorted(d for d in os.listdir(root) if d.startswith("exp-"))

@experiments_bp.route("/<experiment_id>/run", methods=["POST"])
def run(experiment_id):
    try:
        metrics = run_experiment(experiment_id)
        return metrics, 200
    except Exception as e:
        return {"error": str(e)}, 500

@experiments_bp.route("/<experiment_id>/output", methods=["GET"])
def get_output(experiment_id):
    base = os.path.join("experiments", experiment_id)

    if not os.path.exists(base):
        return {"error": "Experiment not found"}, 404

    def load(path):
        return json.load(open(path)) if os.path.exists(path) else None

    return {
        "experiment_meta": load(os.path.join(base, "experiment_meta.json")),
        "run_meta": load(os.path.join(base, "run_meta.json")),
        "metrics": load(os.path.join(base, "output", "metrics.json")),
        "model_exists": os.path.exists(os.path.join(base, "output", "model.bin")),
        "log": open(os.path.join(base, "output", "training.log")).read()
        if os.path.exists(os.path.join(base, "output", "training.log"))
        else None
    }
    import joblib
import numpy as np

@experiments_bp.route("/<experiment_id>/predict", methods=["POST"])
def predict(experiment_id):
    base = os.path.join("experiments", experiment_id, "output")
    model_path = os.path.join(base, "model.bin")

    if not os.path.exists(model_path):
        return {"error": "Trained model not found"}, 404

    data = request.get_json()
    if not data:
        return {"error": "Input data required"}, 400

    # Enforce feature order
    try:
        features = [
            data["age"],
            data["income"],
            data["loan_amount"],
            data["credit_score"]
        ]
    except KeyError as e:
        return {"error": f"Missing feature: {str(e)}"}, 400

    model = joblib.load(model_path)
    prediction = model.predict([features])[0]

    return {
        "experiment_id": experiment_id,
        "prediction": int(prediction)
    }
    
@experiments_bp.route("/<experiment_id>/infer", methods=["POST"])
def infer(experiment_id):
    try:
        data = request.get_json()
        if not data:
            return {"error": "input data required"}, 400

        result = run_inference(experiment_id, data)
        return result, 200

    except Exception as e:
        return {"error": str(e)}, 500

