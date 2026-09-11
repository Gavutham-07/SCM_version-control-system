from flask import Blueprint
from utils.replay_executor import replay_experiment

replay_bp = Blueprint("replay", __name__)


@replay_bp.route("/<experiment_id>", methods=["POST"])
def replay(experiment_id):
    try:
        metrics = replay_experiment(experiment_id)
        return metrics, 200
    except Exception as e:
        return {"error": str(e)}, 500
