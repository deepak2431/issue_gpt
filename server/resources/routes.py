# init all the routes
from .webhooks import Home, Webhooks


def initialize_routes(api):
    api.add_resource(Home, "/")
    api.add_resource(Webhooks, "/webhooks")
