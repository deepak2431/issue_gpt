from .database import db


class RepositoryInfo(db.Model):
    """
    model to store the repository info
    """

    __tablename__ = "repository_info"

    pk_repository = db.Column(db.Integer, primary_key=True)
    repository_name = db.Column(db.String)
    organisation_name = db.Column(db.String)

    def __init__(self, repository_name, organisation_name):
        self.repository_name = repository_name
        self.organisation_name = organisation_name

    def save_info(self):
        try:
            db.session.add(self)
            db.session.commit()
        except Exception as e:
            db.session.rollback()
            raise
