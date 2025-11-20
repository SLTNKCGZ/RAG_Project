package main.java.rag.model;

public class Hit {
    private String docId;
    private String chunkId;
    private int score;
    
    public Hit() {
    }
    
    public Hit(String docId, String chunkId, int score) {
        this.docId = docId;
        this.chunkId = chunkId;
        this.score = score;
    }
    
    public String getDocId() {
        return docId;
    }
    
    public String getChunkId() {
        return chunkId;
    }
    
    public int getScore() {
        return score;
    }
    
    public void setScore(int score) {
        this.score = score;
    }
    
    @Override
    public String toString() {
        return "Hit{" +
               "docId='" + docId + '\'' +
               ", chunkId='" + chunkId + '\'' +
               ", score=" + score +
               '}';
    }
}
