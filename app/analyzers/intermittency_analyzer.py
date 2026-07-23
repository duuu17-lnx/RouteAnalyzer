class IntermittencyAnalyzer:

    LIMIAR_VARIACAO = 10.0

    def analyze(self, trace):

        trace.intermitencia = False
        trace.maior_variacao = 0.0
        trace.hop_mais_instavel = 0
        trace.hops_instaveis = []

        #
        # Sem hops
        #

        if not trace.hops:
            return trace

        #
        # A intermitência da rota só existe se o destino
        # também apresentar variação significativa.
        #

        destino = trace.hops[-1]

        if destino.variacao_execucoes < self.LIMIAR_VARIACAO:
            return trace

        #
        # Identifica quais hops também apresentaram variação.
        #

        for hop in trace.hops:

            #
            # Ignora hops que apenas filtram ICMP
            #

            if hop.icmp_filtrado:
                continue

            #
            # Ignora hops sem perda real (quando aplicável)
            #

            if not hop.perda_real and hop.loss > 0:
                continue

            #
            # Analisa a variação entre as execuções
            #

            if hop.variacao_execucoes >= self.LIMIAR_VARIACAO:

                trace.intermitencia = True

                trace.hops_instaveis.append(hop.numero)

                if hop.variacao_execucoes > trace.maior_variacao:

                    trace.maior_variacao = hop.variacao_execucoes
                    trace.hop_mais_instavel = hop.numero

        return trace