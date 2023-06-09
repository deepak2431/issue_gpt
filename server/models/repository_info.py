from .database import db


class RepositoryInfo(db.Model):
    """
    model to store the repository info
    """

    __tablename__ = "repository_info"

    pk_repository = db.Column(db.Integer, primary_key=True)
    repository_name = db.Column(db.String)
    organisation_name = db.Column(db.String)
    open_issues = db.Column(db.Integer)
    total_issues = db.Column(db.Integer)

    def __init__(self, repository_name, organisation_name, open_issues, total_issues):
        self.repository_name = repository_name
        self.organisation_name = organisation_name
        self.open_issues = open_issues
        self.total_issues = total_issues

    def save_info(self):
        try:
            db.session.add(self)
            db.session.commit()
        except Exception as e:
            db.session.rollback()
            raise

    def get_repository_count(organisation_name):
        """Get the total number of repositories for an organization."""
        try:
            repository_count = RepositoryInfo.query.filter_by(
                organisation_name=organisation_name
            ).count()
            return repository_count
        except Exception as e:
            db.session.rollback()
            raise
