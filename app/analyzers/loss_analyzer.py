from app.analyzers.loss_correlation import LossCorrelation
from app.analyzers.loss_event_detector import LossEventDetector
from app.builders.candidate_builder import CandidateBuilder
from app.models.loss_analysis import LossAnalysis
from app.scorers.loss_score import LossScore


class LossAnalyzer:

    def analyze(
        self,
        trace,
        config,
    ):

        detector = LossEventDetector()

        events = detector.detect(trace)

        #
        # Nenhum evento encontrado
        #

        if not events:
            return LossAnalysis()

        #
        # Gera candidatos
        #

        builder = CandidateBuilder()

        candidates = builder.build_all(
            trace=trace,
            events=events,
        )

        if not candidates:
            return LossAnalysis()

        #
        # Calcula score de todos os candidatos
        #

        scorer = LossScore()

        best_candidate = None
        best_result = None

        for candidate in candidates:

            result = scorer.calculate(
                trace=trace,
                candidate=candidate,
            )

            if (
                best_result is None
                or result.score > best_result.score
            ):
                best_result = result
                best_candidate = candidate

        #
        # Segurança
        #

        if best_candidate is None:
            return LossAnalysis()

        #
        # Correlação final
        #

        correlator = LossCorrelation()

        return correlator.analyze(
            trace=trace,
            config=config,
            candidate=best_candidate,
            score_result=best_result,
        )