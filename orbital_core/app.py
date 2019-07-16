from .routes import add_routes
from .utils.tracing import configure_tracing, get_trace_config
from .session import ExtendedClientSession


def bootstrap_app(app, root_dir=None,
                  service_name="my service",
                  service_description="this is a service.",
                  tracing_route_blacklist=None,
                  span_properties=None):
    """
    This should be called by every application using Orbital, to eliminate
    boilerplate and provide common functionality.
    """
    app["service_name"] = service_name
    app["service_description"] = service_description
    app["span_properties"] = span_properties
    app.on_startup.append(on_startup)
    add_routes(app, root_dir)

    configure_tracing(app, tracing_route_blacklist or {
        '/monitor/ping',
    })


async def create_http_client(app):
    if "http" not in app:
        app["http"] = ExtendedClientSession(
            trace_configs=[get_trace_config(app)])

        async def close_session(app):
            await app["http"].close()
        app.on_cleanup.append(close_session)


async def on_startup(app):
    await create_http_client(app)
