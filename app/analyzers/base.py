from abc import ABC, abstractmethod

from models.trace_result import TraceResult


class Analyzer(ABC):

    @abstractmethod
    def analyze(self, trace: TraceResult):
        pass