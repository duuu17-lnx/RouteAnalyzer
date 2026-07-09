from app.models.trace_result import TraceResult


class NetworkBehaviorAnalyzer:

    def analyze(self, resultado: TraceResult):

        hops = resultado.hops

        if len(hops) < 2:
            return

        destino = hops[-1]

        #
        # Se existe perda no destino,
        # não podemos afirmar que seja apenas ICMP.
        #

        if destino.loss > 0:
            return

        i = 0

        while i < len(hops) - 1:

            hop = hops[i]

            #
            # Hop sem perda
            #

            if hop.loss == 0:

                i += 1
                continue

            #
            # Localiza um bloco contínuo de perda
            #

            inicio = i
            fim = i

            while fim + 1 < len(hops):

                if hops[fim + 1].loss == 0:
                    break

                fim += 1

            #
            # Verifica se existe perda após o bloco
            #

            propagou = False

            for restante in hops[fim + 1:]:

                if restante.loss > 0:

                    propagou = True
                    break

            #
            # Bloco compatível com ICMP filtrado
            #

            if not propagou:

                for j in range(inicio, fim + 1):

                    bloco = hops[j]

                    bloco.perda_real = False
                    bloco.icmp_filtrado = True

                    if bloco.loss >= 100:

                        bloco.evento = "Hop Silencioso"
                        bloco.observacao = (
                            "Equipamento não responde às sondas ICMP"
                        )

                    else:

                        bloco.evento = "ICMP Filtrado"
                        bloco.observacao = (
                            "Firewall / ICMP Rate Limit"
                        )

            i = fim + 1