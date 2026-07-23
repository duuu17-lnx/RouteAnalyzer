from app.models.candidate import Candidate
from app.models.loss_event import LossEvent


class CandidateBuilder:
    """
    Constrói candidatos a partir dos eventos de perda.

    Cada evento gera exatamente um Candidate, cujo hop
    representativo é o primeiro hop do evento.
    """

    def build(self, trace, event: LossEvent, index: int) -> Candidate:

        start = event.start_hop

        hops = trace.hops

        previous_hop = None
        next_hop = None

        previous_hops = []
        next_hops = []

        for hop in hops:

            if hop.numero < start.numero:
                previous_hops.append(hop)

            elif hop.numero > start.numero:
                next_hops.append(hop)

        if previous_hops:
            previous_hop = previous_hops[-1]

        if next_hops:
            next_hop = next_hops[0]

        return Candidate(

            event=event,

            index=index,

            start_hop=event.start_hop,

            end_hop=event.end_hop,

            previous_hop=previous_hop,

            next_hop=next_hop,

            previous_hops=previous_hops,

            next_hops=next_hops

        )

    def build_all(self, trace, events: list[LossEvent]) -> list[Candidate]:

        candidates = []

        for index, event in enumerate(events):

            candidates.append(

                self.build(
                    trace=trace,
                    event=event,
                    index=index
                )

            )

        return candidates