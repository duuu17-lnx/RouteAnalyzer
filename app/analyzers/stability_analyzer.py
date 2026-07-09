class StabilityAnalyzer:

    def analyze(self, trace):

        pior_hop = None
        pior_score = -1

        for indice, hop in enumerate(trace.hops):

            #
            # Ignora hops classificados como ICMP filtrado
            #

            if hop.icmp_filtrado:
                continue

            #
            # Ignora o hop imediatamente após um ICMP filtrado.
            # O RTT costuma ficar distorcido.
            #

            if indice > 0:

                if trace.hops[indice - 1].icmp_filtrado:
                    continue

            #
            # Ignora o destino.
            #

            if indice == len(trace.hops) - 1:
                continue

            variacao = hop.worst - hop.best

            score = variacao + hop.stdev

            if score > pior_score:

                pior_score = score
                pior_hop = hop

        #
        # Nenhum hop válido para análise
        #

        if pior_hop is None:

            return {

                "hop": None,

                "score": 0,

                "variacao": 0,

                "status": "Estável"

            }

        #
        # Classificação
        #

        if pior_score < 3:

            status = "Excelente"

        elif pior_score < 10:

            status = "Boa"

        elif pior_score < 25:

            status = "Instável"

        else:

            status = "Muito Instável"

        return {

            "hop": pior_hop,

            "score": round(pior_score, 2),

            "variacao": round(
                pior_hop.worst - pior_hop.best,
                2
            ),

            "status": status

        }