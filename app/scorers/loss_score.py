from app.models.score_result import ScoreResult


class LossScore:

    def calculate(self, trace, candidate):

        result = ScoreResult()

        self._score_real_loss(result, candidate)
        self._score_persistent_event(result, candidate)
        self._score_destination(result, trace, candidate)
        self._score_continuity(result, candidate)
        self._score_average_loss(result, candidate)
        self._score_peak_loss(result, candidate)
        self._score_event_length(result, candidate)
        self._score_icmp(result, candidate)
        self._score_isolated(result, candidate)

        #
        # Nunca permitir score negativo.
        #

        result.score = max(0, result.score)

        return result

    #
    # ------------------------------------------------------------------
    # Evidências positivas
    # ------------------------------------------------------------------
    #

    def _score_real_loss(self, result, candidate):

        if candidate.start_hop.perda_real:

            result.add(
                "O evento iniciou com perda real.",
                10
            )

    def _score_persistent_event(self, result, candidate):

        if candidate.event.persistent:

            result.add(
                "O evento apresentou perda persistente.",
                15
            )

    def _score_destination(self, result, trace, candidate):

        ultimo = trace.hops[-1]

        if (
            ultimo.perda_real
            and ultimo.loss > 0
            and ultimo.loss >= candidate.event.avg_loss
        ):

            result.add(
                "A perda permaneceu até o destino.",
                15
            )

    def _score_continuity(self, result, candidate):

        if not candidate.next_hops:
            return

        total = 0
        com_perda = 0

        for hop in candidate.next_hops:

            if hop.icmp_filtrado:
                continue

            total += 1

            if hop.perda_real and hop.loss > 0:
                com_perda += 1

        if total == 0:
            return

        continuidade = com_perda / total

        if continuidade >= 0.90:

            result.add(
                "A perda persistiu em praticamente toda a rota.",
                25
            )

        elif continuidade >= 0.75:

            result.add(
                "A perda apresentou alta continuidade.",
                20
            )

        elif continuidade >= 0.50:

            result.add(
                "A perda apresentou continuidade moderada.",
                15
            )

        elif continuidade >= 0.30:

            result.add(
                "A perda apresentou continuidade parcial.",
                8
            )

    def _score_average_loss(self, result, candidate):

        avg = candidate.event.avg_loss

        if avg >= 50:

            result.add(
                "A perda média do evento foi muito elevada.",
                15
            )

        elif avg >= 20:

            result.add(
                "A perda média do evento foi elevada.",
                10
            )

        elif avg >= 5:

            result.add(
                "A perda média do evento foi moderada.",
                5
            )

    def _score_peak_loss(self, result, candidate):

        peak = candidate.event.max_loss

        if peak >= 80:

            result.add(
                "O evento apresentou pico de perda extremamente elevado.",
                5
            )

        elif peak >= 50:

            result.add(
                "O evento apresentou pico elevado de perda.",
                3
            )

    def _score_event_length(self, result, candidate):

        tamanho = candidate.event.total_hops

        if tamanho >= 10:

            result.add(
                "O evento persistiu por muitos hops.",
                15
            )

        elif tamanho >= 5:

            result.add(
                "O evento persistiu por diversos hops.",
                10
            )

        elif tamanho >= 3:

            result.add(
                "O evento persistiu por vários hops.",
                5
            )

    #
    # ------------------------------------------------------------------
    # Evidências negativas
    # ------------------------------------------------------------------
    #

    def _score_icmp(self, result, candidate):

        hops_filtrados = sum(
            1
            for hop in candidate.event.hops
            if hop.icmp_filtrado
        )

        if hops_filtrados == 0:
            return

        if hops_filtrados == len(candidate.event.hops):

            result.add(
                "Todos os hops do evento apresentaram filtragem ICMP.",
                -20
            )

        else:

            result.add(
                "Parte do evento apresentou filtragem ICMP.",
                -10
            )

    def _score_isolated(self, result, candidate):

        if candidate.event.total_hops > 1:
            return

        anterior = False
        proximo = False

        if candidate.previous_hop is not None:

            anterior = (
                candidate.previous_hop.perda_real
                and candidate.previous_hop.loss > 0
            )

        if candidate.next_hop is not None:

            proximo = (
                candidate.next_hop.perda_real
                and candidate.next_hop.loss > 0
            )

        if not anterior and not proximo:

            result.add(
                "Evento isolado possui menor confiabilidade.",
                -10
            )