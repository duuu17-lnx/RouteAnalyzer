from app.models.loss_event import LossEvent


class LossEventDetector:
    """
    Detecta eventos de perda persistente.

    Um evento representa um conjunto contínuo de hops com perda real.

    Pequenas interrupções (1 hop sem perda) são toleradas para evitar
    fragmentar eventos causados por respostas ICMP inconsistentes.
    """

    MAX_GAP = 1

    def detect(self, trace):

        eventos = []

        hops = trace.hops

        atual = None

        gap = 0

        for hop in hops:

            possui_perda = hop.perda_real and hop.loss > 0

            #
            # Início do evento
            #

            if atual is None:

                if possui_perda:

                    atual = LossEvent()

                    atual.start_hop = hop

                    atual.end_hop = hop

                    atual.hops.append(hop)

                continue

            #
            # Continuação normal
            #

            if possui_perda:

                atual.end_hop = hop

                atual.hops.append(hop)

                gap = 0

                continue

            #
            # Pequena interrupção
            #

            gap += 1

            if gap <= self.MAX_GAP:

                continue

            #
            # Finaliza o evento
            #

            self._finalize(atual)

            eventos.append(atual)

            atual = None

            gap = 0

        #
        # Último evento
        #

        if atual is not None:

            self._finalize(atual)

            eventos.append(atual)

        return eventos

    def _finalize(self, event):

        event.total_hops = len(event.hops)

        if event.hops:

            losses = [hop.loss for hop in event.hops]

            event.max_loss = max(losses)

            event.avg_loss = sum(losses) / len(losses)

        else:

            event.max_loss = 0

            event.avg_loss = 0

        event.persistent = event.total_hops > 1