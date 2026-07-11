from reportlab.lib import colors
from reportlab.lib.enums import TA_CENTER

from reportlab.lib.styles import (
    getSampleStyleSheet,
    ParagraphStyle
)


class PDFStyles:

    def __init__(self):

        base = getSampleStyleSheet()

        self.title = ParagraphStyle(

            "RouteAnalyzerTitle",

            parent=base["Title"],

            fontName="Helvetica-Bold",

            fontSize=22,

            alignment=TA_CENTER,

            spaceAfter=18

        )

        self.subtitle = ParagraphStyle(

            "RouteAnalyzerSubtitle",

            parent=base["Heading2"],

            fontName="Helvetica",

            fontSize=12,

            alignment=TA_CENTER,

            textColor=colors.HexColor("#555555"),

            spaceAfter=20

        )

        self.section = ParagraphStyle(

            "Section",

            parent=base["Heading2"],

            fontName="Helvetica-Bold",

            fontSize=14,

            textColor=colors.HexColor("#303030"),

            spaceBefore=10,

            spaceAfter=10

        )

        self.normal = ParagraphStyle(

            "Normal",

            parent=base["Normal"],

            fontName="Helvetica",

            fontSize=10,

            leading=14

        )

        self.small = ParagraphStyle(

            "Small",

            parent=base["Normal"],

            fontName="Helvetica",

            fontSize=8,

            leading=10,

            textColor=colors.grey

        )