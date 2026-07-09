from rich.console import Console
from rich.table import Table

console = Console()


def mostrar_hops(hops):

    tabela = Table(
        title="RouteAnalyzer",
        show_lines=False
    )

    tabela.add_column("Hop", justify="center", style="cyan", no_wrap=True)
    tabela.add_column("Host", style="white")
    tabela.add_column("Loss%", justify="right")
    tabela.add_column("Avg", justify="right")
    tabela.add_column("Δ RTT", justify="right")
    tabela.add_column("ASN", style="cyan")
    tabela.add_column("Evento", style="green")
    tabela.add_column("Observação", style="yellow")

    for hop in hops:

        if hop.loss == 0:
            cor_loss = "green"
        elif hop.loss <= 5:
            cor_loss = "yellow"
        else:
            cor_loss = "red"

        if hop.avg < 20:
            cor_avg = "green"
        elif hop.avg < 70:
            cor_avg = "yellow"
        else:
            cor_avg = "red"

        if hop.delta_rtt == 0:
            delta = "--"
        else:
            delta = f"{hop.delta_rtt:+.2f}"

        if hop.asn:
            asn = f"{hop.asn}\n{hop.empresa}"
        else:
            asn = "-"

        tabela.add_row(
            str(hop.numero),
            hop.host,
            f"[{cor_loss}]{hop.loss:.1f}%[/{cor_loss}]",
            f"[{cor_avg}]{hop.avg:.2f}[/{cor_avg}]",
            delta,
            asn,
            hop.evento,
            hop.observacao
        )

    console.print(tabela)