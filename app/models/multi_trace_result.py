from dataclasses import dataclass, field

from app.models.trace_result import TraceResult

@dataclass
class MultiTraceResult:

    traces: list[TraceResult] = field(default_factory=list)

    def add(self, trace: TraceResult):

        self.traces.append(trace)