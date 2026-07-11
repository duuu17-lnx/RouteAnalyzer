import time

from app.analyzers.comparison_analyzer import ComparisonAnalyzer
from app.analyzers.engine import AnalyzerEngine
from app.analyzers.intermittency_analyzer import IntermittencyAnalyzer
from app.analyzers.latency_analyzer import LatencyAnalyzer
from app.analyzers.loss_analyzer import LossAnalyzer
from app.analyzers.network_behavior_analyzer import NetworkBehaviorAnalyzer

from app.collectors.asn import ASNCollector
from app.collectors.dns import DNSCollector
from app.collectors.collector_factory import CollectorFactory

from app.models.multi_trace_result import MultiTraceResult

from app.utils.progress import Progress
from app.utils.processing import Processing


class AnalysisRunner:

    def run(self, destino, config):

        inicio = time.perf_counter()

        dns = DNSCollector()

        ip_destino = dns.resolve(destino)

        if not ip_destino:

            return None

        ASNCollector.clear_cache()

        collector = CollectorFactory().get()

        progress = Progress()

        processing = Processing()

        multi = MultiTraceResult()

        for i in range(config.execucoes):

            progress.show(

                atual=i + 1,

                total=config.execucoes,

                destino=destino,

                config=config

            )

            trace = collector.run(

                destino,

                ciclos=config.ciclos

            )

            multi.add(trace)

        print()

        print("✓ Coleta concluída com sucesso.")

        processing.start()

        processing.step("Comparando execuções")

        resultado = ComparisonAnalyzer().analyze(multi)

        processing.step("Analisando comportamento da rede")

        NetworkBehaviorAnalyzer().analyze(resultado)

        processing.step("Detectando intermitência")

        IntermittencyAnalyzer().analyze(resultado)

        processing.step("Identificando ASN do destino")

        resultado.destino = destino

        resultado.destino_ip = ip_destino

        asn = ASNCollector().lookup(ip_destino)

        if asn:

            resultado.destino_asn = str(asn["asn"])

            resultado.destino_empresa = asn["description"]

            resultado.destino_pais = asn["country"]

            resultado.destino_prefixo = asn["prefix"]

        processing.step("Calculando latência")

        latency = LatencyAnalyzer().analyze(resultado)

        processing.step("Calculando perda de pacotes")

        loss = LossAnalyzer().analyze(resultado)

        processing.step("Gerando diagnóstico")

        resultado.diagnosticos = AnalyzerEngine().analyze(resultado)

        processing.step("Finalizando relatório")

        processing.finish()

        tempo = time.perf_counter() - inicio

        return {

            "resultado": resultado,

            "latency": latency,

            "loss": loss,

            "tempo": tempo,

            "quantidade_mtr": config.execucoes,

            "ips_consultados": ASNCollector.cache_size()

        }