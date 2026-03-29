import logging
from fastapi import WebSocket, Request, WebSocketDisconnect

from db.local_inmemory_store import store
from config.app import app

logger = logging.getLogger(__name__)


@app.get("/api/health")
async def health_check():
    return {"status": "healthy", "message": "System is up and running, ready to receive requests."}


@app.websocket("/ws/crypto/track")
async def track(websocket: WebSocket):
    crypto_symbols = []
    try:
        await websocket.accept()
        while True:
            message = await websocket.receive_json()
            if message.get("type") == "SUBSCRIBE":
                crypto_symbols = message["data"]["crypto_symbols"]
                await websocket.app.state.binance_client.subscribe(websocket, crypto_symbols)
                await websocket.send_json({"type": "SUBSCRIBE_ACK", "data": {"crypto_symbols": crypto_symbols}})

            else:
                await websocket.send_json({"type": "ERROR", "data": {"message": "Unknown message type"}})

    except WebSocketDisconnect:
        logger.info(f"Unsubscribing disconnected client from crypto symbols: {crypto_symbols}")
        await websocket.app.state.binance_client.unsubscribe(websocket, crypto_symbols)

    except Exception as e:
        logger.error(f"Error while sending subscription acknowledgement to client: {e}")
        await websocket.app.state.binance_client.unsubscribe(websocket, crypto_symbols)

    finally:
        try:
            await websocket.close()
        except Exception:
            pass


@app.get("/api/crypto/price")
async def price(crypto_symbols: str):
    data = []

    try:
        if crypto_symbols:
            crypto_symbols.lower().split(",")

        else:
            crypto_symbols = None

    except Exception:
        crypto_symbols = None

    if isinstance(crypto_symbols, str):
        crypto_symbols = [crypto_symbols]

    if isinstance(crypto_symbols, list):
        for symbol in crypto_symbols:
            d = await store.get(symbol)
            if d:
                data.append(d)
    else:
        d = await store.get_all()
        data = list(d.values())

    return {"status": "success", "data": data}
