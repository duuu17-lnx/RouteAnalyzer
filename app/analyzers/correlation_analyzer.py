class CorrelationAnalyzer:

    def analyze(self, trace):

        conclusoes = []

        #
        # Procura onde saiu do backbone
        #

        hop_saida = None

        for hop in trace.hops:

            if hop.evento in (
                "IX.br",
                "Trânsito",
                "Rede Google",
                "Rede Microsoft",
                "Rede Cloudflare",
                "Rede AWS",
                "Rede Meta",
                "Rede Akamai",
                "Rede Fastly",
                "Troca de ASN"
            ):

                hop_saida = hop
                break

        #
        # Maior aumento de RTT
        #

        maior_delta = 0
        hop_delta = None

        for hop in trace.hops:

            if hop.delta_rtt > maior_delta:

                maior_delta = hop.delta_rtt
                hop_delta = hop

        #
        # Perda persistente
        #

        perda_final = trace.hops[-1].loss

        #
        # Correlação
        #

        if hop_saida and hop_delta:

            if hop_delta.numero >= hop_saida.numero:

                if maior_delta >= 20:

                    conclusoes.append(
                        "O maior aumento de latência ocorreu após a saída da rede do provedor."
                    )

        if perda_final == 0:

            conclusoes.append(
                "Não foi observada perda fim a fim."
            )

        #
        # Problema provável
        #

        if perda_final == 0 and maior_delta < 20:

            conclusoes.append(
                "A rota apresenta comportamento compatível com operação normal."
            )

        return conclusoes