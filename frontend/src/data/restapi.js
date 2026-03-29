class RestAPIClient {
    async getPrice(cryptoSymbols) { //todo: implement UI, for now rest api can be accessed via postman
        try {
            let response = await fetch(`http://localhost:8000/api/crypto/price?crypto_symbols=${cryptoSymbols}`)

            let responseJson = await response.json()

            return responseJson.data

        } catch (e) {
            console.error(e)
            return {} // todo: show error popup
        }

    }
}

