from app.models.hop import Hop
from app.models.trace_result import TraceResult


class TraceBuilder:
    """
    Constrói um TraceResult sintético para testes.

    Cada hop é representado por uma tupla:

        (
            loss,
            perda_real,
            icmp_filtrado
        )
    """

    def build(self, hops):

        trace = TraceResult()

        trace.hops = []

        anterior = None

        for indice, dados in enumerate(hops, start=1):

            loss, perda_real, icmp_filtrado = dados

            hop = Hop()

            #
            # Identificação
            #

            hop.index = indice
            hop.host = f"hop-{indice}"
            hop.ip = f"10.0.0.{indice}"

            #
            # Perda
            #

            hop.loss = float(loss)
            hop.perda_real = perda_real
            hop.icmp_filtrado = icmp_filtrado

            #
            # Latência
            #

            hop.last = indice
            hop.avg = indice
            hop.best = indice
            hop.worst = indice
            hop.stdev = 0.0

            #
            # Informações auxiliares
            #

            hop.asn = 65000
            hop.as_name = "TEST"

            #
            # RTT incremental
            #

            if anterior is None:

                hop.delta_rtt = 0.0

            else:

                hop.delta_rtt = hop.avg - anterior.avg

            trace.hops.append(hop)

            anterior = hop

        return trace