from app.runners.analysis_runner import AnalysisRunner
from app.reports.report import Report
from app.utils.menu import Menu


def main():

    runner = AnalysisRunner()

    report = Report()

    menu = Menu()

    while True:

        print("\nExecutando análise...\n")

        destino = input("Destino: ").strip()

        dados = runner.run(destino)

        if dados is None:

            print("\nErro: não foi possível resolver o destino.")

            continue

        report.show(

            resultado=dados["resultado"],

            quantidade_mtr=dados["quantidade_mtr"],

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

                try:

                    from app.dns.dns_diagnostic import DNSDiagnostic

                    DNSDiagnostic().execute()

                except ImportError:

                    print("\nDiagnóstico DNS ainda não implementado.")

                input("\nPressione ENTER para voltar ao menu...")

            #
            # Exportação
            #

            elif opcao == "3":

                print("\nExportação ainda não implementada.")

                input("\nPressione ENTER para voltar ao menu...")

            #
            # Sair
            #

            elif opcao == "0":

                print("\nEncerrando RouteAnalyzer...\n")

                return

            else:

                print("\nOpção inválida.")

                input("\nPressione ENTER...")


if __name__ == "__main__":

    main()