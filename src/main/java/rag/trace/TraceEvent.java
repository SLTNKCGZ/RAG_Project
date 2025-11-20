package main.java.rag.trace;

/**
 * Represents a trace event for a pipeline stage.
 * Contains stage name, inputs, outputs summary, timing, and optional error.
 */
public class TraceEvent {
    private String stage;
    private String inputs;
    private String outputsSummary;
    private long timingMs;
    private String error;
    
    public TraceEvent(String stage, String inputs, String outputsSummary, long timingMs) {
        this.stage = stage;
        this.inputs = inputs;
        this.outputsSummary = outputsSummary;
        this.timingMs = timingMs;
        this.error = null;
    }
    
    public TraceEvent(String stage, String inputs, String outputsSummary, long timingMs, String error) {
        this.stage = stage;
        this.inputs = inputs;
        this.outputsSummary = outputsSummary;
        this.timingMs = timingMs;
        this.error = error;
    }
    
    public String getStage() {
        return stage;
    }
    
    public String getInputs() {
        return inputs;
    }
    
    public String getOutputsSummary() {
        return outputsSummary;
    }
    
    public long getTimingMs() {
        return timingMs;
    }
    
    public String getError() {
        return error;
    }
    
    public boolean hasError() {
        return error != null;
    }
    
    /**
     * Convert to JSON string for JSONL format.
     */
    public String toJson() {
        StringBuilder json = new StringBuilder();
        json.append("{");
        json.append("\"stage\":\"").append(escapeJson(stage)).append("\",");
        json.append("\"inputs\":\"").append(escapeJson(inputs)).append("\",");
        json.append("\"outputsSummary\":\"").append(escapeJson(outputsSummary)).append("\",");
        json.append("\"timingMs\":").append(timingMs);
        if (error != null) {
            json.append(",\"error\":\"").append(escapeJson(error)).append("\"");
        }
        json.append("}");
        return json.toString();
    }
    
    private String escapeJson(String str) {
        if (str == null) return "";
        return str.replace("\\", "\\\\")
                  .replace("\"", "\\\"")
                  .replace("\n", "\\n")
                  .replace("\r", "\\r")
                  .replace("\t", "\\t");
    }
}
