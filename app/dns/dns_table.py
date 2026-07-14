from rich.console import Console
from rich.table import Table

console = Console()


class DNSTable:

    def show(self, resultados):

        tabela = Table(title="Diagnóstico DNS")

        tabela.add_column("Origem")
        tabela.add_column("Resolvedor")
        tabela.add_column("Servidor")
        tabela.add_column("Tempo", justify="right")
        tabela.add_column("Status")
        tabela.add_column("Resposta")

        for dns in resultados:

            if dns.status == "Excelente":

                cor = "green"

            elif dns.status == "Muito Bom":

                cor = "bright_green"

            elif dns.status == "Bom":

                cor = "cyan"

            elif dns.status == "Normal":

                cor = "yellow"

            elif dns.status == "Elevado":

                cor = "bright_yellow"

            else:

                cor = "red"

            tabela.add_row(

                dns.origem,

                dns.nome,

                dns.servidor,

                f"{dns.tempo:.2f} ms" if dns.tempo else "--",

                f"[{cor}]{dns.status}[/{cor}]",

                dns.resposta

            )

        console.print(tabela)