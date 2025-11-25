from pathlib import Path

from src.config.config import Config
from src.context.context import Context
from src.orchestrator.sequential_rag_pipeline import SequentialRagPipeline
from src.trace.trace_bus import TraceBus
from src.trace.jsonl_trace_sink import JsonlTraceSink


class RagOrchestrator:
    
    def __init__(self, context: Context):
       
        self.context = context
        self.trace_bus = TraceBus()
    
    def run(self, config: Config, question: str) -> None:
       
        # Register JsonlTraceSink for logging
        jsonl_sink = JsonlTraceSink(config.get_logs_dir_path())
        self.trace_bus.register(jsonl_sink)
        
        # Create and execute pipeline
        pipeline = SequentialRagPipeline(config, self.context, self.trace_bus)
        pipeline.execute()
