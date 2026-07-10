from dataclasses import dataclass


@dataclass
class DNSResult:

    origem: str = ""

    nome: str = ""

    servidor: str = ""

    tempo: float = 0.0

    status: str = ""

    resposta: str = ""

    erro: str = ""