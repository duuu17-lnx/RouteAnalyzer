from copy import deepcopy


class ComparisonAnalyzer:

    def analyze(self, multi_trace):

        if not multi_trace.traces:
            return None

        resultado = deepcopy(multi_trace.traces[0])

        #
        # Estes campos serão preenchidos futuramente
        # pelo IntermittencyAnalyzer
        #

        resultado.intermitencia = False
        resultado.maior_variacao = 0.0
        resultado.hop_mais_instavel = 0
        resultado.hops_instaveis = []

        #
        # Consolida hop por hop
        #

        for indice, hop in enumerate(resultado.hops):

            amostras = []

            for trace in multi_trace.traces:

                if indice < len(trace.hops):
                    amostras.append(trace.hops[indice])

            if not amostras:
                continue

            rtts = [h.avg for h in amostras]

            hop.avg = round(sum(rtts) / len(rtts), 2)

            hop.best = min(h.best for h in amostras)

            hop.worst = max(h.worst for h in amostras)

            hop.loss = round(
                sum(h.loss for h in amostras) / len(amostras),
                2
            )

            hop.stdev = round(
                sum(h.stdev for h in amostras) / len(amostras),
                2
            )

            hop.last = amostras[-1].last

            #
            # Apenas armazena a variação.
            # A decisão sobre intermitência será tomada depois.
            #

            hop.variacao_execucoes = round(
                max(rtts) - min(rtts),
                2
            )

            hop.rtts = rtts

        #
        # Recalcula Δ RTT
        #

        anterior = None

        for hop in resultado.hops:

            if anterior is None:
                hop.delta_rtt = 0
            else:
                hop.delta_rtt = round(
                    hop.avg - anterior.avg,
                    2
                )

            anterior = hop

        return resultado