from dataclasses import dataclass, field

from app.models.hop import Hop


@dataclass
class LossEvent:
    """
    Representa um evento contínuo de perda de pacotes.

    Um evento é composto por um ou mais hops consecutivos com perda
    persistente. O detector é responsável por montar este objeto; ele
    não contém nenhuma regra de negócio.
    """

    start_hop: Hop | None = None

    end_hop: Hop | None = None

    hops: list[Hop] = field(default_factory=list)

    total_hops: int = 0

    avg_loss: float = 0.0

    max_loss: float = 0.0

    persistent: bool = False

    @property
    def first_index(self) -> int | None:
        if self.start_hop:
            return self.start_hop.index
        return None

    @property
    def last_index(self) -> int | None:
        if self.end_hop:
            return self.end_hop.index
        return None

    @property
    def duration(self) -> int:
        return self.total_hops

    @property
    def is_single_hop(self) -> bool:
        return self.total_hops == 1

    @property
    def is_multi_hop(self) -> bool:
        return self.total_hops > 1

    def __len__(self):
        return self.total_hops

    def __bool__(self):
        return self.total_hops > 0

    def __str__(self):

        if self.start_hop is None:
            return "LossEvent(vazio)"

        if self.start_hop == self.end_hop:
            return f"Hop {self.start_hop.index}"

        return (
            f"Hops {self.start_hop.index}"
            f" → {self.end_hop.index}"
        )