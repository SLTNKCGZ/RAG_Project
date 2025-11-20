package main.java.rag.orchestrator;

import main.java.rag.config.Config;
import main.java.rag.context.Context;

public class SequentialRagPipeline extends RagPipeline {
    
    public SequentialRagPipeline(Config config, Context context, main.java.rag.trace.TraceBus traceBus) {
        super(config, context, traceBus);
    }

    @Override
    public void execute() {
        
        detectIntent();
        writeQuery();
        retrieve();
        rerank();
        answer();
    }
}
