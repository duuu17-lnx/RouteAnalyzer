from dataclasses import dataclass, field


@dataclass
class LossScenario:

    name: str

    description: str

    expected_hop: int | None

    expected_persistent: bool

    hops: list = field(default_factory=list)


class LossScenarios:
    """
    Biblioteca de cenários sintéticos para validar
    o mecanismo de diagnóstico de perda.

    Cada cenário representa um comportamento clássico
    encontrado em redes IP.
    """

    def all(self):

        return [

            #
            # Sem perda
            #

            LossScenario(

                name="SEM_PERDA",

                description="Rota completamente saudável.",

                expected_hop=None,

                expected_persistent=False,

                hops=[
                    (0, False, False),
                    (0, False, False),
                    (0, False, False),
                    (0, False, False),
                    (0, False, False),
                ]

            ),

            #
            # Perda persistente
            #

            LossScenario(

                name="PERDA_BACKBONE",

                description="Perda iniciando no hop 5 e permanecendo até o destino.",

                expected_hop=5,

                expected_persistent=True,

                hops=[
                    (0, False, False),
                    (0, False, False),
                    (0, False, False),
                    (0, False, False),

                    (18, True, False),
                    (19, True, False),
                    (20, True, False),
                    (18, True, False),
                    (19, True, False),
                ]

            ),

            #
            # ICMP filtrado
            #

            LossScenario(

                name="ICMP_FILTER",

                description="Perda causada apenas por filtragem ICMP.",

                expected_hop=None,

                expected_persistent=False,

                hops=[
                    (0, False, False),
                    (80, False, True),
                    (0, False, False),
                    (0, False, False),
                    (0, False, False),
                ]

            ),

            #
            # Perda apenas destino
            #

            LossScenario(

                name="DESTINO",

                description="Somente o destino apresenta perda.",

                expected_hop=5,

                expected_persistent=False,

                hops=[
                    (0, False, False),
                    (0, False, False),
                    (0, False, False),
                    (0, False, False),
                    (12, True, False),
                ]

            ),

            #
            # Perda isolada
            #

            LossScenario(

                name="ISOLADA",

                description="Perda em um único hop intermediário.",

                expected_hop=3,

                expected_persistent=False,

                hops=[
                    (0, False, False),
                    (0, False, False),
                    (12, True, False),
                    (0, False, False),
                    (0, False, False),
                ]

            ),

        ]