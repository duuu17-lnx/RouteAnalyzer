from dataclasses import dataclass, field

from app.models.evidence_item import EvidenceItem


@dataclass
class ScoreResult:
    """
    Resultado da avaliação de um candidato.

    O ScoreResult é apenas um acumulador de evidências.
    Ele não toma decisões sobre existência de anomalia.
    Essa responsabilidade pertence ao LossCorrelation.
    """

    score: int = 0

    confidence: float = 0.0

    evidences: list[EvidenceItem] = field(default_factory=list)

    positive_points: int = 0

    negative_points: int = 0

    def add(
        self,
        description: str,
        points: int
    ) -> None:

        evidence = EvidenceItem(
            description=description,
            points=points
        )

        self.evidences.append(evidence)

        self.score += points

        if points >= 0:
            self.positive_points += points
        else:
            self.negative_points += abs(points)

        self._update_confidence()

    def _update_confidence(self):

        #
        # A confiança NÃO representa a probabilidade
        # de existir uma anomalia.
        #
        # Ela representa o quanto as evidências
        # sustentam a pontuação calculada.
        #

        score_factor = min(max(self.score, 0), 100) / 100.0

        evidence_factor = min(len(self.evidences), 10) / 10.0

        confidence = (
            score_factor * 0.80 +
            evidence_factor * 0.20
        )

        self.confidence = round(confidence, 2)

    @property
    def evidence_count(self):

        return len(self.evidences)

    @property
    def has_positive_evidence(self):

        return self.positive_points > 0

    @property
    def has_negative_evidence(self):

        return self.negative_points > 0

    def summary(self):

        return [
            f"[{e.points:+}] {e.description}"
            for e in self.evidences
        ]