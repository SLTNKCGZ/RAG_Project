package main.java.rag.trace;

import java.util.ArrayList;
import java.util.List;

public class TraceBus {
    private final List<TraceSink> sinks;
    
    public TraceBus() {
        this.sinks = new ArrayList<>();
    }
    
    
    public void register(TraceSink sink) {
        sinks.add(sink);
    }
    
    
    public void unregister(TraceSink sink) {
        sinks.remove(sink);
    }
    

    public void publish(TraceEvent event) {
        for (TraceSink sink : sinks) {
            sink.record(event);
        }
    }
}
