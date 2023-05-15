# Add all the resources for the github app
import json
import os
import hmac
import hashlib
from dotenv import load_dotenv
from helpers.log_mod import logger
from helpers.github_helpers import GithubAPI
from helpers.open_ai_helpers import SearchIssue


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


def check_similar_issue(owner, repo, issue_title, issue_body):
    """Check if a similar issue already exists."""

    logger.info(f"Checking for similar issues in {owner}/{repo}...")
    github_api = GithubAPI(repo_name=repo, owner=owner)
    df = github_api.get_issues()

    issue_searcher = SearchIssue(df)
    issue_searcher.generate_embeddings()

    # generate the issue with the combined body, title for embeddings
    issue_combined = (
        "Issue description: "
        + issue_body.strip()
        + "; Issue Title: "
        + issue_title.strip()
    )

    similar_issues = issue_searcher.find_similar_issues(new_issue=issue_combined, n=3)

    if len(similar_issues) > 0:
        logger.info(f"{len(similar_issues)} similar issues found.")
        return True
    else:
        logger.info("No similar issues found.")
        return False


def post_comments(issue_number, owner, repo):
    """Add a comment to a GitHub issue.

    Args:
        issue_number (int): The issue number.
        owner (str): The repository owner.
        repo (str): The repository name.
    Returns:
        int: 1 if successful, 0 otherwise.
    """
    logger.info(f"Adding comment to issue #{issue_number}...")
    github_api = GithubAPI(repo_name=repo, owner=owner)

    status = github_api.add_comments(issue_number=issue_number)

    if status == 1:
        logger.info(f"Comment added to issue #{issue_number}.")
    else:
        logger.warning(f"Failed to add comment to issue #{issue_number}.")

    return status


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
        # Add a comment to the issue

        # check if there's an similar issue
        similar_issue_found = check_similar_issue(
            owner=parsed_data["owner"],
            repo=parsed_data["repo"],
            issue_title=parsed_data["title"],
            issue_body=parsed_data["body"],
        )

        if similar_issue_found:
            status = post_comments(
                issue_number=parsed_data["issue_number"],
                owner=parsed_data["owner"],
                repo=parsed_data["repo"],
            )

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
