import asyncio


class PeriodicTask():
    def __init__(self, func, interval, loop=None):
        self.func = func
        self.interval = interval
        self._loop = loop or asyncio.get_event_loop()
        self._set()

    def _set(self):
        self._handler = self._loop.call_later(self.interval, self._run)

    def _run(self):
        try:
            self.func()
        finally:
            self._set()

    def stop(self):
        self._handler.cancel()
