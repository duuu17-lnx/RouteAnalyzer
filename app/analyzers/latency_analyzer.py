class LatencyAnalyzer:

    def analyze(self, trace):

        maior_delta = None
        hop_maior_delta = None

        for indice, hop in enumerate(trace.hops):

            #
            # Ignora o primeiro hop (gateway)
            #

            if indice == 0:
                continue

            #
            # Ignora o destino
            #

            if indice == len(trace.hops) - 1:
                continue

            #
            # Ignora hops sem resposta
            #

            if hop.host is None:
                continue

            #
            # Ignora RTT inválido
            #

            if hop.avg <= 0:
                continue

            if maior_delta is None or hop.delta_rtt > maior_delta:

                maior_delta = hop.delta_rtt
                hop_maior_delta = hop

        return {

            "maior_delta": round(maior_delta or 0.0, 2),

            "hop": hop_maior_delta

        }