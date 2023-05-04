import os
import json
from dotenv import load_dotenv
import pandas as pd

import openai
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

    def __init__(self, repo_name) -> None:
        self.repo_name = repo_name
        logger.info(f"GithubAPI object initialized for {repo_name}.")

    def get_issues(self):
        logger.info(f"Getting issues for {self.repo_name}...")
        github_access_token = os.getenv("GITHUB_ACCESS_TOKEN")
        g = Github(github_access_token)
        repo = g.get_repo(self.repo_name)

        issues = []
        for issue in repo.get_issues(state="open"):
            issues.append({"issue_title": issue.title, "issue_description": issue.body})

        df = pd.DataFrame(issues)
        logger.info(f"{len(df)} issues retrieved for {self.repo_name}.")
        return df
