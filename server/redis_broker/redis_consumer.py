import json
from redis_broker.redis_service import init_redis_client
from resources.helpers import process_webhooks
import logging

# Setup logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


def consume_messages():
    """
    consume the product updates processing message
    """

    # create the redis_client
    redis_client = init_redis_client()

    logger.info("Listening for messages")

    # create the redis subscriber
    redis_subscriber = redis_client.pubsub()

    # subscribe to the issue events
    redis_subscriber.subscribe(
        "issue_create",
    )

    for message in redis_subscriber.listen():
        if message.get("type") == "message":
            data = json.loads(message.get("data"))

            # check message from the product update channel
            if data["channel_name"] == "issue_create":
                process_webhooks(data["payload"])

    return
