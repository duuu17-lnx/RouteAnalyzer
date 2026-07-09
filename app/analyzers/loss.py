from analyzers.base import Analyzer


class LossAnalyzer(Analyzer):

    def analyze(self, trace):

        problemas = []

        if not trace.hops:
            return problemas

        ultimo = trace.hops[-1]

        if ultimo.loss > 0:
            problemas.append(
                f"Destino respondeu com {ultimo.loss:.1f}% de perda."
            )

        return problemas