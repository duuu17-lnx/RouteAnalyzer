import json
import subprocess

from app.analyzers.hop_classifier import HopClassifier
from app.analyzers.location_analyzer import LocationAnalyzer
from app.collectors.asn import ASNCollector
from app.models.hop import Hop
from app.models.trace_result import TraceResult


class MTRCollector:

    def __init__(self):

        self.asn = ASNCollector()

        self.location = LocationAnalyzer()

        self.hop_classifier = HopClassifier()

    def run(self, destino: str, ciclos: int) -> TraceResult:

        comando = [

            "mtr",

            "--report",

            "--report-cycles",

            str(ciclos),

            "--json",

            "-n",

            destino

        ]

        resultado = subprocess.run(

            comando,

            capture_output=True,

            text=True

        )

        if resultado.returncode != 0:

            raise RuntimeError(resultado.stderr)

        dados = json.loads(resultado.stdout)

        hops = []

        hop_anterior = None

        #
        # Coleta dos hops
        #

        for indice, hop in enumerate(

            dados["report"]["hubs"],

            start=1

        ):

            ip = hop.get("host", "")

            avg = float(

                hop.get(

                    "Avg",

                    0

                )

            )

            if hop_anterior is None:

                delta = 0.0

            else:

                delta = round(

                    avg - hop_anterior.avg,

                    2

                )

            info_asn = self.asn.lookup(ip)

            novo_hop = Hop(

                numero=indice,

                host=ip,

                ip=ip,

                hostname="",

                delta_rtt=delta,

                loss=float(

                    hop.get(

                        "Loss%", 0

                    )

                ),

                sent=int(

                    hop.get(

                        "Snt", 0

                    )

                ),

                last=float(

                    hop.get(

                        "Last", 0

                    )

                ),

                avg=avg,

                best=float(

                    hop.get(

                        "Best", 0

                    )

                ),

                worst=float(

                    hop.get(

                        "Wrst", 0

                    )

                ),

                stdev=float(

                    hop.get(

                        "StDev", 0

                    )

                )

            )

            #
            # ASN
            #

            if info_asn:

                empresa = info_asn["description"]

                if " - " in empresa:

                    empresa = empresa.split(

                        " - ",

                        1

                    )[1].strip()

                novo_hop.asn = f"AS{info_asn['asn']}"

                novo_hop.empresa = empresa

                novo_hop.prefixo = info_asn["prefix"]

                novo_hop.pais = info_asn["country"]

            #
            # Localização lógica
            #

            novo_hop.localizacao = self.location.classify(

                novo_hop

            )

            hops.append(

                novo_hop

            )

            hop_anterior = novo_hop

        #
        # Classificação dos hops
        #

        self.hop_classifier.classify(hops)

        return TraceResult(

            origem=dados["report"]["mtr"]["src"],

            destino=dados["report"]["mtr"]["dst"],

            hops=hops

        )