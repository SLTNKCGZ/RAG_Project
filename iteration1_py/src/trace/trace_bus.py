from typing import List
from src.trace.trace_sink import TraceSink
from src.trace.trace_event import TraceEvent


class TraceBus:
    
    def __init__(self):
        self.__sinks: List[TraceSink] = []
    
    def register(self, sink: TraceSink) -> None:
        self.__sinks.append(sink)
    
    def unregister(self, sink: TraceSink) -> None:
        if sink in self.__sinks:
            self.__sinks.remove(sink)
    
    def publish(self, event: TraceEvent) -> None:
        for sink in self.__sinks:
            sink.record(event)
