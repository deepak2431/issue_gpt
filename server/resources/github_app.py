from dotenv import load_dotenv
from datetime import datetime

from helpers.log_mod import logger
from helpers.github_helpers import GithubAPI
from helpers.open_ai_helpers import SearchIssue
from models.duplicate_issues import DuplicateIssues


load_dotenv()


class GithubApp:
    __issue_df = None

    def __init__(self, owner, repo, issue_title, issue_body) -> None:
        self.owner = owner
        self.repo = repo
        self.issue_title = issue_title
        self.issue_body = issue_body

    def check_similar_issue(self):
        """Check if a similar issue already exists."""

        logger.info(f"Checking for similar issues in {self.owner}/{self.repo}...")
        github_api = GithubAPI(repo_name=self.repo, owner=self.owner)
        df = github_api.get_issues()

        self.__issue_df = df

        issue_searcher = SearchIssue(df)
        issue_searcher.generate_embeddings()

        # generate the issue with the combined body, title for embeddings
        issue_combined = (
            "Issue description: "
            + self.issue_body.strip()
            + "; Issue Title: "
            + self.issue_title.strip()
        )

        similar_issues = issue_searcher.find_similar_issues(
            new_issue=issue_combined, n=3
        )

        if len(similar_issues) > 0:
            logger.info(f"{len(similar_issues)} similar issues found.")
            return True
        else:
            logger.info("No similar issues found.")
            return False

    def post_comments(self):
        """Add a comment to a GitHub issue.

        Args:
            issue_number (int): The issue number.
            owner (str): The repository owner.
            repo (str): The repository name.
        Returns:
            int: 1 if successful, 0 otherwise.
        """
        logger.info(f"Adding comment to issue #{self.issue_number}...")
        github_api = GithubAPI(repo_name=self.repo, owner=self.owner)

        status = github_api.add_comments(issue_number=self.issue_number)

        if status == 1:
            logger.info(f"Comment added to issue #{self.issue_number}.")
        else:
            logger.warning(f"Failed to add comment to issue #{self.issue_number}.")

        return status

    def save_duplicate_issues(self, similar_issues):
        """
        get the issue number and save the duplicates
        """
        github_api = GithubAPI(repo_name=self.repo, owner=self.owner)
        for i in range(similar_issues):
            duplicate_issue_id = github_api.get_issue_number(
                issue_title=similar_issues[i]["issue_title"], df_issue=self.__issue_df
            )

            duplicate = DuplicateIssues(
                repository_name=self.repo,
                created_issue_id=self.issue_number,
                duplicate_issue_id=duplicate_issue_id,
                received_dt_utc=datetime.now(),
            )
            duplicate.save_info()
