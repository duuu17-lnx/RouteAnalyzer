from rich.console import Console
from rich.table import Table

from app.application.application_diagnosis import ApplicationDiagnosis
from app.application.performance_analyzer import PerformanceAnalyzer

console = Console()


class ApplicationTable:

    def show(

        self,

        resultado,

        responsabilidade,

        conclusoes,

        estatisticas

    ):

        #
        # Resultado efetivo da requisição
        #

        ultimo = resultado.get_final()

        print()

        print("=" * 92)
        print("Diagnóstico de Aplicação".center(92))
        print("=" * 92)
        print()

        tabela = Table()

        tabela.add_column(

            "Campo",

            style="cyan"

        )

        tabela.add_column(

            "Valor"

        )

        http_status = {

            200: "OK",
            201: "Created",
            202: "Accepted",

            301: "Moved Permanently",
            302: "Found",
            303: "See Other",
            307: "Temporary Redirect",
            308: "Permanent Redirect",

            400: "Bad Request",
            401: "Unauthorized",
            403: "Forbidden",
            404: "Not Found",
            408: "Request Timeout",
            429: "Too Many Requests",

            500: "Internal Server Error",
            502: "Bad Gateway",
            503: "Service Unavailable",
            504: "Gateway Timeout"

        }

        #
        # URL ORIGINAL
        #

        tabela.add_row(

            "URL",

            resultado.url

        )

        #
        # Cadeia de Redirect
        #

        if resultado.redirect:

            tabela.add_row(

                "Redirecionamentos",

                str(

                    resultado.redirects

                )

            )

            if resultado.location:

                tabela.add_row(

                    "Location",

                    resultado.location

                )

        #
        # Destino Final
        #

        if ultimo is not resultado:

            tabela.add_row(

                "Destino Final",

                ultimo.url

            )

        #
        # IP
        #

        if ultimo is resultado:

            tabela.add_row(

                "IP",

                resultado.ip or "--"

            )

        else:

            tabela.add_row(

                "IP Original",

                resultado.ip or "--"

            )

            tabela.add_row(

                "IP Final",

                ultimo.ip or "--"

            )

        #
        # HTTP ORIGINAL
        #

        if resultado.http_code:

            texto = str(

                resultado.http_code

            )

            descricao = http_status.get(

                resultado.http_code,

                ""

            )

            if descricao:

                texto += f" {descricao}"

        else:

            texto = "--"

        if ultimo is resultado:

            tabela.add_row(

                "HTTP",

                texto

            )

        else:

            tabela.add_row(

                "HTTP Original",

                texto

            )

        #
        # HTTP FINAL
        #

        if ultimo is not resultado:

            if ultimo.http_code:

                texto = str(

                    ultimo.http_code

                )

                descricao = http_status.get(

                    ultimo.http_code,

                    ""

                )

                if descricao:

                    texto += f" {descricao}"

            else:

                texto = "--"

            tabela.add_row(

                "HTTP Final",

                texto

            )

        #
        # Versão HTTP
        #

        if ultimo.http_version:

            tabela.add_row(

                "Versão HTTP",

                f"HTTP/{ultimo.http_version}"

            )

        else:

            tabela.add_row(

                "Versão HTTP",

                "--"

            )

        #
        # Servidor
        #

        tabela.add_row(

            "Servidor",

            ultimo.server or "--"

        )

        tabela.add_row(

            "Infraestrutura",

            ultimo.infraestrutura or "--"

        )

        tabela.add_row(

            "Tecnologia",

            ultimo.tecnologia or "--"

        )

        tabela.add_row(

            "Fabricante",

            ultimo.fabricante or "--"

        )

        tabela.add_row(

            "Produto",

            ultimo.produto or "--"

        )

        tabela.add_row(

            "Categoria",

            ultimo.categoria or "--"

        )

        tabela.add_row(

            "Content-Type",

            ultimo.content_type or "--"

        )

        #
        # Exibe a tabela
        #

        console.print(

            tabela

        )
        #
        # Responsabilidade
        #

        print()

        print("Responsabilidade")

        print("-" * 92)

        for item, status in responsabilidade.items():

            if status in (

                "OK",
                "Redirect"

            ):

                simbolo = "✓"

            elif status in (

                "Não avaliada",
                "Não aplicável",
                "Não testado",
                "Não testada"

            ):

                simbolo = "•"

            else:

                simbolo = "✗"

            print(

                f"{simbolo} {item:<20} {status}"

            )

        #
        # Estatísticas
        #

        print()

        print("Estatísticas das Execuções")

        print("-" * 92)

        print(

            f"Execuções...............: {estatisticas['execucoes']}"

        )

        print(

            f"Válidas.................: {estatisticas['validas']}"

        )

        print(

            f"Falhas..................: {estatisticas['falhas']}"

        )

        if estatisticas["intermitencia"] is None:

            texto = "Não avaliada"

        elif estatisticas["intermitencia"]:

            texto = "Sim"

        else:

            texto = "Não"

        print(

            f"Intermitência...........: {texto}"

        )

        print()

        #
        # Distribuição HTTP (Original)
        #

        print(

            "Distribuição HTTP (Original)"

        )

        if estatisticas["http_original"]:

            for codigo, quantidade in sorted(

                estatisticas["http_original"].items()

            ):

                descricao = http_status.get(

                    codigo,

                    ""

                )

                texto = f"HTTP {codigo}"

                if descricao:

                    texto += f" {descricao}"

                print(

                    f"{texto:<42}: {quantidade}"

                )

        else:

            print(

                "Nenhuma resposta HTTP válida foi obtida."

            )

        #
        # Distribuição HTTP (Destino Final)
        #

        if estatisticas["http_final"]:

            print()

            print(

                "Distribuição HTTP (Destino Final)"

            )

            for codigo, quantidade in sorted(

                estatisticas["http_final"].items()

            ):

                descricao = http_status.get(

                    codigo,

                    ""

                )

                texto = f"HTTP {codigo}"

                if descricao:

                    texto += f" {descricao}"

                print(

                    f"{texto:<42}: {quantidade}"

                )

        #
        # Médias
        #
        # Temporariamente ocultadas.
        # Serão reativadas na versão 2.0 após a
        # implementação do resultado_final.
        #
        #
        # Diagnóstico
        #

        print()

        print(

            "Diagnóstico Final"

        )

        print(

            "-" * 92

        )

        diagnostico = ApplicationDiagnosis().build(

            resultado,

            responsabilidade,

            estatisticas

        )

        for linha in diagnostico:

            print(

                f"• {linha}"

            )

        #
        # Análise de desempenho
        #

        if estatisticas["validas"] > 0:

            performance = PerformanceAnalyzer().analyze(

                ultimo

            )

            if performance:

                print()

                print(

                    "Análise de Desempenho"

                )

                print(

                    "-" * 92

                )

                print(

                    f"• A maior parte do tempo da requisição foi consumida durante {performance['etapa'].lower()} ({performance['percentual']:.1f}%)."

                )

                print()

                if resultado.redirect:

                    print(

                        "• A análise de desempenho considera o recurso final obtido após todos os redirecionamentos HTTP."

                    )

                    print()

                print(

                    "• Os testes realizados não indicam limitação de conectividade entre a estação e o servidor remoto."

                )

        print()