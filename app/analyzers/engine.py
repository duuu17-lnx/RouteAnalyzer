from app.analyzers.asn_analyzer import ASNAnalyzer
from app.analyzers.correlation_analyzer import CorrelationAnalyzer
from app.analyzers.latency_analyzer import LatencyAnalyzer
from app.analyzers.loss_analyzer import LossAnalyzer
from app.analyzers.route_analyzer import RouteAnalyzer


class AnalyzerEngine:

    def analyze(self, trace):

        diagnosticos = []

        rota = RouteAnalyzer().analyze(trace)
        asn = ASNAnalyzer().analyze(trace)
        latencia = LatencyAnalyzer().analyze(trace)
        perda = LossAnalyzer().analyze(trace)
        correlacao = CorrelationAnalyzer().analyze(trace)

        #
        # Backbone
        #

        if rota["backbone"]:

            diagnosticos.append(
                f"Backbone identificado: {rota['backbone'].empresa} ({rota['backbone'].asn})."
            )

        #
        # Saída da rede
        #

        if rota["saida_provedor"]:

            diagnosticos.append(
                f"A saída da rede ocorreu no hop {rota['saida_provedor'].numero}."
            )

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
        # Rede destino
        #

        if rota["rede_destino"]:

            diagnosticos.append(
                f"A entrada na rede {rota['rede_destino'].observacao} ocorreu no hop {rota['rede_destino'].numero}."
            )

        #
        # RTT
        #

        if latencia["hop"]:

            diagnosticos.append(
                f"Maior Δ RTT: +{latencia['maior_delta']:.2f} ms (Hop {latencia['hop'].numero})."
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
        # Perda real
        #

        if perda["hop"]:

            if perda["persistente"]:

                diagnosticos.append(
                    f"A perda iniciou no hop {perda['hop'].numero} e permaneceu até o destino."
                )

            else:

                diagnosticos.append(
                    f"A perda observada no hop {perda['hop'].numero} não permaneceu até o destino."
                )

        #
        # ASN
        #

        diagnosticos.append(
            f"Foram percorridos {asn['total_asns']} ASNs."
        )

        #
        # Correlação Inteligente
        #

        diagnosticos.extend(correlacao)

        return diagnosticos