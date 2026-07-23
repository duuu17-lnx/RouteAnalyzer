from dataclasses import dataclass, field

from app.analyzers.loss_analyzer import LossAnalyzer
from app.builders.trace_builder import TraceBuilder
from app.tests.loss.loss_scenarios import LossScenarios


@dataclass
class ScenarioResult:

    name: str

    success: bool

    expected_hop: int | None

    obtained_hop: int | None

    expected_persistent: bool

    obtained_persistent: bool

    analysis: object


@dataclass
class ValidationResult:

    total: int = 0

    passed: int = 0

    failed: int = 0

    scenarios: list[ScenarioResult] = field(default_factory=list)

    @property
    def ok(self):

        return self.failed == 0


class LossValidation:

    """
    Executa toda a suíte de cenários sintéticos do
    LossAnalyzer.

    Não realiza nenhuma impressão na tela.

    Apenas retorna um ValidationResult para que
    quem chamou decida como apresentar os dados.
    """

    def run(self):

        analyzer = LossAnalyzer()

        builder = TraceBuilder()

        validation = ValidationResult()

        for scenario in LossScenarios().all():

            trace = builder.build(scenario.hops)

            analysis = analyzer.analyze(trace)

            obtained_hop = None

            if analysis.hop is not None:

                obtained_hop = analysis.hop.index

            obtained_persistent = analysis.persistent

            success = (

                obtained_hop == scenario.expected_hop

                and

                obtained_persistent == scenario.expected_persistent

            )

            validation.total += 1

            if success:

                validation.passed += 1

            else:

                validation.failed += 1

            validation.scenarios.append(

                ScenarioResult(

                    name=scenario.name,

                    success=success,

                    expected_hop=scenario.expected_hop,

                    obtained_hop=obtained_hop,

                    expected_persistent=scenario.expected_persistent,

                    obtained_persistent=obtained_persistent,

                    analysis=analysis

                )

            )

        return validation