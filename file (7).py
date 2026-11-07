import json
import os
import tempfile
import time

STATE_FILE = os.getenv("STATE_FILE", "state.json")


def write_state(data: dict) -> None:
    """Atomically write the bot's current state so the dashboard never reads a half-written file."""
    data = {**data, "updated_at": time.time()}
    directory = os.path.dirname(os.path.abspath(STATE_FILE))
    with tempfile.NamedTemporaryFile("w", dir=directory, delete=False, suffix=".tmp") as tmp:
        json.dump(data, tmp, indent=2, default=str)
        tmp_name = tmp.name
    os.replace(tmp_name, STATE_FILE)
