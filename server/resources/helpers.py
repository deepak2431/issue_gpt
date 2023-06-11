import json
import os
import hmac
import hashlib
from dotenv import load_dotenv
from resources.github_app import GithubApp

import logging

# Setup logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

load_dotenv()


def verify_webhook_signature(data, signature):
    """Verify GitHub webhook signature."""

    logger.info("Verifying webhook signature...")

    secret = os.getenv("WEBHOOK_SECRET_KEY")
    logger.info(f"Using secret key: {secret}")

    digest = hmac.new(secret.encode("utf-8"), data, hashlib.sha256).hexdigest()
    logger.info(f"Calculated digest: {digest}")

    result = hmac.compare_digest("sha256=" + digest, signature)
    logger.info(f"Signature verification result: {result}")

    return result


def parse_webhooks(data):
    """Parse JSON webhook payload and return issue details."""

    logger.info("Parsing webhook payload...")

    # extracts the owner, repo name, issue number, title and body from the JSON data
    action = data["action"]
    owner = data["repository"]["owner"]["login"]
    repo = data["repository"]["name"]
    issue_number = data["issue"]["number"]
    issue_title = data["issue"]["title"]
    issue_body = data["issue"]["body"]

    # returns the extracted details
    return {
        "owner": owner,
        "action": action,
        "repo": repo,
        "issue_number": issue_number,
        "title": issue_title,
        "body": issue_body,
    }


def process_webhooks(webhooks_data):
    """
    Process GitHub webhooks and add comments to issues.

    Parameters:
    webhooks_data (dict): The JSON payload from the GitHub webhook.

    Functionality:
    - Logs that GitHub webhooks are being processed.
    - Parses the webhook payload using the parse_webhooks() function.
    - Adds a comment to the issue using the post_comments() function.
    - Logs whether the comment was added successfully or failed.

    Returns:
    None
    """

    logger.info("Processing GitHub webhooks...")

    # Parse the webhook payload
    parsed_data = parse_webhooks(data=webhooks_data)

    webhook_action = parsed_data["action"]

    logger.info(f"Processing GitHub webhooks with action {webhook_action}")

    if parsed_data["action"] == "opened":
        github_app = GithubApp(
            owner=parsed_data["owner"],
            repo=parsed_data["repo"],
            issue_title=parsed_data["title"],
            issue_body=parsed_data["body"],
            issue_id=parsed_data["issue_number"],
        )
        github_app.mark_under_processing()

        # check if there's an similar issue
        similar_issue_found = github_app.check_similar_issue()

        if similar_issue_found:
            # save the duplicate issues in the db
            duplicates = github_app.save_duplicate_issues(
                similar_issues=similar_issue_found
            )

            if duplicates:
                status = github_app.post_comments(duplicates=duplicates)

            # Log the result
            if status:
                logger.info("Comment added successfully.")
            else:
                logger.warning("Failed to add comment.")

            return
        else:
            logger.info("No similar issues found")

    else:
        logger.info("Ignoring issues as other then opened")
        return
