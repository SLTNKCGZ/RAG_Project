package com.cse3063f25grp1.reranker;

import java.util.List;
import com.cse3063f25grp1.data.ChunkStore;
import com.cse3063f25grp1.model.Hit;

public interface Reranker {
    List<Hit> rerank(List<String> query, List<Hit> hits, ChunkStore store);
}
