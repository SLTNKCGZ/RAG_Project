from typing import List
from src.trace.trace_sink_abstract import TraceSinkAbstract
from src.trace.trace_event import TraceEvent


class TraceBus:
    
    def __init__(self):
       
        self.sinks: List[TraceSinkAbstract] = []
    
    def register(self, sink: TraceSinkAbstract) -> None:
       
        self.sinks.append(sink)
    
    def unregister(self, sink: TraceSinkAbstract) -> None:
       
        if sink in self.sinks:
            self.sinks.remove(sink)
    
    def publish(self, event: TraceEvent) -> None:
        
        for sink in self.sinks:
            sink.record(event)
