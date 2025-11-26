from typing import List
from src.trace.trace_sink_abstract import TraceSinkAbstract
from src.trace.trace_event import TraceEvent


class TraceBus:
    
    def __init__(self):
        self.__sinks: List[TraceSinkAbstract] = []
    
    def register(self, sink: TraceSinkAbstract) -> None:
        self.__sinks.append(sink)
    
    def unregister(self, sink: TraceSinkAbstract) -> None:
        if sink in self.__sinks:
            self.__sinks.remove(sink)
    
    def publish(self, event: TraceEvent) -> None:
        for sink in self.__sinks:
            sink.record(event)
