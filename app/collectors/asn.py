import ipaddress

from app.utils.http import HTTPClient


class ASNCollector:

    NETWORK_INFO_URL = "https://stat.ripe.net/data/network-info/data.json"
    AS_OVERVIEW_URL = "https://stat.ripe.net/data/as-overview/data.json"

    _cache = {}

    def __init__(self):

        self.http = HTTPClient()

    def lookup(self, ip: str):

        #
        # IP inválido
        #

        if not ip:

            return None

        try:

            ipaddress.ip_address(ip)

        except ValueError:

            return None

        #
        # Cache
        #

        if ip in ASNCollector._cache:

            return ASNCollector._cache[ip]

        try:

            network = self.http.get(

                self.NETWORK_INFO_URL,

                params={

                    "resource": ip

                }

            )

            network_data = network.get("data", {})

            asns = network_data.get("asns", [])

            if not asns:

                ASNCollector._cache[ip] = None

                return None

            asn = asns[0]

            overview = self.http.get(

                self.AS_OVERVIEW_URL,

                params={

                    "resource": f"AS{asn}"

                }

            )

            overview_data = overview.get("data", {})

            resultado = {

                "asn": str(asn),

                "description": overview_data.get("holder", ""),

                "country": overview_data.get("country", ""),

                "prefix": network_data.get("prefix", "")

            }

            ASNCollector._cache[ip] = resultado

            return resultado

        except Exception:

            #
            # Não exibe erro para o usuário.
            # Apenas considera ASN desconhecido.
            #

            ASNCollector._cache[ip] = None

            return None

    @classmethod
    def clear_cache(cls):

        cls._cache.clear()

    @classmethod
    def cache_size(cls):

        return len(cls._cache)