from pprint import pprint
import json
from flask import Flask, jsonify


app = Flask(__name__)


@app.route("/")
def home():
    return "Welcome, Server running successfully!"

@app.route("/webhooks", methods=['POST'])
def github_webhooks():
    return "This is webhooks endpoint!"


if __name__ == "__main__":
    app.run(debug=True)

