package com.cse3063f25grp1.trace;

public interface TraceSink {
    void record(TraceEvent event);
}
