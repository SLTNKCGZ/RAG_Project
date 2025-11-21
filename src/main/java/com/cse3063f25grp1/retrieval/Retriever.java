package com.cse3063f25grp1.retrieval;

import java.util.List;
import com.cse3063f25grp1.data.ChunkStore;
import com.cse3063f25grp1.model.Hit;

public interface Retriever {

    List<Hit> retrieve(List<String> queryTerms, ChunkStore store);
}
