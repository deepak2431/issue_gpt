# init all the routes
from .webhooks import Home, Webhooks
from .client import GitKeys, Repository


def initialize_routes(api):
    api.add_resource(Home, "/")
    api.add_resource(Webhooks, "/webhooks")
    api.add_resource(GitKeys, "/github_keys")
    api.add_resource(Repository, "/repository")
