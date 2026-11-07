import json
import os
from flask import Flask, jsonify, render_template

app = Flask(__name__)
STATE_FILE = os.getenv("STATE_FILE", os.path.join(os.path.dirname(__file__), "..", "state.json"))


def load_state():
    try:
        with open(STATE_FILE) as f:
            return json.load(f)
    except (FileNotFoundError, json.JSONDecodeError):
        return {"status": "waiting for bot"}


@app.route("/")
def index():
    return render_template("index.html")


@app.route("/api/state")
def api_state():
    return jsonify(load_state())


if __name__ == "__main__":
    # Bind to localhost only so the dashboard isn't exposed to the internet.
    app.run(host="127.0.0.1", port=5000, debug=False)
