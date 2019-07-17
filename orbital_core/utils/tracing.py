import sys
import aiotask_context
import aiozipkin
import logging
from traceback import format_exception
from typing import Set, Dict
from aiohttp.web import HTTPException, Application, HTTPInternalServerError, Request
from aiozipkin import APP_AIOZIPKIN_KEY, REQUEST_AIOZIPKIN_KEY
from aiozipkin.constants import HTTP_STATUS_CODE, HTTP_ROUTE
from aiozipkin.helpers import make_context, parse_sampled, parse_debug
from aiozipkin.record import Record
from aiozipkin.span import SpanAbc
from aiozipkin.tracer import Tracer
from aiozipkin.transport import Transport

LOG = logging.getLogger(__name__)


class TracingTransport(Transport):

    def __init__(self, *args, **kargs):
        pass

    def send(self, record: Record) -> None:
        extra = {
            "span": self._record_to_key(record),
            "topic_prefix": "tra",
            "log_format": "span-g",
        }
        LOG.info("", extra=extra)

    async def close(self) -> None:
        pass

    def _record_to_key(self, record: Record):
        data = record.asdict()
        return {
            "xti": data["traceId"],
            "xsi": data["id"],
            "xpi": data["parentId"],
            "xsb": '1' if record._context.sampled else '0',  # Sampled
            "xfl": data["debug"], # Flags
            "spn": data["tags"].get(HTTP_ROUTE, data["name"].split(" ")[1]),
            "spt": data["tags"],
            "tsu": data["timestamp"], # Start Timestamp
            "lat": data["duration"], # Latency of trace
            "spk": data["kind"],
        }


def configure_tracing(app: Application, route_blacklist: Set[str]):
    # aio-context is how tracing context is pinned per co-routine, so it must be set.
    # app.loop is not accessible before startup. Setting it as a
    # startup task ensures that it will exist before a call occurs.
    app.on_startup.append(_add_context_task_factory)
    sampler = aiozipkin.Sampler(sample_rate=1.0)
    transport = TracingTransport()
    endpoint = aiozipkin.create_endpoint(app["service_name"])
    tracer = aiozipkin.Tracer(transport, sampler, endpoint)
    return _setup(app, tracer, route_blacklist)


async def _add_context_task_factory(app: Application):
    """
    add the aiotask context task factory, ensuring
    that new tasks will be able to carry context.
    """
    app.loop.set_task_factory(aiotask_context.task_factory)


def get_tracer(app: Application):
    return aiozipkin.get_tracer(app)


def get_trace_config(app: Application):
    return aiozipkin.make_trace_config(get_tracer(app))


def get_span_context():
    try:
        # faster to try catch in most cases then test for current task
        # and the existence of the event loop. If an exception happens here,
        # it shouldn't block and is horribly malformed so it's best to pass.
        return aiotask_context.get(REQUEST_AIOZIPKIN_KEY)
    except:
        return None


def _set_span_properties(span, span_properties: Dict[str, str]):
    for key, value in span_properties.items():
        span.tag(key, value)


def _get_span(request: Request, tracer: Tracer, sample: bool=True) -> SpanAbc:
    context = make_context(request.headers)

    if context is None:
        sampled = sample and parse_sampled(request.headers)
        debug = parse_debug(request.headers)
        return tracer.new_trace(sampled=sampled, debug=debug)

    return tracer.join_span(context)


def _get_middleware(route_blacklist: Set[str]):
    async def middleware_factory(app, handler):
        async def aiozipkin_middleware(request):
            tracer = request.app[APP_AIOZIPKIN_KEY]

            span = _get_span(request, tracer,
                             request.path not in route_blacklist)
            aiotask_context.set(REQUEST_AIOZIPKIN_KEY, span.context)

            with span:
                aiozipkin.aiohttp_helpers._set_span_properties(span, request)
                _set_span_properties(span, app["span_properties"], request)
                try:
                    resp = await handler(request)
                except HTTPException as e:
                    span.tag(HTTP_STATUS_CODE, e.status)
                    e.headers.update(span.context.make_headers())
                    raise
                except Exception:
                    err = HTTPInternalServerError(reason=format_exception(*sys.exc_info()))

                    span.tag(HTTP_STATUS_CODE, 500)
                    err.headers.update(span.context.make_headers())
                    raise err

                resp.headers.update(span.context.make_headers())
                span.tag(HTTP_STATUS_CODE, resp.status)
            return resp

        return aiozipkin_middleware

    return middleware_factory


def _setup(app: Application, tracer: Tracer, route_blacklist: Set[str]) -> Application:
    app[APP_AIOZIPKIN_KEY] = tracer
    app.middlewares.append(_get_middleware(route_blacklist))

    async def close_aiozipkin(app):
        await app[APP_AIOZIPKIN_KEY].close()

    app.on_cleanup.append(close_aiozipkin)
    return app
