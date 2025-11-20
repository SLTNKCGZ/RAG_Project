package main.java.rag.model;

import java.util.ArrayList;
import java.util.List;

public class Chunk {
    private String docId;
    private String chunkId;
    private String text;
    private String sectionId;
    private int startOffset;
    private int endOffset;
    
    public Chunk() {
    }
    
    public Chunk(String docId, String chunkId, String text, String sectionId, int startOffset, int endOffset) {
        this.docId = docId;
        this.chunkId = chunkId;
        this.text = text;
        this.sectionId = sectionId;
        this.startOffset = startOffset;
        this.endOffset = endOffset;
    }
    
    public String getDocId() {
        return docId;
    }
    
    public String getChunkId() {
        return chunkId;
    }
    
    public String getText() {
        return text;
    }
    
    public String getSectionId() {
        return sectionId;
    }
    
    public int getStartOffset() {
        return startOffset;
    }
    
    public int getEndOffset() {
        return endOffset;
    }
    
    public List<String> getSentences() {
        List<String> sentences = new ArrayList<>();
        if (text == null || text.isEmpty()) {
            return sentences;
        }
        
        String[] parts = text.split("(?<=[.!?])\\s+");
        for (String part : parts) {
            String trimmed = part.trim();
            if (!trimmed.isEmpty()) {
                sentences.add(trimmed);
            }
        }
        
        if (sentences.isEmpty() && !text.trim().isEmpty()) {
            sentences.add(text.trim());
        }
        
        return sentences;
    }
    
    public boolean contains(String term) {
        if (text == null || term == null) {
            return false;
        }
        return text.toLowerCase().contains(term.toLowerCase());
    }
    
    public String formatCitation() {
        return docId + ":" + sectionId + ":" + startOffset + "-" + endOffset;
    }
    
    @Override
    public String toString() {
        return "Chunk{" +
               "docId='" + docId + '\'' +
               ", chunkId='" + chunkId + '\'' +
               ", sectionId='" + sectionId + '\'' +
               ", startOffset=" + startOffset +
               ", endOffset=" + endOffset +
               ", textLength=" + (text != null ? text.length() : 0) +
               '}';
    }
}
