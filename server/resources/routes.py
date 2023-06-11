# init all the routes
from .webhooks import Home, Webhooks
from .client import GitKeys, Repository, IssueInfo, Metrics


def initialize_routes(api):
    api.add_resource(Home, "/")
    api.add_resource(Webhooks, "/webhooks")
    api.add_resource(GitKeys, "/github_keys")
    api.add_resource(Repository, "/repository")
    api.add_resource(IssueInfo, "/issues")
    api.add_resource(Metrics, "/metrics")
