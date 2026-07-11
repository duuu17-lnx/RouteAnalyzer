from app.models.analysis_config import AnalysisConfig


class AnalysisConfigurator:

    def configure(self):

        print()
        print("=" * 92)
        print("Configuração da Análise".center(92))
        print("=" * 92)
        print()

        config = AnalysisConfig()

        print("Selecione o tipo de análise")
        print()

        print("[1] Rápida")
        print("    Ideal para validação rápida de conectividade.")
        print("    2 execuções • 30 ciclos")
        print()

        print("[2] Padrão")
        print("    Equilíbrio entre velocidade e confiabilidade.")
        print("    3 execuções • 80 ciclos")
        print()

        print("[3] Avançada")
        print("    Indicada para investigação de perda, latência e intermitência.")
        print("    5 execuções • 300 ciclos")
        print("    Pode levar vários minutos para ser concluída.")
        print()

        print("[4] Personalizada")
        print("    Defina manualmente o número de execuções e ciclos.")
        print()

        while True:

            opcao = input(

                "Informe a opção desejada\n"
                "(Pressione ENTER para utilizar o perfil Padrão)\n\n"
                "> "

            ).strip()

            if opcao == "":

                config.perfil = "Padrão"
                config.execucoes = 3
                config.ciclos = 80

                break

            if opcao == "1":

                config.perfil = "Rápida"
                config.execucoes = 2
                config.ciclos = 30

                break

            if opcao == "2":

                config.perfil = "Padrão"
                config.execucoes = 3
                config.ciclos = 80

                break

            if opcao == "3":

                config.perfil = "Avançada"
                config.execucoes = 5
                config.ciclos = 300

                break

            if opcao == "4":

                config = self._custom()

                break

            print("\nOpção inválida. Informe uma opção entre 1 e 4.\n")

        self._resume(config)

        while True:

            confirmar = input(

                "\nIniciar coleta? [S/n]: "

            ).strip().lower()

            if confirmar in ("", "s", "sim"):

                return config

            if confirmar in ("n", "nao", "não"):

                print()

                return self.configure()

            print("\nResposta inválida. Informe S ou N.")

    def _custom(self):

        config = AnalysisConfig()

        config.perfil = "Personalizada"

        print()
        print("=" * 92)
        print("Configuração Personalizada".center(92))
        print("=" * 92)
        print()

        while True:

            valor = input(

                "Número de execuções [3]: "

            ).strip()

            if valor == "":

                config.execucoes = 3

                break

            if valor.isdigit():

                valor = int(valor)

                if 1 <= valor <= 20:

                    config.execucoes = valor

                    break

            print("Valor inválido. Informe um número entre 1 e 20.\n")

        while True:

            valor = input(

                "Número de ciclos por execução [80]: "

            ).strip()

            if valor == "":

                config.ciclos = 80

                break

            if valor.isdigit():

                valor = int(valor)

                if 10 <= valor <= 5000:

                    config.ciclos = valor

                    break

            print("Valor inválido. Informe um número entre 10 e 5000.\n")

        return config

    def _resume(self, config):

        print()
        print("-" * 92)
        print("Resumo da coleta")
        print("-" * 92)
        print()

        amostras = config.execucoes * config.ciclos

        #
        # Qualidade da amostragem
        #

        if amostras <= 100:

            qualidade = "Baixa"

        elif amostras <= 300:

            qualidade = "Moderada"

        elif amostras <= 1000:

            qualidade = "Alta"

        elif amostras <= 3000:

            qualidade = "Muito Alta"

        else:

            qualidade = "Máxima"

        #
        # Tempo estimado
        #

        if amostras <= 100:

            estimativa = "Menos de 2 minutos"

        elif amostras <= 250:

            estimativa = "Entre 2 e 5 minutos"

        elif amostras <= 600:

            estimativa = "Entre 5 e 10 minutos"

        elif amostras <= 1500:

            estimativa = "Entre 10 e 20 minutos"

        elif amostras <= 3000:

            estimativa = "Entre 20 e 40 minutos"

        else:

            estimativa = "Superior a 40 minutos"

        print(f"Perfil................: {config.perfil}")
        print(f"Execuções............: {config.execucoes}")
        print(f"Ciclos por execução..: {config.ciclos}")
        print(f"Amostras por hop.....: {amostras}")
        print(f"Qualidade............: {qualidade}")
        print(f"Tempo estimado.......: {estimativa}")

        print()
        print(
            "* O tempo pode variar conforme a quantidade de hops,\n"
            "  perda de pacotes, desempenho do sistema e sistema operacional."
        )

        print()