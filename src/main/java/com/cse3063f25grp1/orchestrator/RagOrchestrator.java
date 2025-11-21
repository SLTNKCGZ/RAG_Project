package com.cse3063f25grp1.orchestrator;

import com.cse3063f25grp1.config.Config;
import com.cse3063f25grp1.context.Context;
import com.cse3063f25grp1.trace.JsonlTraceSink;
import com.cse3063f25grp1.trace.TraceBus;

public class RagOrchestrator {
    private final Context context;
    private final TraceBus traceBus;

    public RagOrchestrator(Context context) {
        this.context = context;
        this.traceBus = new TraceBus();
        System.out.println("RagOrchestrator created.");
    }

    public void run(Config config, String question) {
        // Register JsonlTraceSink for logging
        JsonlTraceSink jsonlSink = new JsonlTraceSink(config.getLogsDirPath());
        traceBus.register(jsonlSink);

        RagPipeline pipeline = new SequentialRagPipeline(config, context, traceBus);
        pipeline.execute();

    }
}
