import os
import json
from dotenv import load_dotenv
import pandas as pd

import openai
from github import Github

load_dotenv()


def get_issues(repo_name):
    """
    Gets all issues for a given GitHub repository and writes them to a file.

    Parameters:
    repo_name (str): The name of the GitHub repository in the format "owner/repo_name".
    file_name (str): The name of the file to write the issues to.

    Functionality:
    - Gets an access token from the environment variable GITHUB_ACCESS_TOKEN.
    - Creates a Github object to access the GitHub API.
    - Gets the repository object from the repo_name.
    - Gets all open issues from the repository.
    - Writes the issue titles and descriptions to the file_name.
    """

    github_access_token = os.getenv("GITHUB_ACCESS_TOKEN")
    g = Github(github_access_token)
    repo = g.get_repo(repo_name)

    issues = []
    for issue in repo.get_issues(state="all"):
        issues.append({"issue_title": issue.title, "issue_description": issue.body})

    return pd.DataFrame(issues)
