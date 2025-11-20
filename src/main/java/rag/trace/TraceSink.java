package main.java.rag.trace;

public interface TraceSink {
    void record(TraceEvent event);
}
