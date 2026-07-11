from reportlab.lib.units import cm

from reportlab.platypus import (
    Paragraph,
    Spacer
)


class PDFConclusion:

    def build(

        self,

        story,

        resultado,

        config,

        styles

    ):

        story.append(

            Paragraph(

                "Conclusão",

                styles.section

            )

        )

        story.append(

            Paragraph(

                f"A análise foi realizada utilizando "

                f"{config.execucoes} execuções independentes, "

                f"com {config.ciclos} ciclos por execução.",

                styles.normal

            )

        )

        story.append(

            Spacer(

                1,

                0.25 * cm

            )

        )

        for diagnostico in resultado.diagnosticos:

            story.append(

                Paragraph(

                    f"• {diagnostico}",

                    styles.normal

                )

            )

        if resultado.intermitencia:

            story.append(

                Paragraph(

                    f"• Foi detectada intermitência no hop "

                    f"{resultado.hop_mais_instavel}, "

                    f"com variação máxima de "

                    f"{resultado.maior_variacao:.2f} ms.",

                    styles.normal

                )

            )

        else:

            story.append(

                Paragraph(

                    f"• As {config.execucoes} execuções apresentaram "

                    f"comportamento consistente.",

                    styles.normal

                )

            )

        story.append(

            Spacer(

                1,

                0.7 * cm

            )

        )