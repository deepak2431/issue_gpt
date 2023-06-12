from .database import db
from datetime import datetime, timedelta


class Issues(db.Model):
    """
    model to store the  issue info
    """

    __tablename__ = "issues"

    pk_duplicate_issues = db.Column(db.Integer, primary_key=True)
    organisation_name = db.Column(db.String)  # TODO: Associate using foreign key
    repository_name = db.Column(db.String)
    created_issue_id = db.Column(db.String)
    duplicate_issue_id = db.Column(db.String)
    comment_added = db.Column(db.Boolean)
    issue_processed = db.Column(db.Boolean)
    received_dt_utc = db.Column(db.DateTime)

    def __init__(
        self,
        repository_name,
        organisation_name,
        created_issue_id,
        duplicate_issue_id,
        comment_added,
        issue_processed,
        received_dt_utc,
    ):
        self.repository_name = repository_name
        self.organisation_name = organisation_name
        self.created_issue_id = created_issue_id
        self.duplicate_issue_id = duplicate_issue_id
        self.comment_added = comment_added
        self.issue_processed = issue_processed
        self.received_dt_utc = received_dt_utc

    def save_info(self):
        try:
            db.session.add(self)
            db.session.commit()
        except Exception as e:
            db.session.rollback()
            raise

    def update_duplicate_issue(created_issue_id, duplicate_issue_id):
        """
        Updates the given duplicate_issue_id for the repository_name
        """
        try:
            issue = Issues.query.filter_by(created_issue_id=created_issue_id).first()
            issue.duplicate_issue_id = duplicate_issue_id
            db.session.commit()
        except Exception as e:
            db.session.rollback()
            raise

    def update_processing_status(created_issue_id):
        """
        Updates the given duplicate_issue_id for the repository_name
        """
        try:
            issue = Issues.query.filter_by(created_issue_id=created_issue_id).first()
            issue.issue_processed = True
            issue.comment_added = True
            db.session.commit()
        except Exception as e:
            db.session.rollback()
            raise

    def check_issue_exists(created_issue_id):
        """
        Check if the issues already exists/being processed
        """
        try:
            issue = Issues.query.filter_by(created_issue_id=created_issue_id).first()
            if issue is not None:
                return True
            return False
        except Exception as e:
            db.session.rollback()
            raise

    def check_org_exists(organisation_name):
        """
        check if the org exists
        """

        org = Issues.query.filter(Issues.organisation_name == organisation_name)
        if org is not None:
            return True
        return False

    def get_duplicate_issues(organisation_name):
        """
        Get all duplicate issues for the given organisation name.
        """
        try:
            duplicate_issues = Issues.query.filter(
                Issues.organisation_name == organisation_name,
                Issues.issue_processed == True,
                Issues.duplicate_issue_id != None,
            ).all()

            return [
                {
                    "organisation_name": issue.organisation_name,
                    "repository_name": issue.repository_name,
                    "created_issue_id": issue.created_issue_id,
                    "duplicate_issue_id": issue.duplicate_issue_id,
                }
                for issue in duplicate_issues
            ]
        except Exception as e:
            db.session.rollback()
            raise

    def get_tracked_issues(organisation_name):
        """
        get the total tracked issues
        """

        # find count of all issues
        tracked_issues = Issues.query.filter(
            Issues.organisation_name == organisation_name
        ).count()
        return tracked_issues

    def get_recent_duplicate(organisation_name):
        """
        Get the recent duplicate issues in the last 24 hours.
        """
        try:
            yesterday = datetime.now() - timedelta(days=1)
            recent_duplicates = (
                Issues.query.filter(
                    Issues.organisation_name == organisation_name,
                    Issues.issue_processed == True,
                    Issues.duplicate_issue_id != None,
                    Issues.received_dt_utc > yesterday,
                )
                .limit(7)
                .all()
            )
            return [
                {
                    "organisation_name": issue.organisation_name,
                    "repository_name": issue.repository_name,
                    "created_issue_id": issue.created_issue_id,
                    "duplicate_issue_id": issue.duplicate_issue_id,
                }
                for issue in recent_duplicates
            ]
        except Exception as e:
            db.session.rollback()
            raise

    def get_recent_issues(organisation_name):
        """Get the recent issues added in the last 24 hours."""
        try:
            yesterday = datetime.now() - timedelta(days=1)
            recent_issues = (
                Issues.query.filter(
                    Issues.organisation_name == organisation_name,
                    Issues.received_dt_utc > yesterday,
                )
                .limit(7)
                .all()
            )
            return [
                {
                    "organisation_name": issue.organisation_name,
                    "repository_name": issue.repository_name,
                    "created_issue_id": issue.created_issue_id,
                }
                for issue in recent_issues
            ]
        except Exception as e:
            db.session.rollback()
            raise
