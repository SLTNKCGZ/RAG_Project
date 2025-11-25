from abc import ABC, abstractmethod
from src.trace.trace_event import TraceEvent


class TraceSinkAbstract(ABC):
    

    @abstractmethod
    def record(self, event: TraceEvent) -> None:
      
        pass
