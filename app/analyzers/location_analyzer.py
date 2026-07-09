from app.utils.location_database import LOCATION_DATABASE

class LocationAnalyzer:

    def classify(self, hop):

        host = hop.host.lower()

        for codigo, pais in LOCATION_DATABASE.items():

            if f".{codigo}." in host:
                return pais

            if host.startswith(codigo + "."):
                return pais

            if host.endswith("." + codigo):
                return pais

            if f"-{codigo}-" in host:
                return pais

            if f"_{codigo}_" in host:
                return pais

        return ""