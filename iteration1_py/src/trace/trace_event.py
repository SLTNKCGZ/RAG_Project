from typing import Optional


class TraceEvent:
   
    def __init__(self, stage: str, inputs: str, outputs_summary: str, timing_ms: float, error: Optional[str] = None):
        
        
        self.stage = stage
        self.inputs = inputs
        self.outputs_summary = outputs_summary
        self.timing_ms = timing_ms
        self.error = error
    
    def get_stage(self) -> str:
       
        return self.stage
    
    def get_inputs(self) -> str:
        """Get inputs."""
        return self.inputs
    
    def get_outputs_summary(self) -> str:
        
        return self.outputs_summary
    
    def get_timing_ms(self) -> float:
        
        return self.timing_ms
    
    def get_error(self) -> Optional[str]:
        
        return self.error
    
    def has_error(self) -> bool:
        
        return self.error is not None
    
    def to_json(self) -> str:
        
        import json
        return json.dumps({
            "stage": self.stage,
            "inputs": self.inputs,
            "outputs": self.outputs_summary,
            "timing_ms": self.timing_ms,
            "error": self.error
        })
    
    def __str__(self) -> str:
        return f"TraceEvent(stage={self.stage}, timing_ms={self.timing_ms}, error={self.error is not None})"
    
    def __repr__(self) -> str:
        return f"TraceEvent(stage={self.stage!r}, inputs={self.inputs!r}, outputs_summary={self.outputs_summary!r}, timing_ms={self.timing_ms}, error={self.error!r})"
