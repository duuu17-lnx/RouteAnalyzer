from reportlab.lib import colors
from reportlab.lib.units import cm

from reportlab.platypus import (
    Paragraph,
    Spacer,
    Table,
    TableStyle
)


class PDFStatistics:

    def build(

        self,

        story,

        resultado,

        config,

        tempo,

        ips_consultados,

        styles

    ):

        story.append(

            Paragraph(

                "Estatísticas",

                styles.section

            )

        )

        dados = [

            [

                "Perfil",

                config.perfil

            ],

            [

                "Execuções",

                str(config.execucoes)

            ],

            [

                "Ciclos por Execução",

                str(config.ciclos)

            ],

            [

                "Amostras por Hop",

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

                "IPs Consultados",

                str(

                    ips_consultados

                )

            ],

            [

                "Tempo Total",

                f"{tempo:.2f} s"

            ]

        ]

        tabela = Table(

            dados,

            colWidths=[

                5 * cm,

                6 * cm

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