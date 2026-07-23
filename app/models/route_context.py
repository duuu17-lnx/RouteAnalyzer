from dataclasses import dataclass

from app.models.trace_result import TraceResult


@dataclass
class RouteContext:
    """
    Contexto compartilhado da rota.

    Este objeto contém informações derivadas da rota que podem ser
    reutilizadas por todos os analisadores, evitando cálculos
    repetidos.
    """

    trace: TraceResult