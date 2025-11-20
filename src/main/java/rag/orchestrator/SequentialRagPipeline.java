package main.java.rag.orchestrator;

import main.java.rag.config.Config;
import main.java.rag.context.Context;

/**
 * Sequential implementation of RAG Pipeline.
 * Overrides only execute() method to define sequential execution order.
 * All concrete methods from RagPipeline are used through context.
 */
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
