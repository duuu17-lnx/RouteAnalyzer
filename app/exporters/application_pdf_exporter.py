from datetime import datetime

from reportlab.lib.styles import getSampleStyleSheet
from reportlab.lib.units import cm
from reportlab.platypus import (
    Paragraph,
    SimpleDocTemplate,
    Spacer
)

from app.application.application_diagnosis import ApplicationDiagnosis
from app.utils.app_paths import AppPaths


class ApplicationPDFExporter:

    def export(

        self,

        resultado,

        responsabilidade,

        estatisticas

    ):

        #
        # Pasta de saída
        #

        output = AppPaths.reports_dir()

        #
        # Nome do arquivo
        #

        arquivo = output / (

            "ApplicationReport_"

            + datetime.now().strftime("%Y%m%d_%H%M%S")

            + ".pdf"

        )

        styles = getSampleStyleSheet()

        doc = SimpleDocTemplate(

            str(arquivo),

            rightMargin=1.5 * cm,

            leftMargin=1.5 * cm,

            topMargin=1.5 * cm,

            bottomMargin=1.5 * cm

        )

        story = []

        #
        # Cabeçalho
        #

        story.append(

            Paragraph(

                "<b>RouteAnalyzer - Diagnóstico de Aplicação</b>",

                styles["Heading1"]

            )

        )

        story.append(

            Spacer(

                1,

                0.4 * cm

            )

        )

        #
        # Informações Gerais
        #

        story.append(

            Paragraph(

                f"<b>URL:</b> {resultado.url}",

                styles["BodyText"]

            )

        )

        story.append(

            Spacer(

                1,

                0.4 * cm

            )

        )

        #
        # Responsabilidade
        #

        story.append(

            Paragraph(

                "<b>Responsabilidade</b>",

                styles["Heading2"]

            )

        )

        for chave, valor in responsabilidade.items():

            story.append(

                Paragraph(

                    f"{chave}: {valor}",

                    styles["BodyText"]

                )

            )

        story.append(

            Spacer(

                1,

                0.4 * cm

            )

        )

        #
        # Estatísticas
        #

        story.append(

            Paragraph(

                "<b>Estatísticas</b>",

                styles["Heading2"]

            )

        )

        story.append(

            Paragraph(

                f"Execuções: {estatisticas['execucoes']}",

                styles["BodyText"]

            )

        )

        story.append(

            Paragraph(

                f"Válidas: {estatisticas['validas']}",

                styles["BodyText"]

            )

        )

        story.append(

            Paragraph(

                f"Falhas: {estatisticas['falhas']}",

                styles["BodyText"]

            )

        )

        story.append(

            Spacer(

                1,

                0.4 * cm

            )

        )

        #
        # Diagnóstico
        #

        story.append(

            Paragraph(

                "<b>Diagnóstico Final</b>",

                styles["Heading2"]

            )

        )

        diagnostico = ApplicationDiagnosis().build(

            resultado,

            responsabilidade,

            estatisticas

        )

        for linha in diagnostico:

            story.append(

                Paragraph(

                    f"• {linha}",

                    styles["BodyText"]

                )

            )

        doc.build(

            story

        )

        return arquivo