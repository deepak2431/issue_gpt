from pprint import pprint

import json
from flask import Flask, jsonify, request, abort

from resources.github_app import verify_webhook_signature
from log_mod import logger


app = Flask(__name__)


@app.route("/")
def home():
    return "Welcome, Server running successfully!"


@app.route("/webhooks", methods=["POST"])
def receive_github_webhook():
    """Receive and verify GitHub webhook."""
    logger.info("GitHub webhook received.")
    # Retrieve the signature from the request header
    signature = request.headers.get("X-Hub-Signature-256")
    if not signature:
        logger.warning("Missing X-Hub-Signature-256 header. Aborting with 400.")
        abort(400, "Missing X-Hub-Signature-256 header")

    # Check if the payload is empty
    if not request.data:
        logger.info("Received empty payload")
        return "Empty payload", 200

    # Verify the signature
    if not verify_webhook_signature(request.data, signature):
        logger.warning("Invalid signature. Aborting with 400.")
        abort(400, "Invalid signature")

    payload = None

    # Parse the payload and process the webhook (add your logic here)
    content_type = request.headers.get("Content-Type")
    if content_type == "application/x-www-form-urlencoded":
        payload = request.form
    elif content_type == "application/json":
        payload = request.get_json()
    else:
        abort(400, "Unsupported content type")

    with open("hooks.json", "w") as f:
        json.dump(payload, f, indent=4)

    # Return a success response
    logger.info("Returning 200 response.")
    return "Webhook received and verified", 200


if __name__ == "__main__":
    logger.info("Starting the server")
    app.run(debug=True, host="0.0.0.0", port=8080)
