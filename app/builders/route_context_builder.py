from app.models.route_context import RouteContext


class RouteContextBuilder:
    """
    Responsável por construir o contexto compartilhado
    da rota.
    """

    def build(self, trace):

        return RouteContext(
            trace=trace
        )