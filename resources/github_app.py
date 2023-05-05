# Add all the resources for the github app
import json
import os
import hmac
import hashlib
import base64
from dotenv import load_dotenv
from log_mod import logger
from helpers.github_helpers import GithubAPI
from helpers.open_ai_helpers import SearchIssue

load_dotenv()


def verify_webhook_signature(data, signature):
    """Verify GitHub webhook signature."""

    secret = os.getenv("WEBHOOK_SECRET_KEY")
    digest = hmac.new(secret.encode("utf-8"), data, hashlib.sha256).hexdigest()
    return hmac.compare_digest("sha256=" + digest, signature)


def parse_webhooks():
    # method implementation to verify the webhooks
    pass


def check_similar_issue():
    repo_name = "deepak2431/djangoBlog"

    github_api = GithubAPI(repo_name=repo_name)
    df = github_api.get_issues()

    issue_searcher = SearchIssue(df)
    issue_searcher.generate_embeddings()
    similar_issue = issue_searcher.find_similar_issues(new_issue="draft post", n=3)

    with open("result.json", "w") as f:
        json.dump(similar_issue, f, indent=4)
