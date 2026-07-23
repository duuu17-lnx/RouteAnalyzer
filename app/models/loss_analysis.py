from dataclasses import dataclass, field
from typing import Optional

from app.models.hop import Hop


@dataclass
class LossAnalysis:

    #
    # Primeira perda observada
    #

    first_loss: Optional[Hop] = None

    #
    # Primeira perda considerada relevante
    # (>= 2%)
    #

    first_relevant_loss: Optional[Hop] = None

    #
    # Primeira perda considerada persistente
    #

    first_persistent_loss: Optional[Hop] = None

    #
    # Hop escolhido como origem mais provável da perda
    #

    hop: Optional[Hop] = None

    #
    # A perda permaneceu até o destino?
    #

    persistent: bool = False

    #
    # Quantidade estimada de pacotes perdidos
    #

    lost_packets: int = 0

    #
    # Pontuação da análise
    #

    score: int = 0

    #
    # Grau de confiança
    #

    confidence: str = "Baixa"

    #
    # Evidências utilizadas
    #

    evidencias: list[str] = field(default_factory=list)

    #
    # Status da correlação
    #
    # Valores esperados:
    #
    #   NO_ANOMALY
    #   ANOMALY
    #   INCONCLUSIVE
    #

    status: str = "NO_ANOMALY"

    #
    # Diagnóstico final da análise
    #

    diagnosis: str = ""

    #
    # Recomendação operacional
    #

    recommendation: Optional[str] = None