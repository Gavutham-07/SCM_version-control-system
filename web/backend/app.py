from flask import Flask, send_from_directory, redirect
import os

from web.backend.api.experiments import experiments_bp
from web.backend.api.datasets import datasets_bp
from web.backend.api.models import models_bp
from web.backend.api.analytics import analytics_bp
from web.backend.api.replay import replay_bp
from web.backend.api.tickets import tickets_bp

app = Flask(__name__)

FRONTEND_DIR = os.path.abspath("web/frontend")

app.register_blueprint(experiments_bp, url_prefix="/api/experiments")
app.register_blueprint(datasets_bp, url_prefix="/api/datasets")
app.register_blueprint(models_bp, url_prefix="/api/models")
app.register_blueprint(analytics_bp, url_prefix="/api/analytics")
app.register_blueprint(replay_bp, url_prefix="/api/replay")
app.register_blueprint(tickets_bp, url_prefix="/api/tickets")


@app.route("/")
def index():
    return redirect("/ui/experiments.html")


@app.route("/ui/<path:filename>")
def ui_files(filename):
    return send_from_directory(FRONTEND_DIR, filename)


@app.route("/api/health")
def health():
    return {"status": "ok"}


if __name__ == "__main__":
    app.run(debug=True)
