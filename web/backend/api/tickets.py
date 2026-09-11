from flask import Blueprint, jsonify
import os
import json

tickets_bp = Blueprint("tickets", __name__)

TICKETS_ROOT = os.path.abspath("tickets")


@tickets_bp.route("/", methods=["GET"])
def list_tickets():
    if not os.path.exists(TICKETS_ROOT):
        return []

    tickets = []
    for tkt in sorted(os.listdir(TICKETS_ROOT)):
        path = os.path.join(TICKETS_ROOT, tkt, "ticket.json")
        if os.path.exists(path):
            with open(path) as f:
                tickets.append(json.load(f))

    return tickets
