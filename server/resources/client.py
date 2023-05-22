from flask_restful import Resource, request
from helpers.log_mod import logger

from models.github_keys import GithubKeys
from models.repository_info import RepositoryInfo


class GitKeys(Resource):
    def post(self):
        logger.info("Received GitHub keys info")

        github_keys = request.get_json()
        organisation_name = github_keys["organisation_name"]
        personal_access_token = github_keys["personal_access_token"]
        webhooks_secret = github_keys["webhooks_secret"]

        logger.info("Creating new GithubKeys object")
        new_github_keys = GithubKeys(
            organisation_name=organisation_name,
            personal_access_token=personal_access_token,
            webhooks_secret=webhooks_secret,
        )
        logger.info("Saving GithubKeys info to database")
        try:
            new_github_keys.save_info()
            logger.info("GithubKeys info saved successfully")

            return {"message": "Keys saved successfully"}, 201
        except Exception as e:
            logger.error("Failed to save GithubKeys info", exc_info=1)
            return {"message": "Failed to save the keys"}, 400

    def get(self):
        logger.info("Received request for GitHub keys")
        organisation_name = request.args.get("organisation_name")
        github_keys = GithubKeys.query.filter_by(
            organisation_name=organisation_name
        ).first()
        if github_keys:
            logger.info("Returning GitHub keys")
            return {
                "organisation_name": github_keys.organisation_name,
                "personal_access_token": github_keys.personal_access_token,
                "webhooks_secret": github_keys.webhooks_secret,
            }, 200
        else:
            logger.warning("No keys found for the given organisation name")
            return {"message": "No keys found for the given organisation name"}, 404


class Repository(Resource):
    def post(self):
        logger.info("Received repository info")

        data = request.get_json()
        org_name = data["org_name"]
        repository = data["repository"]

        logger.info("Creating new RepositoryInfo object")
        repository_info = RepositoryInfo(
            repository_name=repository, organisation_name=org_name
        )

        logger.info("Saving repository info to database")
        try:
            repository_info.save_info()
            logger.info("Repository info saved successfully")

            return {"message": "Repository added successfully"}, 201
        except Exception as e:
            logger.error("Failed to save repository info")
            return {"message": "Failed to save the repository"}, 400
