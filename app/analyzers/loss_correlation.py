from app.models.loss_analysis import LossAnalysis


class LossCorrelation:

    NO_ANOMALY = "NO_ANOMALY"
    ANOMALY = "ANOMALY"
    INCONCLUSIVE = "INCONCLUSIVE"

    def analyze(
        self,
        trace,
        config,
        candidate,
        score_result,
    ):

        analysis = LossAnalysis()

        analysis.first_loss = candidate.start_hop

        #
        # Primeira perda considerada relevante (>=2%)
        #

        analysis.first_relevant_loss = self._find_first_relevant_loss(
            trace
        )

        analysis.first_persistent_loss = candidate.start_hop
        analysis.hop = candidate.start_hop

        analysis.persistent = candidate.persistent

        analysis.score = score_result.score
        analysis.confidence = score_result.confidence
        analysis.evidencias = score_result.evidences

        #
        # Indica se a perda foi considerada ruído estatístico.
        #

        statistical_noise = self._is_statistical_noise(
            trace,
            config,
        )

        analysis.status = self._classify(
            trace=trace,
            config=config,
            candidate=candidate,
            score_result=score_result,
        )

        #
        # Diagnóstico
        #

        if analysis.status == self.ANOMALY:

            analysis.diagnosis = (
                "Foi identificada perda persistente compatível com degradação do encaminhamento."
            )

            analysis.recommendation = None

        elif analysis.status == self.NO_ANOMALY:

            if statistical_noise:

                analysis.diagnosis = (
                    "Foi observada perda residual compatível com ruído estatístico. "
                    "Não foram encontradas evidências de degradação do encaminhamento."
                )

            else:

                analysis.diagnosis = (
                    "Não foram encontradas evidências de perda real de encaminhamento."
                )

            analysis.recommendation = None

        else:

            analysis.diagnosis = (
                "Os dados coletados não são suficientes para confirmar ou descartar a ocorrência de perda real."
            )

            if self._is_advanced(config):

                analysis.recommendation = (
                    "Recomenda-se repetir a análise avançada para validar o comportamento observado."
                )

            else:

                analysis.recommendation = (
                    "Recomenda-se executar a análise avançada."
                )

        return analysis

    #
    # ---------------------------------------------------------
    # Correlação principal
    # ---------------------------------------------------------
    #

    def _classify(
        self,
        trace,
        config,
        candidate,
        score_result,
    ):

        if self._is_statistical_noise(
            trace,
            config,
        ):
            return self.NO_ANOMALY

        if self._is_advanced_inconclusive(
            trace,
            config,
        ):
            return self.INCONCLUSIVE

        if self._is_anomaly(
            trace,
            candidate,
            score_result,
        ):
            return self.ANOMALY

        if self._is_no_anomaly(
            trace,
            candidate,
        ):
            return self.NO_ANOMALY

        return self.INCONCLUSIVE

    #
    # ---------------------------------------------------------
    # Existe anomalia
    # ---------------------------------------------------------
    #

    def _is_anomaly(
        self,
        trace,
        candidate,
        score_result,
    ):

        destino = trace.hops[-1]

        if destino.loss <= 0:
            return False

        if not destino.perda_real:
            return False

        if not candidate.persistent:
            return False

        if score_result.score < 40:
            return False

        if not score_result.has_positive_evidence:
            return False

        return True

    #
    # ---------------------------------------------------------
    # Não existe anomalia
    # ---------------------------------------------------------
    #

    def _is_no_anomaly(
        self,
        trace,
        candidate,
    ):

        destino = trace.hops[-1]

        if destino.loss <= 0:
            return True

        if not destino.perda_real:
            return True

        if not candidate.persistent:
            return True

        return False

    #
    # ---------------------------------------------------------
    # Ruído estatístico
    # ---------------------------------------------------------
    #

    def _is_statistical_noise(
        self,
        trace,
        config,
    ):

        if not self._is_advanced(config):
            return False

        destino = trace.hops[-1]

        return (
            destino.perda_real
            and destino.loss > 0
            and destino.loss <= 0.50
        )

    #
    # ---------------------------------------------------------
    # Faixa inconclusiva
    # ---------------------------------------------------------
    #

    def _is_advanced_inconclusive(
        self,
        trace,
        config,
    ):

        if not self._is_advanced(config):
            return False

        destino = trace.hops[-1]

        return (
            destino.perda_real
            and 0.50 < destino.loss < 1.00
        )

    #
    # ---------------------------------------------------------
    # Primeira perda relevante
    # ---------------------------------------------------------
    #

    def _find_first_relevant_loss(
        self,
        trace,
    ):

        for hop in trace.hops:

            if (
                hop.perda_real
                and hop.loss >= 2.0
            ):
                return hop

        return None

    #
    # ---------------------------------------------------------
    # Perfil
    # ---------------------------------------------------------
    #

    def _is_advanced(
        self,
        config,
    ):

        return config.perfil.casefold() == "avançada"