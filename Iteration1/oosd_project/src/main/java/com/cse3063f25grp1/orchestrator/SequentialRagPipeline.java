package com.cse3063f25grp1.orchestrator;

import com.cse3063f25grp1.config.Config;
import com.cse3063f25grp1.context.Context;

public class SequentialRagPipeline extends RagPipeline {

    public SequentialRagPipeline(Config config, Context context, com.cse3063f25grp1.trace.TraceBus traceBus) {
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
