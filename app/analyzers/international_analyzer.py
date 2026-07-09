class InternationalAnalyzer:

    def analyze(self, trace):

        pais_anterior = None

        for hop in trace.hops:

            if not hop.pais:
                continue

            if pais_anterior is None:
                pais_anterior = hop.pais
                continue

            if hop.pais != pais_anterior:

                return {
                    "internacional": True,
                    "hop": hop,
                    "origem": pais_anterior,
                    "destino": hop.pais
                }

        return {
            "internacional": False,
            "hop": None,
            "origem": "",
            "destino": ""
        }