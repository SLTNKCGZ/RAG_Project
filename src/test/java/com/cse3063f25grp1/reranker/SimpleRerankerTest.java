package com.cse3063f25grp1.reranker;

import com.cse3063f25grp1.data.ChunkStore;
import com.cse3063f25grp1.model.Chunk;
import com.cse3063f25grp1.model.Hit;
import org.junit.jupiter.api.Test;

import java.util.Arrays;
import java.util.List;

import static org.junit.jupiter.api.Assertions.assertEquals;

class SimpleRerankerTest {

@Test
void verifiesTopKOrderAndTieBreaks() {
    ChunkStore store = new ChunkStore();

    Chunk chunk1 = new Chunk("staff.txt", "ali_yilmaz", "Bilgisayar mühendisliği", "staff", 0, 20);
    Chunk chunk2 = new Chunk("staff.txt", "ayse_demir", "Bilgisayar mühendisliği", "staff", 0, 20);

    store.addChunk(chunk1);
    store.addChunk(chunk2);
    store.setDocumentTitle("staff.txt", "Personel"); 

    Hit hit1 = new Hit("staff.txt", "ali_yilmaz", 2); // base: 20
    Hit hit2 = new Hit("staff.txt", "ayse_demir", 2); // base: 20

    SimpleReranker reranker = new SimpleReranker(50, 5, 3);

    List<Hit> reranked = reranker.rerank(
            Arrays.asList("bilgisayar", "elektronik"), 
            Arrays.asList(hit1, hit2),
            store
    );

    assertEquals(2, reranked.size());
    assertEquals(20, reranked.get(0).getScore()); 
    assertEquals(20, reranked.get(1).getScore());
    assertEquals("ali_yilmaz", reranked.get(0).getChunkId());   
    assertEquals("ayse_demir", reranked.get(1).getChunkId());
}
    
}


