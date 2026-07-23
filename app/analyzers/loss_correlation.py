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
        analysis.first_persistent_loss = candidate.start_hop
        analysis.hop = candidate.start_hop

        analysis.persistent = candidate.persistent

        analysis.score = score_result.score
        analysis.confidence = score_result.confidence
        analysis.evidencias = score_result.evidences

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
                    "Recomenda-se repetir a coleta em outro momento para validar o comportamento observado."
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

        #
        # Primeiro verifica se existem evidências suficientes
        # para afirmar uma anomalia.
        #

        if self._is_anomaly(
            trace,
            candidate,
            score_result,
        ):
            return self.ANOMALY

        #
        # Depois verifica se existem evidências suficientes
        # para afirmar que NÃO existe perda.
        #

        if self._is_no_anomaly(
            trace,
            candidate,
        ):
            return self.NO_ANOMALY

        #
        # Restante dos casos.
        #

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

        #
        # Destino sem perda.
        #

        if destino.loss <= 0:
            return False

        if not destino.perda_real:
            return False

        #
        # Perda precisa persistir.
        #

        if not candidate.persistent:
            return False

        #
        # Score muito baixo.
        #

        if score_result.score < 40:
            return False

        #
        # Deve existir evidência positiva.
        #

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

        #
        # Sem perda no destino.
        #

        if destino.loss <= 0:
            return True

        #
        # Existe perda apenas intermediária.
        #

        if not destino.perda_real:
            return True

        #
        # Evento não persistente.
        #

        if not candidate.persistent:
            return True

        return False

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