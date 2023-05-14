import json
import threading
from flask import Flask, jsonify, request, abort

from resources.github_app import verify_webhook_signature, process_webhooks
from redis_broker.redis_service import init_redis_client
from redis_broker.redis_consumer import consume_messages
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
        logger.error("Unsupported content type")

    redis_client = init_redis_client()

    # create the data to publish
    data = {
        "channel_name": "issue_create",
        "payload": payload,
    }

    # publish the lock status to the redis client
    redis_client.publish("issue_create", json.dumps(data))

    # Return a success response
    logger.info("Returning 200 response.")
    return "Webhook received and verified", 200


if __name__ == "__main__":
    logger.info("Starting the server")

    # init redis thread process
    redis_thread = threading.Thread(target=consume_messages, daemon=True)
    redis_thread.start()
    app.run(debug=True, host="0.0.0.0", port=8080)
