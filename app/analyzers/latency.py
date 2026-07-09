from analyzers.base import Analyzer


class LatencyAnalyzer(Analyzer):

    def analyze(self, trace):

        problemas = []

        if len(trace.hops) < 2:
            return problemas

        anterior = trace.hops[0]

        for hop in trace.hops[1:]:

            aumento = hop.avg - anterior.avg

            if aumento > 20:

                problemas.append(
                    f"Aumento de latência de {aumento:.1f} ms entre os hops "
                    f"{anterior.numero} e {hop.numero}."
                )

            anterior = hop

        return problemas