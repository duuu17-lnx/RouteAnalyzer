from dataclasses import dataclass, field
from typing import Optional

from app.models.hop import Hop
from app.models.loss_event import LossEvent


@dataclass
class Candidate:
    """
    Representa um candidato à origem de um problema.

    Atualmente um candidato é construído a partir de um LossEvent,
    mas o modelo é genérico o suficiente para ser reutilizado por
    outros analisadores no futuro.
    """

    event: LossEvent

    index: int

    start_hop: Hop

    end_hop: Hop

    previous_hop: Optional[Hop] = None

    next_hop: Optional[Hop] = None

    previous_hops: list[Hop] = field(default_factory=list)

    next_hops: list[Hop] = field(default_factory=list)

    @property
    def hop(self) -> Hop:
        """
        Compatibilidade com o código existente.

        O hop representativo do candidato é sempre o primeiro hop
        do evento.
        """
        return self.start_hop

    @property
    def is_first(self) -> bool:
        return self.previous_hop is None

    @property
    def is_last(self) -> bool:
        return self.next_hop is None

    @property
    def remaining_hops(self) -> int:
        return len(self.next_hops)

    @property
    def distance_to_destination(self) -> int:
        return len(self.next_hops)

    @property
    def event_size(self) -> int:
        return self.event.total_hops

    @property
    def persistent(self) -> bool:
        return self.event.persistent

    @property
    def average_loss(self) -> float:
        return self.event.avg_loss

    @property
    def maximum_loss(self) -> float:
        return self.event.max_loss

    def __str__(self):

        return (
            f"Candidate("
            f"hop={self.start_hop.index}, "
            f"event={self.event.total_hops} hops)"
        )