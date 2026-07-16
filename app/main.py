from app.runners.analysis_runner import AnalysisRunner
from app.reports.report import Report
from app.utils.menu import Menu
from app.utils.analysis_configurator import AnalysisConfigurator
from app.utils.config_manager import ConfigManager
from app.exceptions.tool_error import ToolError


def main():

    runner = AnalysisRunner()

    report = Report()

    menu = Menu()

    configurator = AnalysisConfigurator()

    config_manager = ConfigManager()

    #
    # Última análise executada
    #

    ultima_analise = None

    while True:

        opcao = menu.show()

        #
        # Diagnóstico MTR
        #

        if opcao == "1":

            print()
            print("=" * 92)
            print("Diagnóstico MTR".center(92))
            print("=" * 92)
            print()

            print("Insira o destino da análise (IPv4 /32 ou domínio):")
            print()

            destino = input("> ").strip()

            if not destino:

                print()

                print("Destino inválido.")

                input("\nPressione ENTER para retornar ao menu...")

                continue

            print()

            config = config_manager.load()

            if config:

                usar = config_manager.ask(config)

                if not usar:

                    config = configurator.configure()

                    config_manager.save(config)

            else:

                config = configurator.configure()

                config_manager.save(config)

            print()

            print("Executando análise...\n")

            dados = runner.run(

                destino,

                config

            )

            if dados is None:

                print()

                print("Erro: não foi possível resolver o destino.")

                input("\nPressione ENTER para retornar ao menu...")

                continue

            report.show(

                resultado=dados["resultado"],

                config=config,

                latency=dados["latency"],

                loss=dados["loss"],

                tempo=dados["tempo"],

                ips_consultados=dados["ips_consultados"]

            )

            ultima_analise = {

                "tipo": "mtr",

                "dados": dados,

                "config": config

            }

        #
        # Diagnóstico de Aplicação
        #

        elif opcao == "2":

            from app.application.application_diagnostic import ApplicationDiagnostic

            resultado = ApplicationDiagnostic().execute()

            if resultado is not None:

                ultima_analise = resultado

        #
        # Exportar Relatório
        #

        elif opcao == "3":

            print()
            print("=" * 92)
            print("Exportar Relatório".center(92))
            print("=" * 92)
            print()

            if ultima_analise is None:

                print("Nenhum diagnóstico foi executado nesta sessão.")

                input("\nPressione ENTER para retornar ao menu...")

                continue

            #
            # Relatório MTR
            #

            if ultima_analise["tipo"] == "mtr":

                from app.exporters.pdf_exporter import PDFExporter

                arquivo = PDFExporter().export(

                    resultado=ultima_analise["dados"]["resultado"],

                    config=ultima_analise["config"],

                    latency=ultima_analise["dados"]["latency"],

                    loss=ultima_analise["dados"]["loss"],

                    tempo=ultima_analise["dados"]["tempo"],

                    ips_consultados=ultima_analise["dados"]["ips_consultados"]

                )

            #
            # Relatório Aplicação
            #

            elif ultima_analise["tipo"] == "application":

                from app.exporters.application_pdf_exporter import (

                    ApplicationPDFExporter

                )

                arquivo = ApplicationPDFExporter().export(

                    resultado=ultima_analise["resultado"],

                    responsabilidade=ultima_analise["responsabilidade"],

                    estatisticas=ultima_analise["estatisticas"]

                )

            else:

                print("Tipo de relatório desconhecido.")

                input("\nPressione ENTER para retornar ao menu...")

                continue

            print()

            print("=" * 92)
            print("Relatório exportado".center(92))
            print("=" * 92)
            print()

            print(f"Arquivo: {arquivo}")

            input("\nPressione ENTER para retornar ao menu...")

        #
        # Acessar Relatórios
        #

        elif opcao == "4":

            from app.utils.report_directory import ReportDirectory

            ReportDirectory().open()

        #
        # Sair
        #

        elif opcao == "0":

            print()

            print("Encerrando o RouteAnalyzer...")

            print()

            return

        else:

            print()

            print("Opção inválida.")

            input("\nPressione ENTER para continuar...")


if __name__ == "__main__":

    try:

        main()

    except KeyboardInterrupt:

        print()

        print("=" * 92)
        print("Investigação cancelada pelo usuário.".center(92))
        print("=" * 92)
        print()

    except ToolError as erro:

        print()

        print(str(erro))

        print()

        input("Pressione ENTER para retornar ao menu...")

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