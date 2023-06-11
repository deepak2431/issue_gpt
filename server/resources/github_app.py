from dotenv import load_dotenv
from datetime import datetime

from helpers.github_helpers import GithubAPI
from helpers.open_ai_helpers import SearchIssue
from models.issues import Issues

import logging

# Setup logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


load_dotenv()


class GithubApp:
    __issue_df = None

    def __init__(self, owner, repo, issue_title, issue_body, issue_id) -> None:
        self.owner = owner
        self.repo = repo
        self.issue_title = issue_title
        self.issue_body = issue_body
        self.issue_id = issue_id

    def mark_under_processing(self):
        """Marks the issue under processing status"""

        from app import create_app

        app = create_app()

        with app.app_context():
            issue = Issues(
                repository_name=self.repo,
                created_issue_id=self.issue_id,
                duplicate_issue_id=None,
                comment_added=False,
                issue_processed=False,
                received_dt_utc=datetime.now(),
            )
            issue.save_info()
            return

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
            return similar_issues
        else:
            logger.info("No similar issues found.")
            return None

    def post_comments(self, duplicates):
        """Add a comment to a GitHub issue.

        Args:
            issue_number (int): The issue number.
            owner (str): The repository owner.
            repo (str): The repository name.
        Returns:
            int: 1 if successful, 0 otherwise.
        """
        logger.info(f"Adding comment to issue #{self.issue_id}...")
        github_api = GithubAPI(repo_name=self.repo, owner=self.owner)

        comment = ", ".join([f"#{num}" for num in duplicates])

        status = github_api.add_comments(
            issue_number=self.issue_id, comment=f"Found duplicates with ${comment}"
        )

        if status == 1:
            logger.info(f"Comment added to issue #{self.issue_id}.")
        else:
            logger.warning(f"Failed to add comment to issue #{self.issue_id}.")

        return status

    def save_duplicate_issues(self, similar_issues):
        """
        get the issue number and save the duplicates
        """

        from app import create_app

        duplicated_issues = []
        github_api = GithubAPI(repo_name=self.repo, owner=self.owner)
        for issue in similar_issues:
            duplicate_issue_id = github_api.get_issue_number(
                issue_title=issue["issues_title"], df_issue=self.__issue_df, n=2
            )
            logger.info(duplicate_issue_id)
            logger.info(type(duplicate_issue_id))

            duplicated_issues.append(str(duplicate_issue_id))

            app = create_app()
            with app.app_context():
                Issues.update_duplicate_issue(
                    created_issue_id=self.issue_id,
                    duplicate_issue_id=str(duplicate_issue_id),
                )

        return duplicated_issues
