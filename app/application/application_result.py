from dataclasses import dataclass
from typing import Optional


@dataclass
class ApplicationResult:

    #
    # Execução
    #

    execucao: int = 0

    sucesso: bool = False

    erro: str = ""

    #
    # URL
    #

    url: str = ""

    dominio: str = ""

    #
    # Rede
    #

    ip: str = ""

    asn: str = ""

    empresa: str = ""

    #
    # Infraestrutura
    #

    infraestrutura: str = ""

    tecnologia: str = ""

    #
    # Fingerprint
    #

    fabricante: str = ""

    produto: str = ""

    categoria: str = ""

    #
    # HTTP
    #

    http_code: int = 0

    http_version: str = ""

    server: str = ""

    content_type: str = ""

    #
    # Redirect
    #

    redirect: bool = False

    redirects: int = 0

    location: str = ""

    #
    # Resultado após seguir o redirect (quando existir)
    #

    redirect_result: Optional["ApplicationResult"] = None

    #
    # TLS
    #

    tls_version: str = ""

    cipher: str = ""

    #
    # Tempos por etapa
    #

    dns_time: float = 0.0

    tcp_time: float = 0.0

    tls_time: float = 0.0

    application_time: float = 0.0

    transfer_time: float = 0.0

    total_time: float = 0.0

    #
    # Compatibilidade
    #

    ttfb: float = 0.0

    #
    # Resultado bruto
    #

    curl_exit_code: int = 0

    stderr: str = ""

    stdout: str = ""

    #
    # Headers HTTP
    #

    headers: dict = None

    #
    # Retorna o último resultado da cadeia de redirecionamentos
    #

    def get_final(

        self

    ):

        atual = self

        while atual.redirect_result is not None:

            atual = atual.redirect_result

        return atual