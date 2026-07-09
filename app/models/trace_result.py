from dataclasses import dataclass, field
from typing import List

from app.models.hop import Hop

@dataclass
class TraceResult:

    #
    # Origem / Destino
    #

    origem: str

    destino: str

    destino_ip: str = ""

    destino_asn: str = ""

    destino_empresa: str = ""

    destino_pais: str = ""

    destino_prefixo: str = ""

    #
    # Hops
    #

    hops: List[Hop] = field(default_factory=list)

    #
    # Diagnóstico
    #

    diagnosticos: List[str] = field(default_factory=list)

    #
    # Estatísticas da comparação (Multi MTR)
    #

    intermitencia: bool = False

    maior_variacao: float = 0.0

    hop_mais_instavel: int = 0

    hops_instaveis: List[int] = field(default_factory=list)