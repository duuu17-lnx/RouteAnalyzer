import time

from app.analyzers.comparison_analyzer import ComparisonAnalyzer
from app.analyzers.network_behavior_analyzer import NetworkBehaviorAnalyzer
from app.analyzers.intermittency_analyzer import IntermittencyAnalyzer
from app.analyzers.engine import AnalyzerEngine
from app.analyzers.latency_analyzer import LatencyAnalyzer
from app.analyzers.loss_analyzer import LossAnalyzer

from app.collectors.asn import ASNCollector
from app.collectors.dns import DNSCollector
from app.collectors.mtr import MTRCollector

from app.models.multi_trace_result import MultiTraceResult

from app.utils.header import mostrar_header
from app.utils.table import mostrar_hops


def main():

    inicio = time.perf_counter()

    print("\nExecutando análise...\n")

    destino = input("Destino: ").strip()

    dns = DNSCollector()

    ip_destino = dns.resolve(destino)

    if not ip_destino:
        print("\nErro: não foi possível resolver o destino.")
        return

    ASNCollector.clear_cache()

    multi = MultiTraceResult()

    collector = MTRCollector()

    quantidade_mtr = 3

    print()

    for i in range(quantidade_mtr):

        print(f"Executando MTR {i + 1}/{quantidade_mtr}...")

        trace = collector.run(destino)

        multi.add(trace)

    print()

    #
    # Consolida os três MTRs
    #

    resultado = ComparisonAnalyzer().analyze(multi)

    #
    # Analisa o comportamento da rede
    #

    NetworkBehaviorAnalyzer().analyze(resultado)

    #
    # Detecta intermitência (ignorando ICMP filtrado)
    #

    IntermittencyAnalyzer().analyze(resultado)

    #
    # Informações do destino
    #

    resultado.destino = destino
    resultado.destino_ip = ip_destino

    asn = ASNCollector().lookup(ip_destino)

    if asn:

        resultado.destino_asn = str(asn["asn"])
        resultado.destino_empresa = asn["description"]
        resultado.destino_pais = asn["country"]
        resultado.destino_prefixo = asn["prefix"]

    #
    # Exibição
    #

    mostrar_header(resultado)

    mostrar_hops(resultado.hops)

    #
    # Analisadores
    #

    latency = LatencyAnalyzer().analyze(resultado)

    loss = LossAnalyzer().analyze(resultado)

    engine = AnalyzerEngine()

    resultado.diagnosticos = engine.analyze(resultado)

    #
    # Resumo
    #

    print("\nResumo")
    print("-" * 92)

    print(f"✓ MTR Executados....: {quantidade_mtr}")
    print(f"✓ Hops..............: {len(resultado.hops)}")
    print(f"✓ RTT Final.........: {resultado.hops[-1].avg:.2f} ms")
    print(f"✓ Perda Final.......: {resultado.hops[-1].loss:.1f}%")

    if latency["hop"]:

        print(
            f"✓ Maior Δ RTT.......: +{latency['maior_delta']:.2f} ms "
            f"(Hop {latency['hop'].numero})"
        )

    else:

        print(
            "✓ Maior Δ RTT.......: Não identificado"
        )

    if loss["hop"]:

        print(
            f"✓ Primeira perda....: Hop {loss['hop'].numero}"
        )

        print(
            f"✓ Perda persistente.: {'Sim' if loss['persistente'] else 'Não'}"
        )

    if resultado.intermitencia:

        print("✓ Intermitência.....: Detectada")

        print(
            f"✓ Hop mais instável.: {resultado.hop_mais_instavel}"
        )

        print(
            f"✓ Maior variação....: {resultado.maior_variacao:.2f} ms"
        )

    else:

        print("✓ Intermitência.....: Não detectada")

    #
    # Conclusão
    #

    print()

    print("Conclusão")
    print("-" * 92)

    print(
        f"• A análise foi baseada em {quantidade_mtr} execuções independentes do MTR."
    )

    for item in resultado.diagnosticos:

        print(f"• {item}")

    if resultado.intermitencia:

        print(
            f"• Foi detectada intermitência no hop "
            f"{resultado.hop_mais_instavel}, "
            f"com variação máxima de "
            f"{resultado.maior_variacao:.2f} ms entre as medições."
        )

    else:

        print(
            "• As três execuções apresentaram comportamento consistente."
        )

    #
    # Estatísticas
    #

    tempo = time.perf_counter() - inicio

    print()

    print("Estatísticas")
    print("-" * 92)

    print(f"✓ MTR executados....: {quantidade_mtr}")
    print(f"✓ IPs consultados...: {ASNCollector.cache_size()}")
    print(f"✓ Tempo total.......: {tempo:.2f} s")


if __name__ == "__main__":
    main()