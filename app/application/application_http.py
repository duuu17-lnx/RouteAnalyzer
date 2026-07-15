import subprocess
from urllib.parse import urlparse

from app.application.application_result import ApplicationResult
from app.application.infrastructure_detector import InfrastructureDetector
from app.application.fingerprint_detector import FingerprintDetector


class ApplicationHTTP:

    def execute(self, url: str):

        #
        # Completa https automaticamente
        #

        if not url.startswith(("http://", "https://")):

            url = "https://" + url

        resultado = ApplicationResult()

        resultado.url = url

        resultado.dominio = urlparse(url).hostname or ""

        #
        # Informações retornadas pelo curl
        #

        write_out = (

            "\nRA_HTTP_CODE:%{http_code}"

            "\nRA_REMOTE_IP:%{remote_ip}"

            "\nRA_HTTP_VERSION:%{http_version}"

            "\nRA_NUM_REDIRECTS:%{num_redirects}"

            "\nRA_TIME_NAMLOOKUP:%{time_namelookup}"

            "\nRA_TIME_CONNECT:%{time_connect}"

            "\nRA_TIME_APPCONNECT:%{time_appconnect}"

            "\nRA_TIME_STARTTRANSFER:%{time_starttransfer}"

            "\nRA_TIME_TOTAL:%{time_total}"

            "\nRA_REDIRECT_URL:%{redirect_url}"

        )

        #
        # Uma única requisição HTTP
        # Não segue redirects.
        #

        comando = [

            "curl.exe",

            "--max-redirs",

            "0",

            "-sS",

            "--connect-timeout",

            "5",

            "--max-time",

            "15",

            "-D",

            "-",

            "-o",

            "NUL",

            "-w",

            write_out,

            url

        ]

        processo = subprocess.run(

            comando,

            capture_output=True,

            text=True,

            encoding="utf-8",

            errors="ignore"

        )

        resultado.curl_exit_code = processo.returncode

        resultado.stdout = processo.stdout

        resultado.stderr = processo.stderr

        #
        # Situação
        #

        resultado.sucesso = (

            processo.returncode == 0

        )

        if not resultado.sucesso:

            codigo = processo.returncode

            if codigo == 6:

                resultado.erro = "DNS"

            elif codigo == 7:

                resultado.erro = "TCP"

            elif codigo == 28:

                resultado.erro = "Timeout"

            elif codigo == 35:

                resultado.erro = "TLS"

            else:

                resultado.erro = f"CURL {codigo}"

        #
        # Parse dos headers
        #

        resultado.headers = {}

        lendo_headers = True

        dns = 0.0

        connect = 0.0

        appconnect = 0.0

        starttransfer = 0.0

        total = 0.0

        for linha in processo.stdout.splitlines():

            linha = linha.strip()

            if lendo_headers:

                if linha == "":

                    continue

                if linha.startswith("RA_"):

                    lendo_headers = False

                elif ":" in linha:

                    chave, valor = linha.split(":", 1)

                    resultado.headers[

                        chave.strip().lower()

                    ] = valor.strip()

                    continue

            if not linha.startswith("RA_"):

                continue

            chave, valor = linha.split(":", 1)

            valor = valor.strip()

            try:

                if chave == "RA_HTTP_CODE":

                    resultado.http_code = int(valor)
                elif chave == "RA_REMOTE_IP":

                    resultado.ip = valor

                elif chave == "RA_HTTP_VERSION":

                    resultado.http_version = valor

                elif chave == "RA_NUM_REDIRECTS":

                    resultado.redirects = int(valor)

                    resultado.redirect = resultado.redirects > 0

                elif chave == "RA_TIME_NAMLOOKUP":

                    dns = float(valor) * 1000

                elif chave == "RA_TIME_CONNECT":

                    connect = float(valor) * 1000

                elif chave == "RA_TIME_APPCONNECT":

                    appconnect = float(valor) * 1000

                elif chave == "RA_TIME_STARTTRANSFER":

                    starttransfer = float(valor) * 1000

                elif chave == "RA_TIME_TOTAL":

                    total = float(valor) * 1000

                elif chave == "RA_REDIRECT_URL":

                    resultado.location = valor

            except Exception:

                pass

        #
        # Converte tempos acumulados em tempos individuais
        #

        if resultado.sucesso:

            resultado.dns_time = round(

                dns,

                2

            )

            resultado.tcp_time = round(

                max(

                    0.0,

                    connect - dns

                ),

                2

            )

            resultado.tls_time = round(

                max(

                    0.0,

                    appconnect - connect

                ),

                2

            )

            resultado.application_time = round(

                max(

                    0.0,

                    starttransfer - appconnect

                ),

                2

            )

            resultado.transfer_time = round(

                max(

                    0.0,

                    total - starttransfer

                ),

                2

            )

            resultado.ttfb = round(

                starttransfer,

                2

            )

            resultado.total_time = round(

                total,

                2

            )

        else:

            resultado.dns_time = 0.0

            resultado.tcp_time = 0.0

            resultado.tls_time = 0.0

            resultado.application_time = 0.0

            resultado.transfer_time = 0.0

            resultado.ttfb = 0.0

            resultado.total_time = 0.0

        #
        # Headers conhecidos
        #

        resultado.server = resultado.headers.get(

            "server",

            ""

        )

        resultado.content_type = resultado.headers.get(

            "content-type",

            ""

        )

        if not resultado.location:

            resultado.location = resultado.headers.get(

                "location",

                ""

            )
        #
        # Detecta infraestrutura
        #

        infraestrutura = InfrastructureDetector()

        resultado.infraestrutura, resultado.tecnologia = infraestrutura.detect(

            resultado.headers

        )

        #
        # Fingerprint da plataforma
        #

        fingerprint = FingerprintDetector().detect(

            resultado.headers

        )

        if fingerprint:

            resultado.fabricante = fingerprint["fabricante"]

            resultado.produto = fingerprint["produto"]

            resultado.categoria = fingerprint["categoria"]

        #
        # Alguns servidores não enviam redirect_url no write-out,
        # mas enviam o header Location.
        #

        if (

            not resultado.location

            and

            "location" in resultado.headers

        ):

            resultado.location = resultado.headers["location"]

        #
        # Considera redirect apenas quando existe Location e
        # o código HTTP pertence à família 3xx.
        #

        if (

            resultado.http_code >= 300

            and

            resultado.http_code < 400

            and

            resultado.location

        ):

            resultado.redirect = True

            if resultado.redirects == 0:

                resultado.redirects = 1

        else:

            resultado.redirect = False

        return resultado