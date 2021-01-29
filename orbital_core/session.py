import logging

from aiohttp import ClientSession
from .utils import tracing

LOG = logging.getLogger(__name__)


async def wrap_request(request_func, *args, **kargs):
    ctx = tracing.get_span_context()
    if ctx:
        kargs['trace_request_ctx'] = {'span_context': ctx}

    return await request_func(*args, **kargs)


class ExtendedClientSession(ClientSession):

    async def get(self, *args, **kargs):
        return await wrap_request(super().get, *args, **kargs)

    async def post(self, *args, **kargs):
        return await wrap_request(super().post, *args, **kargs)

    async def delete(self, *args, **kargs):
        return await wrap_request(super().delete, *args, **kargs)

    async def put(self, *args, **kargs):
        return await wrap_request(super().put, *args, **kargs)

    async def options(self, *args, **kargs):
        return await wrap_request(super().options, *args, **kargs)

    async def patch(self, *args, **kargs):
        return await wrap_request(super().patch, *args, **kargs)

    async def head(self, *args, **kargs):
        return await wrap_request(super().head, *args, **kargs)
