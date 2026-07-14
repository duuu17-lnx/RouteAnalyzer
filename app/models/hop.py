from dataclasses import dataclass, field


@dataclass
class Hop:

    #
    # Identificação
    #

    numero: int

    host: str

    ip: str = ""

    hostname: str = ""

    #
    # Informações de Rede
    #

    asn: str = ""

    empresa: str = ""

    prefixo: str = ""

    pais: str = ""

    cidade: str = ""

    localizacao: str = ""

    #
    # Classificação
    #

    tipo: str = ""

    evento: str = ""

    observacao: str = ""

    #
    # Análise ICMP
    #

    perda_real: bool = True

    icmp_filtrado: bool = False

    motivo_icmp: str = ""

    #
    # Estatísticas do MTR
    #

    delta_rtt: float = 0.0

    tracert_avg: float = 0.0

    loss: float = 0.0

    sent: int = 0

    last: float = 0.0

    avg: float = 0.0

    best: float = 0.0

    worst: float = 0.0

    stdev: float = 0.0

    #
    # Comparação entre múltiplos MTRs
    #

    rtts: list[float] = field(default_factory=list)

    variacao_execucoes: float = 0.0