from flask import Blueprint, request
from utils.experiment_comparator import compare_experiments

analytics_bp = Blueprint("analytics", __name__)


@analytics_bp.route("/compare", methods=["GET", "POST"])
def compare():
    try:
        data = request.get_json(silent=True)
        selected = None

        if data and "experiments" in data:
            selected = data["experiments"]

        result = compare_experiments(selected)
        return result, 200

    except Exception as e:
        return {"error": str(e)}, 500
