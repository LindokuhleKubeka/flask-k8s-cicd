from flask import Flask, jsonify
import os
import socket
from datetime import datetime

app = Flask(__name__)

# App metadata
APP_NAME = "Flask K8s CI/CD Demo"
VERSION = "1.0.0"
START_TIME = datetime.utcnow()

@app.route("/")
def index():
    """Homepage with basic app info"""
    return jsonify({
        "message": f"Welcome to {APP_NAME} 👋",
        "version": VERSION,
        "hostname": socket.gethostname(),
        "status": "running",
        "timestamp": datetime.utcnow().isoformat()
    })

@app.route("/health")
def health():
    """Kubernetes liveness probe"""
    return jsonify({
        "status": "healthy",
        "timestamp": datetime.utcnow().isoformat()
    }), 200

@app.route("/ready")
def ready():
    """Kubernetes readiness probe"""
    uptime = (datetime.utcnow() - START_TIME).total_seconds()
    return jsonify({
        "status": "ready",
        "uptime_seconds": int(uptime),
        "timestamp": datetime.utcnow().isoformat()
    }), 200

if __name__ == "__main__":
    port = int(os.environ.get("PORT", 5000))
    app.run(host="0.0.0.0", port=port)
