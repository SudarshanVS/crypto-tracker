import asyncio
from contextlib import asynccontextmanager
from third_party.binance_client import BinanceClient


# Lifespan context manager
@asynccontextmanager
async def lifespan(app):
    binance_client = BinanceClient()
    app.state.binance_client = binance_client

    await binance_client.connect()
    task = asyncio.create_task(binance_client.listen())
    yield
    await binance_client.shutdown()
    task.cancel()
    try:
        await task
    except asyncio.CancelledError:
        pass
