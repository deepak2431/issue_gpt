import os
import json
from dotenv import load_dotenv
import pandas as pd
import requests

from github import Github

load_dotenv()

# Setup logging
import logging

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


class GithubAPI:

    """
    Class GithubAPI:

    Parameters:
    repo_name (str): The name of the GitHub repository in the format "owner/repo_name".

    Functionality:
    - Gets an access token from the environment variable GITHUB_ACCESS_TOKEN.
    - Creates a Github object to access the GitHub API.
    - Gets the repository object from the repo_name.
    - Gets all open issues from the repository.
    - Returns the issues as a Pandas DataFrame.

    Methods:
    get_issues():
    Gets all issues for a given GitHub repository.

    Parameters:
    repo_name (str): The name of the GitHub repository in the format "owner/repo_name".
    file_name (str): The name of the file to write the issues to.

    Functionality:
    - Gets an access token from the environment variable GITHUB_ACCESS_TOKEN.
    - Creates a Github object to access the GitHub API.
    - Gets the repository object from the repo_name.
    - Gets all open issues from the repository.
    - Returns the issues as a Pandas DataFrame.
    """

    def __init__(self, repo_name, owner) -> None:
        self.repo_name = repo_name
        self.owner = owner
        logger.info(f"GithubAPI object initialized for {repo_name}.")

    def get_issues(self):
        logger.info(f"Getting issues for {self.repo_name}...")
        github_access_token = os.getenv("GITHUB_ACCESS_TOKEN")
        g = Github(github_access_token)
        repo = g.get_repo(f"{self.owner}/{self.repo_name}")

        issues = []
        for issue in repo.get_issues(state="open"):
            issues.append(
                {
                    "issue_title": issue.title,
                    "issue_description": issue.body,
                    "issue_number": issue.number,
                }
            )

        df = pd.DataFrame(issues)
        logger.info(f"{len(df)} issues retrieved for {self.repo_name}.")
        return df

    def add_comments(self, issue_number):
        """Add a comment to an issue."""

        comment_url = f"https://api.github.com/repos/{self.owner}/{self.repo_name}/issues/{issue_number}/comments"

        headers = {
            "Authorization": f'Bearer {os.getenv("GITHUB_ACCESS_TOKEN")}',
            "Accept": "application/vnd.github+json",
            "X-GitHub-Api-Version": "2022-11-28",
        }

        comment_data = {"body": "This is a test comment feature"}

        response = requests.post(comment_url, headers=headers, json=comment_data)

        if response.status_code == 201:
            logger.info(f"Comment added to issue #{issue_number}.")
            return 1
        else:
            logger.warning(
                f"Failed to add comment to issue #{issue_number}. Response: {response.text}"
            )
            return 0
