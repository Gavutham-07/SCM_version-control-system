import os
import json
from datetime import datetime

PROJECT_ROOT = os.path.abspath(
    os.path.join(os.path.dirname(__file__), "..")
)

TICKETS_ROOT = os.path.join(PROJECT_ROOT, "tickets")


def _next_ticket_id():
    os.makedirs(TICKETS_ROOT, exist_ok=True)
    existing = [
        d for d in os.listdir(TICKETS_ROOT)
        if d.startswith("tkt-")
    ]
    nums = [int(d.split("-")[1]) for d in existing] if existing else []
    next_num = max(nums) + 1 if nums else 1
    return f"tkt-{next_num:04d}"


def create_ticket(source_type, experiment_id, error, log_path):
    ticket_id = _next_ticket_id()
    ticket_dir = os.path.join(TICKETS_ROOT, ticket_id)
    os.makedirs(ticket_dir, exist_ok=True)

    ticket = {
        "ticket_id": ticket_id,
        "type": "experiment_failure",
        "source": {
            "experiment_id": experiment_id,
            "mode": source_type
        },
        "status": "open",
        "error": error,
        "log_path": log_path,
        "created_at": datetime.utcnow().isoformat()
    }

    with open(os.path.join(ticket_dir, "ticket.json"), "w") as f:
        json.dump(ticket, f, indent=2)

    return ticket_id
