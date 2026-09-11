from flask import Blueprint, request, jsonify
from utils.dataset_manager import upload_dataset, list_datasets

datasets_bp = Blueprint("datasets", __name__)

@datasets_bp.route("/", methods=["POST"])
def upload():
    if "file" not in request.files:
        return {"error": "file required"}, 400
    name = request.form.get("dataset")
    if not name:
        return {"error": "dataset name required"}, 400

    f = request.files["file"]
    meta = upload_dataset(name, f.filename, f.read())
    return jsonify(meta), 201

@datasets_bp.route("/", methods=["GET"])
def list_all():
    return jsonify(list_datasets())
