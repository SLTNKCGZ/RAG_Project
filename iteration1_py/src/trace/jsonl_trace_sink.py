import json
from pathlib import Path
from datetime import datetime

from src.trace.trace_sink_abstract import TraceSinkAbstract
from src.trace.trace_event import TraceEvent


class JsonlTraceSink(TraceSinkAbstract):
    """
    Trace sink that writes events to JSONL (JSON Lines) format.
    One JSON object per line.
    """
    
    def __init__(self, logs_dir: Path):
        """
        Initialize JsonlTraceSink.
        
        Args:
            logs_dir: Directory to write log files
        """
        logs_dir = Path(logs_dir)
        
        # Create logs directory if it doesn't exist
        try:
            logs_dir.mkdir(parents=True, exist_ok=True)
        except Exception as e:
            raise RuntimeError(f"Failed to create logs directory: {logs_dir}") from e
        
        # Generate log file name with timestamp
        now = datetime.now()
        timestamp = now.strftime("%Y%m%d-%H%M%S")
        self.log_file = logs_dir / f"run-{timestamp}.jsonl"
    
    def record(self, event: TraceEvent) -> None:
        """
        Record a trace event to JSONL file.
        
        Args:
            event: TraceEvent to record
        """
        try:
            json_line = event.to_json() + "\n"
            with open(self.log_file, 'a', encoding='utf-8') as f:
                f.write(json_line)
        except Exception as e:
            raise RuntimeError(f"Failed to write trace event to {self.log_file}") from e
    
    def get_log_file(self) -> Path:
        """Get the log file path."""
        return self.log_file
