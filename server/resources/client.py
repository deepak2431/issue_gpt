from flask_restful import Resource, request
from flask import jsonify, make_response

from models.github_keys import GithubKeys
from models.repository_info import RepositoryInfo
from models.issues import Issues

from helpers.log_mod import logger


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
            repository_name=repository,
            organisation_name=org_name,
            open_issues="0",
            total_issues="0",
        )

        logger.info("Saving repository info to database")
        try:
            repository_info.save_info()
            logger.info("Repository info saved successfully")

            return {"message": "Repository added successfully"}, 201
        except Exception as e:
            logger.error("Failed to save repository info")
            return {"message": "Failed to save the repository"}, 500


class IssueInfo(Resource):
    def get(self):
        logger.info("Received request to get all duplicate issues")

        org_name = request.args.get("org_name")

        recent = request.args.get("recent")

        if not Issues.check_org_exists(organisation_name=org_name):
            return {"message": "No data found"}, 404

        if recent and org_name:
            if recent == "recent_duplicate":
                logger.info(f"Getting recent duplicate issues for {org_name}")

                duplicate_issues = Issues.get_recent_duplicate(
                    organisation_name=org_name
                )
                return make_response(jsonify({"issues": duplicate_issues}), 200)
            elif recent == "recent_open":
                logger.info(f"Getting recent created issues for {org_name}")
                duplicate_issues = Issues.get_recent_issues(organisation_name=org_name)
                return make_response(jsonify({"issues": duplicate_issues}), 200)
            elif recent == "recent_week":
                logger.info(f"Getting recent week issues for {org_name}")
                duplicate_issues = Issues.get_weeks_issues(organisation_name=org_name)
                return make_response(jsonify({"issues": duplicate_issues}), 200)

        logger.info(f"Getting duplicate issues for {org_name}")
        duplicate_issues = Issues.get_duplicate_issues(organisation_name=org_name)

        logger.info(f"{len(duplicate_issues)} duplicate issues found for {org_name}")
        return make_response(jsonify({"issues": duplicate_issues}), 200)


class Metrics(Resource):
    # update this route
    def get(self):
        logger.info("Received request for issue metrics")

        org_name = request.args.get("org_name")

        logger.info(f"Getting metrics for {org_name}")

        if not Issues.check_org_exists(organisation_name=org_name):
            return {"message": "No data found"}, 404

        metrics = {}

        repo_count = RepositoryInfo.get_repository_count(organisation_name=org_name)
        metrics["repository_count"] = repo_count

        tracked_issues = Issues.get_tracked_issues(organisation_name=org_name)
        metrics["tracked_issues"] = tracked_issues

        duplicate_issues = Issues.get_duplicate_issues(organisation_name=org_name)
        metrics["duplicate_issues"] = len(duplicate_issues)

        logger.info(f"{len(metrics)} metrics retrieved for {org_name}")
        logger.info(metrics)
        return make_response(jsonify({"metrics": metrics}), 200)
