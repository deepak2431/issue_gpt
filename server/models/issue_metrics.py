from .database import db


class IssueMetrics(db.Model):
    """
    model to store the issue metrics info
    """

    __tablename__ = "issue_metrics"

    pk_issue_metrics = db.Column(db.Integer, primary_key=True)
    organisation_name = db.Column(db.String)  #TODO: Associate using foreign key
    repository_name = db.Column(db.String)
    open_issues = db.Column(db.Integer)
    total_issues = db.Column(db.Integer)
    duplicate_issues = db.Column(db.Integer)

    def __init__(self, repository_name, open_issues, total_issues, duplicate_issues):
        self.repository_name = repository_name
        self.open_issues = open_issues
        self.total_issues = total_issues
        self.duplicate_issues = duplicate_issues

    def save_info(self):
        try:
            db.session.add(self)
            db.session.commit()
        except Exception as e:
            db.session.rollback()
            raise
