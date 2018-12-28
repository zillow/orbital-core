import aiohttp_cors
from aiohttp import web

def enable_cors(app):
    """
    Globally enable CORS.

    This is an unsafe operation for sensitive services,
    as it allows any website to perform actions on this service
    with the user's credentials.

    This is a quick workaround that might be more acceptible for an
    internal tool.

    This function should be called after all other routes are added.
    """
    # Configure default CORS settings.
    cors = aiohttp_cors.setup(app, defaults={
        "*": aiohttp_cors.ResourceOptions(
                allow_credentials=True,
                expose_headers="*",
                allow_headers="*",
            )
    })

    # Configure CORS on all routes.
    for route in list(app.router.routes()):
        if not isinstance(route.resource, web.StaticResource):
            cors.add(route)
