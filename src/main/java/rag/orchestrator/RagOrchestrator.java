package main.java.rag.orchestrator;

import main.java.rag.config.Config;
import main.java.rag.context.Context;
import main.java.rag.trace.JsonlTraceSink;
import main.java.rag.trace.TraceBus;

public class RagOrchestrator {
    private final Context context;
    private final TraceBus traceBus;

    public RagOrchestrator(Context context) {
        this.context = context;
        this.traceBus = new TraceBus();
    }
     
    public void run(Config config, String question) {
        // Register JsonlTraceSink for logging
        JsonlTraceSink jsonlSink = new JsonlTraceSink(config.getLogsDirPath());
        traceBus.register(jsonlSink);
        
        
        RagPipeline pipeline = new SequentialRagPipeline(config, context, traceBus);
        pipeline.execute();
        
    }
}
