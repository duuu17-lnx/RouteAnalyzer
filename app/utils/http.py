import requests


class HTTPClient:

    DEFAULT_TIMEOUT = 5

    DEFAULT_HEADERS = {
        "User-Agent": "RouteAnalyzer/1.0"
    }

    def get(self, url, params=None):

        resposta = requests.get(
            url,
            params=params,
            headers=self.DEFAULT_HEADERS,
            timeout=self.DEFAULT_TIMEOUT
        )

        resposta.raise_for_status()

        return resposta.json()