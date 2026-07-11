from reportlab.lib import colors
from reportlab.lib.units import cm

from reportlab.platypus import (
    Paragraph,
    Spacer,
    Table,
    TableStyle
)


class PDFHopsTable:

    def build(

        self,

        story,

        resultado,

        styles

    ):

        story.append(

            Paragraph(

                "Tabela dos Hops",

                styles.section

            )

        )

        dados = [

            [

                Paragraph("<b>Hop</b>", styles.normal),

                Paragraph("<b>Host</b>", styles.normal),

                Paragraph("<b>Loss%</b>", styles.normal),

                Paragraph("<b>Avg</b>", styles.normal),

                Paragraph("<b>Δ RTT</b>", styles.normal),

                Paragraph("<b>ASN</b>", styles.normal),

                Paragraph("<b>Evento</b>", styles.normal),

                Paragraph("<b>Observação</b>", styles.normal)

            ]

        ]

        for hop in resultado.hops:

            #
            # Delta RTT
            #

            if hop.delta_rtt == 0:

                delta = "--"

            elif hop.delta_rtt > 0:

                delta = f"+{hop.delta_rtt:.2f}"

            else:

                delta = f"{hop.delta_rtt:.2f}"

            #
            # ASN
            #

            asn = hop.asn if hop.asn else "-"

            #
            # Linha
            #

            dados.append(

                [

                    Paragraph(

                        str(hop.numero),

                        styles.normal

                    ),

                    Paragraph(

                        hop.host,

                        styles.normal

                    ),

                    Paragraph(

                        f"{hop.loss:.1f}",

                        styles.normal

                    ),

                    Paragraph(

                        f"{hop.avg:.2f}",

                        styles.normal

                    ),

                    Paragraph(

                        delta,

                        styles.normal

                    ),

                    Paragraph(

                        asn,

                        styles.normal

                    ),

                    Paragraph(

                        hop.evento or "",

                        styles.normal

                    ),

                    Paragraph(

                        hop.observacao or "",

                        styles.normal

                    )

                ]

            )

        tabela = Table(

            dados,

            repeatRows=1,

            colWidths=[

                1.0 * cm,   # Hop

                5.2 * cm,   # Host

                1.5 * cm,   # Loss

                1.8 * cm,   # Avg

                1.8 * cm,   # Delta

                2.3 * cm,   # ASN

                4.2 * cm,   # Evento

                7.0 * cm    # Observação

            ]

        )

        estilo = [

            (

                "BACKGROUND",

                (0, 0),

                (-1, 0),

                colors.HexColor("#3F3F46")

            ),

            (

                "TEXTCOLOR",

                (0, 0),

                (-1, 0),

                colors.white

            ),

            (

                "FONTNAME",

                (0, 0),

                (-1, 0),

                "Helvetica-Bold"

            ),

            (

                "FONTSIZE",

                (0, 0),

                (-1, 0),

                9

            ),

            (

                "FONTSIZE",

                (0, 1),

                (-1, -1),

                8

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

                5

            ),

            (

                "TOPPADDING",

                (0, 0),

                (-1, -1),

                5

            ),

            (

                "VALIGN",

                (0, 0),

                (-1, -1),

                "MIDDLE"

            ),

            #
            # Alinhamentos
            #

            (

                "ALIGN",

                (0, 0),

                (0, -1),

                "CENTER"

            ),

            (

                "ALIGN",

                (2, 0),

                (4, -1),

                "RIGHT"

            ),

            (

                "ALIGN",

                (5, 0),

                (5, -1),

                "CENTER"

            ),

        ]

        #
        # Zebra
        #

        for linha in range(

            1,

            len(dados)

        ):

            if linha % 2 == 0:

                estilo.append(

                    (

                        "BACKGROUND",

                        (0, linha),

                        (-1, linha),

                        colors.HexColor("#F7F7F7")

                    )

                )

        tabela.setStyle(

            TableStyle(

                estilo

            )

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