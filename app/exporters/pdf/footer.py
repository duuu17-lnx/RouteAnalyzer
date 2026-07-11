from datetime import datetime

from reportlab.platypus import (
    Paragraph,
    Spacer
)


class PDFFooter:

    def build(

        self,

        story,

        styles

    ):

        story.append(

            Spacer(

                1,

                0.8

            )

        )

        story.append(

            Paragraph(

                "<b>RouteAnalyzer</b>",

                styles.small

            )

        )

        story.append(

            Paragraph(

                "Relatório gerado automaticamente.",

                styles.small

            )

        )

        story.append(

            Paragraph(

                datetime.now().strftime(

                    "%d/%m/%Y %H:%M:%S"

                ),

                styles.small

            )

        )