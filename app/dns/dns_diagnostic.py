from concurrent.futures import ThreadPoolExecutor
from concurrent.futures import as_completed

from rich.console import Console
from rich.progress import Progress
from rich.progress import SpinnerColumn
from rich.progress import TextColumn

from app.dns.dns_database import DNS_DATABASE
from app.dns.dns_collector import DNSCollector
from app.dns.dns_analyzer import DNSAnalyzer
from app.dns.dns_table import DNSTable

console = Console()


class DNSDiagnostic:

    def execute(self):

        print()
        print("=" * 92)
        print("Diagnóstico DNS".center(92))
        print("=" * 92)
        print()

        #
        # Solicita o domínio
        #

        while True:

            dominio = input(
                "Informe o domínio que deseja consultar (ex.: google.com):\n\n> "
            ).strip().lower()

            if not dominio:

                print("\nDomínio não informado.\n")
                continue

            if "://" in dominio or "/" in dominio:

                print(
                    "\nInforme apenas o domínio (ex.: google.com).\n"
                )

                continue

            break

        print()

        collector = DNSCollector()

        resultados = []

        #
        # Consultas em paralelo
        #

        with Progress(

            SpinnerColumn(),

            TextColumn("[cyan]Consultando resolvedores DNS..."),

            transient=True,

            console=console

        ) as progress:

            progress.add_task("dns", total=None)

            with ThreadPoolExecutor(max_workers=8) as executor:

                futures = {

                    executor.submit(
                        collector.query,
                        dominio,
                        dns
                    ): dns

                    for dns in DNS_DATABASE

                }

                for future in as_completed(futures):

                    resultados.append(future.result())

        #
        # Mantém a ordem definida na base
        #

        resultados.sort(

            key=lambda r: next(

                indice

                for indice, dns in enumerate(DNS_DATABASE)

                if dns["nome"] == r.nome

            )

        )

        #
        # Análise
        #

        conclusoes = DNSAnalyzer().analyze(resultados)

        #
        # Tabela
        #

        print()

        print(f"Domínio consultado: {dominio}")

        print()

        DNSTable().show(resultados)

        #
        # Conclusão
        #

        print()

        print("Conclusão DNS")
        print("-" * 92)

        for conclusao in conclusoes:

            print(f"• {conclusao}")

        print()

        input("Pressione ENTER para voltar...")