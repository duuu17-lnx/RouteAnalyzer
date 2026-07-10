import time

from app.analyzers.comparison_analyzer import ComparisonAnalyzer
from app.analyzers.engine import AnalyzerEngine
from app.analyzers.intermittency_analyzer import IntermittencyAnalyzer
from app.analyzers.latency_analyzer import LatencyAnalyzer
from app.analyzers.loss_analyzer import LossAnalyzer
from app.analyzers.network_behavior_analyzer import NetworkBehaviorAnalyzer

from app.collectors.asn import ASNCollector
from app.collectors.dns import DNSCollector
from app.collectors.mtr import MTRCollector

from app.models.multi_trace_result import MultiTraceResult


class AnalysisRunner:

    def run(self, destino):

        inicio = time.perf_counter()

        dns = DNSCollector()

        ip_destino = dns.resolve(destino)

        if not ip_destino:

            return None

        ASNCollector.clear_cache()

        quantidade_mtr = 3

        collector = MTRCollector()

        multi = MultiTraceResult()

        print()

        for i in range(quantidade_mtr):

            print(f"Executando MTR {i + 1}/{quantidade_mtr}...")

            trace = collector.run(destino)

            multi.add(trace)

        print()

        resultado = ComparisonAnalyzer().analyze(multi)

        NetworkBehaviorAnalyzer().analyze(resultado)

        IntermittencyAnalyzer().analyze(resultado)

        resultado.destino = destino
        resultado.destino_ip = ip_destino

        asn = ASNCollector().lookup(ip_destino)

        if asn:

            resultado.destino_asn = str(asn["asn"])
            resultado.destino_empresa = asn["description"]
            resultado.destino_pais = asn["country"]
            resultado.destino_prefixo = asn["prefix"]

        latency = LatencyAnalyzer().analyze(resultado)

        loss = LossAnalyzer().analyze(resultado)

        resultado.diagnosticos = AnalyzerEngine().analyze(resultado)

        tempo = time.perf_counter() - inicio

        return {

            "resultado": resultado,

            "latency": latency,

            "loss": loss,

            "tempo": tempo,

            "quantidade_mtr": quantidade_mtr,

            "ips_consultados": ASNCollector.cache_size()

        }