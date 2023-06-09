from .database import db


class IssueMetrics(db.Model):
    """
    model to store the issue metrics info
    """

    __tablename__ = "issue_metrics"

    pk_issue_metrics = db.Column(db.Integer, primary_key=True)
    organisation_name = db.Column(db.String)  # TODO: Associate using foreign key
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

    def get_metrics(organisation_name):
        try:
            issue_metrics = IssueMetrics.query.filter_by(
                organisation_name=organisation_name
            ).all()
            return [
                {
                    "organisation_name": metric.organisation_name,
                    "repository_name": metric.repository_name,
                    "open_issues": metric.open_issues,
                    "total_issues": metric.total_issues,
                    "duplicate_issues": metric.duplicate_issues,
                }
                for metric in issue_metrics
            ]
        except Exception as e:
            db.session.rollback()
            raise
