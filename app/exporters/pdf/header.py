from datetime import datetime

from reportlab.lib import colors
from reportlab.lib.units import cm

from reportlab.platypus import (
    Paragraph,
    Spacer,
    Table,
    TableStyle
)


class PDFHeader:

    def build(

        self,

        story,

        resultado,

        config,

        styles

    ):

        #
        # Título
        #

        story.append(

            Paragraph(

                "RouteAnalyzer",

                styles.title

            )

        )

        story.append(

            Paragraph(

                "Relatório Técnico de Diagnóstico de Rede",

                styles.subtitle

            )

        )

        story.append(

            Spacer(

                1,

                0.4 * cm

            )

        )

        #
        # Dados Gerais
        #

        story.append(

            Paragraph(

                "Dados Gerais",

                styles.section

            )

        )

        dados = [

            [

                "Origem",

                resultado.origem

            ],

            [

                "Destino",

                resultado.destino

            ],

            [

                "IP Destino",

                resultado.destino_ip

            ],

            [

                "ASN",

                resultado.destino_asn

            ],

            [

                "Empresa",

                resultado.destino_empresa

            ],

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

                "Data",

                datetime.now().strftime(

                    "%d/%m/%Y %H:%M:%S"

                )

            ]

        ]

        tabela = Table(

            dados,

            colWidths=[

                4 * cm,

                10 * cm

            ]

        )

        tabela.setStyle(

            TableStyle([

                (

                    "BACKGROUND",

                    (0, 0),

                    (0, -1),

                    colors.HexColor("#E6E6E6")

                ),

                (

                    "TEXTCOLOR",

                    (0, 0),

                    (0, -1),

                    colors.black

                ),

                (

                    "FONTNAME",

                    (0, 0),

                    (0, -1),

                    "Helvetica-Bold"

                ),

                (

                    "FONTNAME",

                    (1, 0),

                    (1, -1),

                    "Helvetica"

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