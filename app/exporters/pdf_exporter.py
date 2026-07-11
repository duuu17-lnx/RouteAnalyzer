from datetime import datetime
from pathlib import Path

from reportlab.lib.pagesizes import A4, landscape
from reportlab.lib.units import cm

from reportlab.platypus import SimpleDocTemplate

from app.exporters.pdf.styles import PDFStyles
from app.exporters.pdf.header import PDFHeader
from app.exporters.pdf.summary import PDFSummary
from app.exporters.pdf.hops_table import PDFHopsTable
from app.exporters.pdf.conclusion import PDFConclusion
from app.exporters.pdf.statistics import PDFStatistics
from app.exporters.pdf.footer import PDFFooter


class PDFExporter:

    def export(

        self,

        resultado,

        config,

        latency,

        loss,

        tempo,

        ips_consultados

    ):

        #
        # Pasta de saída
        #

        output = Path(

            "output"

        )

        output.mkdir(

            exist_ok=True

        )

        #
        # Nome do arquivo
        #

        arquivo = output / datetime.now().strftime(

            "RouteAnalyzer_%Y%m%d_%H%M%S.pdf"

        )

        #
        # Documento
        #

        doc = SimpleDocTemplate(

            str(arquivo),

            pagesize=landscape(A4),

            leftMargin=1.3 * cm,

            rightMargin=1.3 * cm,

            topMargin=1.5 * cm,

            bottomMargin=1.5 * cm

        )

        #
        # Estilos
        #

        styles = PDFStyles()

        #
        # Story
        #

        story = []

        #
        # Cabeçalho
        #

        PDFHeader().build(

            story,

            resultado,

            config,

            styles

        )

        #
        # Resumo
        #

        PDFSummary().build(

            story,

            resultado,

            config,

            latency,

            loss,

            tempo,

            styles

        )

        #
        # Hops
        #

        PDFHopsTable().build(

            story,

            resultado,

            styles

        )

        #
        # Conclusão
        #

        PDFConclusion().build(

            story,

            resultado,

            config,

            styles

        )

        #
        # Estatísticas
        #

        PDFStatistics().build(

            story,

            resultado,

            config,

            tempo,

            ips_consultados,

            styles

        )

        #
        # Rodapé
        #

        PDFFooter().build(

            story,

            styles

        )

        #
        # Gera PDF
        #

        doc.build(

            story

        )

        return arquivo