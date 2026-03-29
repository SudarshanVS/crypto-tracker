from __future__ import annotations

import asyncio
from collections import OrderedDict

MAX_SIZE = 1000

# todo: add redis support for horizontal scaling
class InMemoryStore:
    def __init__(self, max_size: int = MAX_SIZE):
        self._store: OrderedDict = OrderedDict()
        self._lock = asyncio.Lock()
        self._max_size = max_size

    async def save(self, symbol: str, data: dict):
        async with self._lock:
            self._store[symbol] = data
            if len(self._store) > self._max_size:
                self._store.popitem(last=False)  # evict oldest

    async def get(self, symbol: str) -> dict | None:
        async with self._lock:
            return self._store.get(symbol)

    async def get_all(self) -> dict:
        async with self._lock:
            return dict(self._store)


store = InMemoryStore()