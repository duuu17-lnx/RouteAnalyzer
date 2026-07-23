from app.utils.header import mostrar_header
from app.utils.table import mostrar_hops


class Report:

    def show(
        self,
        resultado,
        config,
        latency,
        loss,
        tempo,
        ips_consultados
    ):

        mostrar_header(resultado)

        mostrar_hops(resultado.hops)

        self._mostrar_resumo(

            resultado,

            config,

            latency,

            loss

        )

        self._mostrar_conclusao(

            resultado,

            config,

            loss

        )

        self._mostrar_estatisticas(

            config,

            ips_consultados,

            tempo

        )

    def _mostrar_resumo(

        self,

        resultado,

        config,

        latency,

        loss

    ):

        print("\nResumo")
        print("-" * 92)

        print(f"✓ Perfil............: {config.perfil}")
        print(f"✓ Execuções.........: {config.execucoes}")
        print(f"✓ Ciclos............: {config.ciclos}")
        print(
            f"✓ Amostras/Hop......: "
            f"{config.execucoes * config.ciclos}"
        )

        print(f"✓ Hops..............: {len(resultado.hops)}")
        print(f"✓ RTT Final.........: {resultado.hops[-1].avg:.2f} ms")
        print(f"✓ Perda Final.......: {resultado.hops[-1].loss:.1f}%")

        if latency["hop"]:

            print(
                f"✓ Maior Δ RTT.......: "
                f"+{latency['maior_delta']:.2f} ms "
                f"(Hop {latency['hop'].numero})"
            )

        else:

            print(
                "✓ Maior Δ RTT.......: Não identificado"
            )

        #
        # Mostrar informações de perda somente quando
        # houver perda real de encaminhamento.
        #

        if loss.status == "ANOMALY" and loss.hop:

            print(
                f"✓ Primeira perda....: Hop {loss.hop.numero}"
            )

            print(
                f"✓ Perda persistente.: "
                f"{'Sim' if loss.persistent else 'Não'}"
            )

        if resultado.intermitencia:

            print("✓ Intermitência.....: Detectada")

            print(
                f"✓ Hop mais instável.: "
                f"{resultado.hop_mais_instavel}"
            )

            print(
                f"✓ Maior variação....: "
                f"{resultado.maior_variacao:.2f} ms"
            )

        else:

            print("✓ Intermitência.....: Não detectada")

    def _mostrar_conclusao(

        self,

        resultado,

        config,

        loss

    ):

        print()

        print("Conclusão")
        print("-" * 92)

        #
        # Diagnóstico de perda
        #

        if loss.diagnosis:

            print(f"• {loss.diagnosis}")

        if loss.recommendation:

            print(f"• {loss.recommendation}")

        #
        # Diagnósticos adicionais
        #

        for item in resultado.diagnosticos:

            print(f"• {item}")

        #
        # Intermitência
        #

        if resultado.intermitencia:

            print(
                f"• Foi detectada intermitência "
                f"no hop "
                f"{resultado.hop_mais_instavel}, "
                f"com variação máxima de "
                f"{resultado.maior_variacao:.2f} ms."
            )

        else:

            print(
                f"• As {config.execucoes} execuções "
                f"apresentaram comportamento consistente."
            )

    def _mostrar_estatisticas(

        self,

        config,

        ips_consultados,

        tempo

    ):

        print()

        print("Estatísticas")
        print("-" * 92)

        print(f"✓ Perfil............: {config.perfil}")
        print(f"✓ Execuções.........: {config.execucoes}")
        print(f"✓ Ciclos............: {config.ciclos}")
        print(
            f"✓ Amostras/Hop......: "
            f"{config.execucoes * config.ciclos}"
        )

        print(f"✓ IPs consultados...: {ips_consultados}")
        print(f"✓ Tempo total.......: {tempo:.2f} s")