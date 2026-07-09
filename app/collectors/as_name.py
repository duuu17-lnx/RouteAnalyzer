import requests


class ASNameCollector:

    BASE_URL = "https://stat.ripe.net/data/as-overview/data.json"

    def lookup(self, asn: int):

        try:

            resposta = requests.get(
                self.BASE_URL,
                params={"resource": f"AS{asn}"},
                timeout=5
            )

            resposta.raise_for_status()

            dados = resposta.json()["data"]

            return dados.get("holder", "")

        except Exception:

            return ""