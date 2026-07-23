from app.models.trace_result import TraceResult


class NetworkBehaviorAnalyzer:

    def analyze(self, resultado: TraceResult):

        hops = resultado.hops

        if len(hops) < 2:
            return

        destino = hops[-1]

        #
        # Se o destino respondeu sem perda,
        # não existe evidência de perda de encaminhamento.
        # Todos os eventos intermediários passam a ser tratados
        # apenas como comportamento ICMP.
        #

        if destino.loss == 0:

            for hop in hops[:-1]:

                if hop.loss == 0:
                    continue

                hop.perda_real = False
                hop.icmp_filtrado = True

                if hop.loss >= 100:

                    hop.evento = "Hop Silencioso"
                    hop.observacao = (
                        "Equipamento não responde às sondas ICMP"
                    )

                else:

                    hop.evento = "ICMP Filtrado"
                    hop.observacao = (
                        "Firewall / ICMP Rate Limit"
                    )

            return

        #
        # Havendo perda no destino,
        # a análise detalhada permanece para a etapa
        # de correlação de perda.
        #