from datetime import datetime

from reportlab.lib.styles import getSampleStyleSheet
from reportlab.lib.units import cm
from reportlab.platypus import (
    Paragraph,
    SimpleDocTemplate,
    Spacer
)

from app.application.application_diagnosis import ApplicationDiagnosis
from app.utils.report_directory import ReportDirectory


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

        output = ReportDirectory.get_directory()

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
        # Descobre o destino efetivo
        #

        ultimo = resultado

        while getattr(

            ultimo,

            "redirect_result",

            None

        ):

            ultimo = ultimo.redirect_result

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

        if resultado.redirect:

            story.append(

                Paragraph(

                    f"<b>Redirecionamentos:</b> {resultado.redirects}",

                    styles["BodyText"]

                )

            )

            if resultado.location:

                story.append(

                    Paragraph(

                        f"<b>Location:</b> {resultado.location}",

                        styles["BodyText"]

                    )

                )

        if ultimo is not resultado:

            story.append(

                Paragraph(

                    f"<b>Destino Efetivo:</b> {ultimo.url}",

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