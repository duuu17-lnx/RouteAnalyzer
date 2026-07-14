from app.runners.analysis_runner import AnalysisRunner
from app.reports.report import Report
from app.utils.menu import Menu
from app.utils.analysis_configurator import AnalysisConfigurator
from app.utils.config_manager import ConfigManager


def main():

    runner = AnalysisRunner()

    report = Report()

    menu = Menu()

    configurator = AnalysisConfigurator()

    config_manager = ConfigManager()

    while True:

        print()

        print("=" * 92)
        print("RouteAnalyzer".center(92))
        print("=" * 92)
        print()

        print("Insira o destino da análise (IPv4 /32 ou domínio):")
        print()

        destino = input("> ").strip()

        if not destino:

            print("\nDestino inválido.\n")

            continue

        print()

        #
        # Última configuração utilizada
        #

        config = config_manager.load()

        if config:

            usar = config_manager.ask(config)

            if not usar:

                config = configurator.configure()

                config_manager.save(config)

        else:

            config = configurator.configure()

            config_manager.save(config)

        print("\nExecutando análise...\n")

        dados = runner.run(

            destino,

            config

        )

        if dados is None:

            print("\nErro: não foi possível resolver o destino.")

            continue

        report.show(

            resultado=dados["resultado"],

            config=config,

            latency=dados["latency"],

            loss=dados["loss"],

            tempo=dados["tempo"],

            ips_consultados=dados["ips_consultados"]

        )

        #
        # Menu principal
        #

        while True:

            opcao = menu.show()

            #
            # Nova análise
            #

            if opcao == "1":

                print()

                break

            #
            # Diagnóstico DNS
            #

            elif opcao == "2":

                from app.dns.dns_diagnostic import DNSDiagnostic

                DNSDiagnostic().execute()

            #
            # Exportação
            #

            elif opcao == "3":

                from app.exporters.pdf_exporter import PDFExporter

                arquivo = PDFExporter().export(

                    resultado=dados["resultado"],

                    config=config,

                    latency=dados["latency"],

                    loss=dados["loss"],

                    tempo=dados["tempo"],

                    ips_consultados=dados["ips_consultados"]

                )

                print()

                print("=" * 92)
                print("Relatório exportado".center(92))
                print("=" * 92)
                print()

                print(f"Arquivo: {arquivo}")

                input("\nPressione ENTER para voltar ao menu...")

            #
            # Sair
            #

            elif opcao == "0":

                print("\nEncerrando o RouteAnalyzer...\n")

                return

            else:

                print("\nOpção inválida.")

                input("\nPressione ENTER...")


if __name__ == "__main__":

    try:

        main()

    except KeyboardInterrupt:

        print()

        print("=" * 92)
        print("Investigação cancelada pelo usuário.".center(92))
        print("=" * 92)
        print()

    except Exception:

        import traceback

        print()

        print("=" * 92)
        print("ERRO INESPERADO".center(92))
        print("=" * 92)
        print()

        traceback.print_exc()

        print()

        input("Pressione ENTER para encerrar...")