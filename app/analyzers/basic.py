from models.trace_result import TraceResult


class BasicAnalyzer:

    def analyze(self, trace: TraceResult):

        problemas = []

        if len(trace.hops) == 0:
            problemas.append("Nenhum hop encontrado.")

        ultimo = trace.hops[-1]

        if ultimo.loss > 0:
            problemas.append(
                f"O destino respondeu com {ultimo.loss:.1f}% de perda."
            )

        return problemas