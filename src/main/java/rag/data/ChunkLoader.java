package main.java.rag.data;

import java.io.IOException;
import java.nio.file.Files;
import java.nio.file.Path;
import java.util.List;
import main.java.rag.model.Chunk;


public class ChunkLoader {
    
    
    public ChunkStore loadChunks(Path chunksJsonPath) {
        try {
            List<String> lines = Files.readAllLines(chunksJsonPath);
            String jsonContent = String.join("\n", lines);
            
            ChunkStore chunkStore = new ChunkStore();
            parseJsonAndLoadChunks(jsonContent, chunkStore);
            
            return chunkStore;
        } catch (IOException e) {
            throw new RuntimeException("Failed to load chunks from: " + chunksJsonPath, e);
        }
    }
    

    private void parseJsonAndLoadChunks(String jsonContent, ChunkStore chunkStore) {
        // Remove whitespace and newlines for easier parsing
        String cleaned = jsonContent.replaceAll("\\s+", " ").trim();
        
        // Find documents array
        int documentsStart = cleaned.indexOf("\"documents\"");
        if (documentsStart == -1) {
            throw new RuntimeException("Invalid JSON: 'documents' key not found");
        }
        
        int arrayStart = cleaned.indexOf("[", documentsStart);
        if (arrayStart == -1) {
            throw new RuntimeException("Invalid JSON: documents array not found");
        }
        
        // Parse each document
        int pos = arrayStart + 1;
        while (pos < cleaned.length()) {
            int docStart = cleaned.indexOf("{", pos);
            if (docStart == -1) break;
            
            int docEnd = findMatchingBrace(cleaned, docStart);
            if (docEnd == -1) break;
            
            String docJson = cleaned.substring(docStart, docEnd + 1);
            parseDocument(docJson, chunkStore);
            
            pos = docEnd + 1;
        }
    }
    
   
    private void parseDocument(String docJson, ChunkStore chunkStore) {
        // Extract docId
        String docId = extractStringValue(docJson, "docId");
        if (docId == null) {
            throw new RuntimeException("Invalid document: docId not found");
        }
        
        // Extract title
        String title = extractStringValue(docJson, "title");
        if (title != null) {
            chunkStore.setDocumentTitle(docId, title);
        }
        
        // Extract sections array
        int sectionsStart = docJson.indexOf("\"sections\"");
        if (sectionsStart == -1) return;
        
        int arrayStart = docJson.indexOf("[", sectionsStart);
        if (arrayStart == -1) return;
        
        // Parse each section
        int pos = arrayStart + 1;
        while (pos < docJson.length()) {
            int sectionStart = docJson.indexOf("{", pos);
            if (sectionStart == -1) break;
            
            int sectionEnd = findMatchingBrace(docJson, sectionStart);
            if (sectionEnd == -1) break;
            
            String sectionJson = docJson.substring(sectionStart, sectionEnd + 1);
            parseSection(sectionJson, docId, chunkStore);
            
            pos = sectionEnd + 1;
        }
    }
    
    
    private void parseSection(String sectionJson, String docId, ChunkStore chunkStore) {
        // Extract sectionId
        String sectionId = extractStringValue(sectionJson, "sectionId");
        if (sectionId == null) {
            sectionId = ""; // Default if not found
        }
        
        // Extract chunks array
        int chunksStart = sectionJson.indexOf("\"chunks\"");
        if (chunksStart == -1) return;
        
        int arrayStart = sectionJson.indexOf("[", chunksStart);
        if (arrayStart == -1) return;
        
        // Parse each chunk
        int pos = arrayStart + 1;
        while (pos < sectionJson.length()) {
            int chunkStart = sectionJson.indexOf("{", pos);
            if (chunkStart == -1) break;
            
            int chunkEnd = findMatchingBrace(sectionJson, chunkStart);
            if (chunkEnd == -1) break;
            
            String chunkJson = sectionJson.substring(chunkStart, chunkEnd + 1);
            parseChunk(chunkJson, docId, sectionId, chunkStore);
            
            pos = chunkEnd + 1;
        }
    }
    
    
    private void parseChunk(String chunkJson, String docId, String sectionId, ChunkStore chunkStore) {
        String chunkId = extractStringValue(chunkJson, "chunkId");
        String content = extractStringValue(chunkJson, "content");
        int startOffset = extractIntValue(chunkJson, "startOffset");
        int endOffset = extractIntValue(chunkJson, "endOffset");
        
        if (chunkId == null || content == null) {
            throw new RuntimeException("Invalid chunk: missing required fields");
        }
        
        Chunk chunk = new Chunk(docId, chunkId, content, sectionId, startOffset, endOffset);
        chunkStore.addChunk(chunk);
    }
    
    
    private String extractStringValue(String json, String key) {
        String searchKey = "\"" + key + "\"";
        int keyPos = json.indexOf(searchKey);
        if (keyPos == -1) return null;
        
        int colonPos = json.indexOf(":", keyPos);
        if (colonPos == -1) return null;
        
        // Find the value (string between quotes)
        int quoteStart = json.indexOf("\"", colonPos);
        if (quoteStart == -1) return null;
        
        int quoteEnd = json.indexOf("\"", quoteStart + 1);
        if (quoteEnd == -1) return null;
        
        return json.substring(quoteStart + 1, quoteEnd);
    }
    
    /**
     * Extract integer value from JSON by key.
     */
    private int extractIntValue(String json, String key) {
        String searchKey = "\"" + key + "\"";
        int keyPos = json.indexOf(searchKey);
        if (keyPos == -1) return 0;
        
        int colonPos = json.indexOf(":", keyPos);
        if (colonPos == -1) return 0;
        
        // Find the number
        int numStart = colonPos + 1;
        while (numStart < json.length() && Character.isWhitespace(json.charAt(numStart))) {
            numStart++;
        }
        
        int numEnd = numStart;
        while (numEnd < json.length() && (Character.isDigit(json.charAt(numEnd)) || json.charAt(numEnd) == '-')) {
            numEnd++;
        }
        
        try {
            return Integer.parseInt(json.substring(numStart, numEnd).trim());
        } catch (NumberFormatException e) {
            return 0;
        }
    }
    
    /**
     * Find matching closing brace for an opening brace.
     */
    private int findMatchingBrace(String str, int openBracePos) {
        int depth = 1;
        int pos = openBracePos + 1;
        
        while (pos < str.length() && depth > 0) {
            char c = str.charAt(pos);
            if (c == '{') {
                depth++;
            } else if (c == '}') {
                depth--;
            } else if (c == '"') {
                // Skip string content
                pos++;
                while (pos < str.length() && str.charAt(pos) != '"') {
                    if (str.charAt(pos) == '\\') {
                        pos++; // Skip escaped character
                    }
                    pos++;
                }
            }
            pos++;
        }
        
        return depth == 0 ? pos - 1 : -1;
    }
}
