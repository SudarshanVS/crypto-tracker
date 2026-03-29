class WebSocketClient {
    constructor(url) {
        this.url = url;
        this.socket = new WebSocket(url);
        console.log("WebSocketClient created");
    }

    async subscribe(cryptoSymbols) {
        if (this.socket.readyState === WebSocket.OPEN) {
            try {
                await this.socket.send(JSON.stringify({type: "SUBSCRIBE", data: {crypto_symbols: cryptoSymbols}}))
            } catch (e) {
                console.error(e)
            }

        }
    }
}

export default WebSocketClient;