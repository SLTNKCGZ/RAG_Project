package main.java.rag.data;

import java.util.ArrayList;
import java.util.HashMap;
import java.util.List;
import java.util.Map;
import java.util.Set;
import main.java.rag.model.Chunk;


public class ChunkStore {
    private final Map<String, Chunk> chunks; // key: docId||chunkId
    private final Map<String, String> documentTitles; // key: docId, value: title
    
    public ChunkStore() {
        this.chunks = new HashMap<>();
        this.documentTitles = new HashMap<>();
    }
    
    
    public void addChunk(Chunk chunk) {
        String key = chunk.getDocId() + "||" + chunk.getChunkId();
        chunks.put(key, chunk);
    }
    
    
    public Chunk getChunk(String docId, String chunkId) {
        String key = docId + "||" + chunkId;
        return chunks.get(key);
    }
    
    
    public List<Chunk> getAllChunks() {
        return new ArrayList<>(chunks.values());
    }
    
    
    public void setDocumentTitle(String docId, String title) {
        documentTitles.put(docId, title);
    }
    
    
    public String getDocumentTitle(String docId) {
        return documentTitles.get(docId);
    }
    
    
    public Set<String> getAllDocIds() {
        return documentTitles.keySet();
    }
    
    
    public int size() {
        return chunks.size();
    }
}
