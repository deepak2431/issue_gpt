import threading
from flask import Flask
from flask_restful import Api
from flask_cors import CORS

from redis_broker.redis_consumer import consume_messages

from models.database import initialize_db
from resources.routes import initialize_routes

from helpers.log_mod import logger


def create_app():
    """Initialize the core application"""

    app = Flask(__name__)
    CORS(app)
    api = Api(app)
    app.config.from_object("config.Config")

    initialize_routes(api)
    initialize_db(app)

    # init redis thread process
    redis_thread = threading.Thread(target=consume_messages, daemon=True)
    redis_thread.start()

    return app


if __name__ == "__main__":
    logger.info("Starting the server")

    app = create_app()
    app.run(debug=True, port=8000, host="0.0.0.0")
