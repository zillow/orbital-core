import aiohttp
import os


async def redirect_to_index(request):
    """ redirect to index.html """
    return aiohttp.web.HTTPFound('/docs/index.html')


def add_docs(app, app_root):
    doc_root = os.path.join(app_root, "docs")
    app.router.add_route('GET', '/docs', redirect_to_index)
    app.router.add_route('GET', '/docs/', redirect_to_index)
    app.router.add_static('/docs', doc_root)
