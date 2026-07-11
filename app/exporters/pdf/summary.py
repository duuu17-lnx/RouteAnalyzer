from reportlab.lib import colors
from reportlab.lib.units import cm

from reportlab.platypus import (
    Paragraph,
    Spacer,
    Table,
    TableStyle
)


class PDFSummary:

    def build(

        self,

        story,

        resultado,

        config,

        latency,

        loss,

        tempo,

        styles

    ):

        story.append(

            Paragraph(

                "Resumo",

                styles.section

            )

        )

        if latency["hop"]:

            maior_delta = (

                f"+{latency['maior_delta']:.2f} ms "

                f"(Hop {latency['hop'].numero})"

            )

        else:

            maior_delta = "Não identificado"

        if loss["hop"]:

            primeira_perda = str(

                loss["hop"].numero

            )

            persistente = (

                "Sim"

                if loss["persistente"]

                else "Não"

            )

        else:

            primeira_perda = "-"

            persistente = "-"

        resumo = [

            [

                "Perfil",

                config.perfil

            ],

            [

                "Execuções",

                str(config.execucoes)

            ],

            [

                "Ciclos",

                str(config.ciclos)

            ],

            [

                "Amostras / Hop",

                str(

                    config.execucoes *

                    config.ciclos

                )

            ],

            [

                "Quantidade de Hops",

                str(

                    len(resultado.hops)

                )

            ],

            [

                "RTT Final",

                f"{resultado.hops[-1].avg:.2f} ms"

            ],

            [

                "Perda Final",

                f"{resultado.hops[-1].loss:.1f}%"

            ],

            [

                "Maior Δ RTT",

                maior_delta

            ],

            [

                "Primeira Perda",

                primeira_perda

            ],

            [

                "Perda Persistente",

                persistente

            ],

            [

                "Tempo Total",

                f"{tempo:.2f} s"

            ]

        ]

        tabela = Table(

            resumo,

            colWidths=[

                5 * cm,

                9 * cm

            ]

        )

        tabela.setStyle(

            TableStyle([

                (

                    "BACKGROUND",

                    (0, 0),

                    (0, -1),

                    colors.HexColor("#EFEFEF")

                ),

                (

                    "FONTNAME",

                    (0, 0),

                    (0, -1),

                    "Helvetica-Bold"

                ),

                (

                    "GRID",

                    (0, 0),

                    (-1, -1),

                    0.25,

                    colors.grey

                ),

                (

                    "BOTTOMPADDING",

                    (0, 0),

                    (-1, -1),

                    6

                ),

                (

                    "TOPPADDING",

                    (0, 0),

                    (-1, -1),

                    6

                ),

                (

                    "VALIGN",

                    (0, 0),

                    (-1, -1),

                    "MIDDLE"

                )

            ])

        )

        story.append(

            tabela

        )

        story.append(

            Spacer(

                1,

                0.7 * cm

            )

        )