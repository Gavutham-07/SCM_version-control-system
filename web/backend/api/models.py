from flask import Blueprint, request, jsonify
from utils.model_manager import register_model, list_models

models_bp = Blueprint("models", __name__)

@models_bp.route("/", methods=["POST"])
def register():
    if "file" not in request.files:
        return {"error": "training script required"}, 400

    model_name = request.form.get("model")
    if not model_name:
        return {"error": "model name required"}, 400

    f = request.files["file"]
    meta = register_model(model_name, f.filename, f.read())
    return jsonify(meta), 201

@models_bp.route("/", methods=["GET"])
def list_all():
    return jsonify(list_models())
