from aiohttp import web
from aiohttp_transmute import add_route
from .templates import get_template
from .docs import add_docs


async def ping(request):
    status = 200
    if request.app[SHUTDOWN_KEY]:
        status = 400
    return web.json_response({
        "will_shutdown": request.app[SHUTDOWN_KEY]
    }, status=status)


async def index(request):
    body = get_template("index.html").render({
        "service_name": request.app["service_name"],
        "service_description": request.app["service_description"]
    }).encode("UTF-8")
    return web.Response(body=body, content_type="text/html")


def add_routes(app, root_dir):
    app.router.add_get("/", index)
    app.router.add_get("/monitor/ping", ping)
    add_docs(app, root_dir)
