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
        created_issue_id,
        duplicate_issue_id,
        comment_added,
        issue_processed,
        received_dt_utc,
    ):
        self.repository_name = repository_name
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

    def get_duplicate_issues(organisation_name):
        """
        Get all duplicate issues for the given organisation name.
        """
        try:
            duplicate_issues = Issues.query.filter_by(
                organisation_name=organisation_name
            ).all()
            return [
                {
                    "organisation_name": issue.organisation_name,
                    "repository_name": issue.repository_name,
                    "created_issue_id": issue.created_issue_id,
                    "duplicate_issue_id": issue.duplicate_issue_id,
                    "received_dt_utc": issue.received_dt_utc,
                }
                for issue in duplicate_issues
            ]
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
