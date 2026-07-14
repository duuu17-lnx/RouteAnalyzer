from concurrent.futures import ThreadPoolExecutor
from concurrent.futures import as_completed
import socket

from app.analyzers.hop_classifier import HopClassifier
from app.analyzers.location_analyzer import LocationAnalyzer

from app.collectors.asn import ASNCollector
from app.collectors.windows_ping import WindowsPing
from app.collectors.windows_tracert import WindowsTracert

from app.models.hop import Hop
from app.models.trace_result import TraceResult


class WindowsMTRCollector:

    def __init__(self):

        self.asn = ASNCollector()

        self.location = LocationAnalyzer()

        self.hop_classifier = HopClassifier()

        self.tracert = WindowsTracert()

        self.ping = WindowsPing()

        #
        # Cache da rota
        #

        self.route_cache = None

        self.destination_cache = None


    def run(self, destino: str, ciclos: int):

        #
        # Primeira execução:
        # descobre toda a rota.
        #

        if (

            self.route_cache is None

            or

            self.destination_cache != destino

        ):

            self.route_cache = self._discover_route(

                destino

            )

            self.destination_cache = destino

        #
        # Demais execuções:
        # atualiza apenas os valores do tracert.
        #

        else:

            rota_atual = self._discover_route(

                destino

            )

            for antigo, novo in zip(

                self.route_cache,

                rota_atual

            ):

                antigo["ip"] = novo["ip"]
                antigo["loss"] = novo["loss"]
                antigo["avg"] = novo["avg"]
                antigo["best"] = novo["best"]
                antigo["worst"] = novo["worst"]

        #
        # Executa os pings
        #

        ping_results = self._collect_ping_results(

            self.route_cache,

            ciclos

        )

        #
        # Constrói os hops
        #

        hops = self._build_hops(

            self.route_cache,

            ping_results

        )

        #
        # Classificação lógica
        #

        self.hop_classifier.classify(

            hops

        )

        return TraceResult(

            origem=socket.gethostname(),

            destino=destino,

            hops=hops

        )
    def _discover_route(self, destino):

        rota = self.tracert.run(

            destino

        )

        if not rota:

            raise RuntimeError(

                "Não foi possível descobrir a rota."

            )

        return rota


    def _collect_ping_results(self, rota, ciclos):

        resultados = {}

        with ThreadPoolExecutor(

            max_workers=16

        ) as executor:

            futures = {

                executor.submit(

                    self.ping.run,

                    hop["ip"],

                    ciclos

                ): hop["ip"]

                for hop in rota

            }

            for future in as_completed(

                futures

            ):

                ip = futures[future]

                try:

                    resultados[ip] = future.result()

                except Exception:

                    resultados[ip] = {

                        "loss": 100.0,

                        "sent": ciclos,

                        "received": 0,

                        "last": 0.0,

                        "avg": 0.0,

                        "best": 0.0,

                        "worst": 0.0,

                        "stdev": 0.0

                    }

        return resultados
    def _build_hops(self, rota, ping_results):

        hops = []

        ultimo_rtt_valido = None

        for indice, dados_hop in enumerate(rota):

            ip = dados_hop["ip"]

            estatisticas = ping_results.get(ip)

            if estatisticas is None:

                estatisticas = {

                    "loss": 100.0,

                    "sent": 0,

                    "received": 0,

                    "last": 0.0,

                    "avg": 0.0,

                    "best": 0.0,

                    "worst": 0.0,

                    "stdev": 0.0

                }

            #
            # RTT medido pelo TRACERT
            #

            tracert_avg = float(

                dados_hop.get(

                    "avg",

                    0.0

                )

            )

            eh_gateway = indice == 0

            hop_silencioso = (

                dados_hop["loss"] == 100.0

            )

            #
            # Δ RTT
            #

            eh_destino = indice == len(rota) - 1

            #
            # Δ RTT
            #

            if eh_gateway:

                delta = 0.0

            elif hop_silencioso:

                delta = None

            elif eh_destino:

                delta = None

            elif ultimo_rtt_valido is None:

                delta = 0.0

            else:

                delta = round(

                    tracert_avg - ultimo_rtt_valido,

                    2

                )
            info_asn = self.asn.lookup(ip)

            hop = Hop(

                numero=dados_hop["numero"],

                host=ip,

                ip=ip,

                hostname="",

                delta_rtt=delta,

                tracert_avg=tracert_avg,

                loss=dados_hop["loss"],

                sent=estatisticas["sent"],

                last=estatisticas["last"],

                avg=estatisticas["avg"],

                best=estatisticas["best"],

                worst=estatisticas["worst"],

                stdev=estatisticas["stdev"]

            )

            if info_asn:

                empresa = info_asn["description"]

                if " - " in empresa:

                    empresa = empresa.split(

                        " - ",

                        1

                    )[1].strip()

                hop.asn = f"AS{info_asn['asn']}"

                hop.empresa = empresa

                hop.prefixo = info_asn["prefix"]

                hop.pais = info_asn["country"]

            hop.localizacao = self.location.classify(

                hop

            )

            hops.append(

                hop

            )

            #
            # Todo hop que possui RTT no tracert
            # vira referência para o próximo Δ RTT.
            #

            if tracert_avg > 0:

                ultimo_rtt_valido = tracert_avg

        return hops