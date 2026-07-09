class LatencyAnalyzer:

    def analyze(self, trace):

        maior_delta = 0.0
        hop_maior_delta = None

        for indice, hop in enumerate(trace.hops):

            #
            # Ignora hops classificados como ICMP Filtrado
            #

            if hop.icmp_filtrado:
                continue

            #
            # Ignora o hop imediatamente após um ICMP Filtrado,
            # pois o RTT costuma ficar artificialmente distorcido.
            #

            if indice > 0:

                if trace.hops[indice - 1].icmp_filtrado:
                    continue

            #
            # Ignora o destino.
            #

            if indice == len(trace.hops) - 1:
                continue

            if hop.delta_rtt > maior_delta:

                maior_delta = hop.delta_rtt
                hop_maior_delta = hop

        return {

            "maior_delta": round(maior_delta, 2),

            "hop": hop_maior_delta

        }