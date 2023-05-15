from .database import db


class DuplicateIssues(db.Model):
    """
    model to store the duplicate issue info
    """

    __tablename__ = "duplicate_issues"

    pk_duplicate_issues = db.Column(db.Integer, primary_key=True)
    repository_name = db.Column(db.String)
    created_issue_id = db.Column(db.String)
    duplicate_issue_id = db.Column(db.String)

    received_dt_utc = db.Column(db.DateTime)

    def __init__(
        self, repository_name, created_issue_id, duplicate_issue_id, received_dt_utc
    ):
        self.repository_name = repository_name
        self.created_issue_id = created_issue_id
        self.duplicate_issue_id = duplicate_issue_id
        self.received_dt_utc = received_dt_utc

    def save_info(self):
        try:
            db.session.add(self)
            db.session.commit()
        except Exception as e:
            db.session.rollback()
            raise
