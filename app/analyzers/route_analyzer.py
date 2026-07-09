class RouteAnalyzer:

    def analyze(self, trace):

        resultado = {
            "backbone": None,
            "saida_provedor": None,
            "transito": None,
            "ix": None,
            "rede_destino": None
        }

        primeiro_asn = None

        #
        # Primeiro ASN da rota
        #

        for hop in trace.hops:

            if hop.asn:
                primeiro_asn = hop.asn
                resultado["backbone"] = hop
                break

        #
        # Percorre todos os hops
        #

        for hop in trace.hops:

            #
            # IX.br
            #

            if hop.evento == "IX.br" and resultado["ix"] is None:

                resultado["ix"] = hop

            #
            # Trânsito
            #

            if hop.evento == "Trânsito" and resultado["transito"] is None:

                resultado["transito"] = hop

            #
            # Primeira saída do provedor
            #

            if (
                resultado["saida_provedor"] is None
                and hop.asn
                and hop.asn != primeiro_asn
            ):

                resultado["saida_provedor"] = hop

            #
            # Rede de conteúdo
            #

            if (
                hop.evento.startswith("Rede ")
                and resultado["rede_destino"] is None
            ):

                resultado["rede_destino"] = hop

        return resultado