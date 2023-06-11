from flask_sqlalchemy import SQLAlchemy
from sqlalchemy.ext.declarative import declarative_base

db = SQLAlchemy()
Base = declarative_base()


def initialize_db(app):
    db.init_app(app)

    with app.app_context():
        from models.issues import Issues
        from models.github_keys import GithubKeys
        from models.repository_info import RepositoryInfo

        try:
            db.create_all()
            db.session.commit()
        except Exception as e:
            db.session.rollback()
            raise
