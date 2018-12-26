from .routes import add_routes
from aiohttp import ClientSession

def bootstrap_app(app, root_dir=None,
                  service_name="my service",
                  service_description="this is a service."):
    """
    This should be called by every application using Orbital, to eliminate
    boilerplate and provide common functionality.
    """
    app["service_name"] = service_name
    app["service_description"] = service_description
    _add_client_session(app)
    add_routes(app, root_dir)

def _add_client_session(app):
    """ add a client session object """
    app["http"] = ClientSession()
    async def close_session(app):
        await app["http"].close()
    app.on_cleanup.append(close_session)


async def on_startup(app):
    pass
