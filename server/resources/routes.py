# init all the routes
from .webhooks import Home, Webhooks
from .client import (GitKeys, Repository, RecentDuplicateIssue, RecentOpenIssue, RecentWeekIssue, Metrics)


def initialize_routes(api):
    api.add_resource(Home, "/")
    api.add_resource(Webhooks, "/webhooks")
    api.add_resource(GitKeys, "/keys")
    api.add_resource(Repository, "/repository")
    api.add_resource(RecentWeekIssue, "/issues/week")
    api.add_resource(RecentDuplicateIssue, "/issues/duplicate")
    api.add_resource(RecentOpenIssue, "/issues/open")
    api.add_resource(Metrics, "/metrics")
