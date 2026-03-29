import asyncio
import json
import logging

import websockets
from config.settings import STREAMS

from db.local_inmemory_store import store

logger = logging.getLogger(__name__)


class BinanceConnectionError(Exception):
    pass


class BinanceClient:

    def __init__(self):
        self.client = None
        self.active_channels = dict()
        self._shutdown = False
        self._lock = asyncio.Lock()

    async def connect(self):
        retry = 0
        while retry < 4:
            try:
                logger.info("Connecting to Binance WebSocket")
                self.client = await websockets.connect(
                    f"wss://stream.binance.com:9443/stream?streams={STREAMS}"
                )

                logger.info("Connected to Binance WebSocket")
                retry = 0
                return
            except Exception as e:
                logger.error(f"Error while connecting to Binance WebSocket: {e}")
                await asyncio.sleep(2 ** retry)
                retry += 1

        raise BinanceConnectionError("Failed to connect to Binance WebSocket")

    async def shutdown(self):
        self._shutdown = True
        if self.client:
            logger.info("Disconnecting from Binance WebSocket")
            try:
                await self.client.close()
            except Exception as e:
                logger.error(f"Error while closing websocket client: {e}")

        all_clients = []

        async with self._lock:
            for channel, clients in self.active_channels.items():
                all_clients.extend(clients)

            self.active_channels.clear()

        logger.info(f"Disconnecting all clients. Total clients: {len(all_clients)}")
        for client in all_clients:
            try:
                await client.close()
            except Exception as e:
                logger.error(f"Error while closing websocket client: {e}")

        logger.info("Binance client shutdown completed.")

    async def subscribe(self, websocket_client, symbols):
        if isinstance(symbols, str):
            symbols = [symbols]

        async with self._lock:
            for symbol in symbols:
                if symbol not in self.active_channels:
                    self.active_channels[symbol] = set()

                self.active_channels[symbol].add(websocket_client)

    async def unsubscribe(self, websocket_client, symbols):
        if isinstance(symbols, str):
            symbols = [symbols]

        async with self._lock:
            for symbol in symbols:
                try:
                    self.active_channels[symbol].remove(websocket_client)
                except (KeyError, ValueError):
                    pass

    async def broadcast_to_group(self, symbol, data):
        dead_connections = []

        async with self._lock:
            active_clients = list(self.active_channels.get(symbol, []))

        for websocket_client in active_clients:
            try:
                await websocket_client.send_json({"type": "INFO", "data": data})
            except Exception as e:
                logger.error(f"Error while broadcasting to channel {symbol}: {e}")
                try:
                    await websocket_client.close()
                except Exception as e:
                    logger.error(f"Error while closing websocket client: {e}")

                dead_connections.append(websocket_client)

        async with self._lock:
            for websocket_client in dead_connections:
                try:
                    self.active_channels[symbol].remove(websocket_client)
                except (KeyError, ValueError):
                    pass

    async def listen(self):
        if not self.client:
            raise RuntimeError("Cannot call listen() before connect()")

        while not self._shutdown:
            try:
                async for message in self.client:
                    m = json.loads(message)
                    data = {
                        "symbol": m["data"]["s"],
                        "last_price": m["data"]["c"],
                        "percent_change": m["data"]["P"],
                        "timestamp": m["data"]["E"],
                    }

                    await store.save(data["symbol"].lower(), data)
                    await self.broadcast_to_group(data["symbol"].lower(), data)
            except Exception as e:
                logger.error(f"Error while receiving message from Binance Websocket: {e}")
                try:
                    await self.client.close()
                except Exception as e:
                    logger.error(f"Error while closing websocket client: {e}")

                await asyncio.sleep(2)
                if not self._shutdown:
                    await self.connect()
