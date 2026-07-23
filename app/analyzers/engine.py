from app.analyzers.asn_analyzer import ASNAnalyzer
from app.analyzers.correlation_analyzer import CorrelationAnalyzer
from app.analyzers.route_analyzer import RouteAnalyzer


class AnalyzerEngine:

    def analyze(self, trace, latency, loss):

        diagnosticos = []

        #
        # Analyzers que ainda pertencem ao Engine
        #

        rota = RouteAnalyzer().analyze(trace)
        asn = ASNAnalyzer().analyze(trace)
        correlacao = CorrelationAnalyzer().analyze(trace)

        #
        # IX
        #

        if rota["ix"]:

            diagnosticos.append(
                f"O tráfego passou pelo IX.br no hop {rota['ix'].numero}."
            )

        #
        # Trânsito
        #

        if rota["transito"]:

            diagnosticos.append(
                f"O trânsito foi realizado pela {rota['transito'].observacao}."
            )

        #
        # Hops com ICMP filtrado
        #

        hops_icmp = [hop for hop in trace.hops if hop.icmp_filtrado]

        if hops_icmp:

            if len(hops_icmp) == 1:

                hop = hops_icmp[0]

                diagnosticos.append(
                    f"O hop {hop.numero} apresentou perda apenas nas respostas ICMP. "
                    "Os hops seguintes responderam normalmente, indicando comportamento "
                    "compatível com Firewall, ICMP Rate Limit ou CoPP."
                )

            else:

                lista = ", ".join(str(h.numero) for h in hops_icmp)

                diagnosticos.append(
                    f"Os hops {lista} apresentaram perda apenas nas respostas ICMP. "
                    "Os hops subsequentes responderam normalmente, indicando limitação "
                    "das respostas ICMP, sem evidências de perda de encaminhamento."
                )

        #
        # Correlação Inteligente
        #

        diagnosticos.extend(correlacao)

        return diagnosticos