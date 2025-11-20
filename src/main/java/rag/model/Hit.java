package main.java.rag.model;

import java.util.Objects;

public class Hit implements Comparable<Hit> {
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
    
    public void setDocId(String docId) {
        this.docId = docId;
    }
    
    public String getChunkId() {
        return chunkId;
    }
    
    public void setChunkId(String chunkId) {
        this.chunkId = chunkId;
    }
    
    public int getScore() {
        return score;
    }
    
    public void setScore(int score) {
        this.score = score;
    }
    
    @Override
    public int compareTo(Hit other) {
        if (other == null) {
            return 1;
        }
        
        int scoreCompare = Integer.compare(other.score, this.score);
        if (scoreCompare != 0) {
            return scoreCompare;
        }
        
        if (docId == null && other.docId == null) {
            return 0;
        }
        if (docId == null) {
            return -1;
        }
        if (other.docId == null) {
            return 1;
        }
        
        int docIdCompare = docId.compareTo(other.docId);
        if (docIdCompare != 0) {
            return docIdCompare;
        }
        
        if (chunkId == null && other.chunkId == null) {
            return 0;
        }
        if (chunkId == null) {
            return -1;
        }
        if (other.chunkId == null) {
            return 1;
        }
        
        return chunkId.compareTo(other.chunkId);
    }
    
    @Override
    public boolean equals(Object o) {
        if (this == o) return true;
        if (o == null || getClass() != o.getClass()) return false;
        Hit hit = (Hit) o;
        return score == hit.score &&
               Objects.equals(docId, hit.docId) &&
               Objects.equals(chunkId, hit.chunkId);
    }
    
    @Override
    public int hashCode() {
        return Objects.hash(docId, chunkId, score);
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
