import json
import threading
from flask import Flask, jsonify, request, abort
from flask_restful import Resource

from resources.helpers import verify_webhook_signature
from redis_broker.redis_service import init_redis_client
import logging

# Setup logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


class Home(Resource):
    def get(self):
        return "Welcome, Server running successfully!"


class Webhooks(Resource):
    def post(self):
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
