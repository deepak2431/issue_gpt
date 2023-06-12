import json

from redis_broker.redis_service import redis_client
from resources.helpers import process_webhooks
from helpers.log_mod import logger


is_subscribed = False


def consume_messages():
    """
    consume the product updates processing message
    """

    # create the redis_client

    logger.info("Listening for messages")
    global is_subscribed

    # create the redis subscriber
    redis_subscriber = redis_client.pubsub()

    if not is_subscribed:
        # subscribe to the issue events
        redis_subscriber.subscribe(
            "issue_create",
        )
        is_subscribed = True

    for message in redis_subscriber.listen():
        if message.get("type") == "message":
            data = json.loads(message.get("data"))

            # check message from the product update channel
            if data["channel_name"] == "issue_create":
                process_webhooks(data["payload"])

    return
