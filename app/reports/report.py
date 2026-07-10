from app.utils.header import mostrar_header
from app.utils.table import mostrar_hops


class Report:

    def show(
        self,
        resultado,
        quantidade_mtr,
        latency,
        loss,
        tempo,
        ips_consultados
    ):

        mostrar_header(resultado)

        mostrar_hops(resultado.hops)

        self._mostrar_resumo(
            resultado,
            quantidade_mtr,
            latency,
            loss
        )

        self._mostrar_conclusao(
            resultado,
            quantidade_mtr
        )

        self._mostrar_estatisticas(
            quantidade_mtr,
            ips_consultados,
            tempo
        )

    def _mostrar_resumo(
        self,
        resultado,
        quantidade_mtr,
        latency,
        loss
    ):

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

    def _mostrar_conclusao(
        self,
        resultado,
        quantidade_mtr
    ):

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

    def _mostrar_estatisticas(
        self,
        quantidade_mtr,
        ips_consultados,
        tempo
    ):

        print()

        print("Estatísticas")
        print("-" * 92)

        print(f"✓ MTR executados....: {quantidade_mtr}")
        print(f"✓ IPs consultados...: {ips_consultados}")
        print(f"✓ Tempo total.......: {tempo:.2f} s")
