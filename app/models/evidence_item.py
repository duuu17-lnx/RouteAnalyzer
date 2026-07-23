
from dataclasses import dataclass


@dataclass
class EvidenceItem:
    """
    Representa uma evidência utilizada durante uma análise.
    """

    description: str
    points: int