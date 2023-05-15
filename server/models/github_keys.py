from .database import db


class GithubKeys(db.Model):
    """
    model to store the github keys info
    """

    __tablename__ = "github_keys"

    pk_github_keys = db.Column(db.Integer, primary_key=True)
    organisation_name = db.Column(db.String)
    personal_access_token = db.Column(db.String)
    webhooks_secret = db.Column(db.String)

    def __init__(self, organisation_name, personal_access_token, webhooks_secret):
        self.organisation_name = organisation_name
        self.personal_access_token = personal_access_token
        self.webhooks_secret = webhooks_secret

    def save_info(self):
        try:
            db.session.add(self)
            db.session.commit()
        except Exception as e:
            db.session.rollback()
            raise
