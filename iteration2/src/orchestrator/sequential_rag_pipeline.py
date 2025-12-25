from src.orchestrator.rag_pipeline import RagPipeline
from src.config.config import Config
from src.context.context import Context
from src.trace.trace_bus import TraceBus


class SequentialRagPipeline(RagPipeline):
  
    def __init__(self, config: Config, context: Context, trace_bus: TraceBus):
       
        super().__init__(config, context, trace_bus)
    
    def execute(self) -> None:
       
        self.detect_intent()
        self.write_query()
        self.retrieve()
        self.rerank()
        self.answer()
