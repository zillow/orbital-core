import os
import time
import json
import asyncio
import pytest
from aiohttp import web
from orbital_core import bootstrap_app, enable_cors

APP_ROOT = os.path.dirname(__file__)


@pytest.fixture
def app(loop):
    app = web.Application()
    bootstrap_app(app, APP_ROOT,
                  service_name="example",
                  service_description="example service")
    enable_cors(app)
    return app


@pytest.fixture
def cli(loop, test_client, app):
    return loop.run_until_complete(test_client(app))


async def test_app_sanity(cli):
    """ sanity check, to see if bootstrap_app works. """
    resp = await cli.get('/')
    assert resp.status == 200

async def test_app_ping(cli):
    """ sanity check, to see if bootstrap_app works. """
    resp = await cli.get('/monitor/ping')
    assert resp.status == 200
