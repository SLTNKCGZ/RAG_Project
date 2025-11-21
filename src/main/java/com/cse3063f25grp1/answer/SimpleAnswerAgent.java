package com.cse3063f25grp1.answer;

import java.util.ArrayList;
import java.util.List;

import com.cse3063f25grp1.data.ChunkStore;
import com.cse3063f25grp1.model.Answer;
import com.cse3063f25grp1.model.Chunk;
import com.cse3063f25grp1.model.Hit;

/**
 * Baseline implementation of AnswerAgent
 * Produces a short answer and citation(s) using simple sentence selection
 */
public class SimpleAnswerAgent implements AnswerAgent {

    private static class SentenceInfo {
        String sentence;
        int startOffset;
        int endOffset;

        SentenceInfo(String sentence, int startOffset, int endOffset) {
            this.sentence = sentence;
            this.startOffset = startOffset;
            this.endOffset = endOffset;
        }
    }

    @Override
    public Answer answer(List<String> query, List<Hit> topHits, ChunkStore chunkStore) {
        if (topHits == null || topHits.isEmpty()) {
            return new Answer("Üzgünüm, sorunuza cevap bulamadım.", new ArrayList<>());
        }

        // Get the top-1 chunk
        Hit topHit = topHits.get(0);
        Chunk chunk = chunkStore.getChunk(topHit.getDocId(), topHit.getChunkId());

        if (chunk == null) {
            return new Answer("Üzgünüm, sorunuza ait detaylı metni bulamadım.", new ArrayList<>());
        }

        // Select best sentence from top-1 chunk
        SentenceInfo bestSentenceInfo = selectBestSentence(chunk.getText(), query);

        // Create citation
        String citation = String.format("%s:%s:%d-%d",
                chunk.getDocId(),
                chunk.getSectionId(),
                chunk.getStartOffset() + bestSentenceInfo.startOffset,
                chunk.getStartOffset() + bestSentenceInfo.endOffset);

        // Create answer using template
        String answerText = String.format("Your answer: %s. See: %s",
                bestSentenceInfo.sentence, citation);

        List<String> citations = new ArrayList<>();
        citations.add(citation);

        return new Answer(answerText, citations);
    }

    /**
     * Select the best sentence from text based on query terms
     * Choose the sentence (split on . ! ?) that contains the most query terms
     * If none contain query terms, take the first sentence
     */
    private SentenceInfo selectBestSentence(String text, List<String> queryTerms) {
        if (text == null || text.isEmpty()) {
            return new SentenceInfo("Bilgi bulunamadı", 0, 0);
        }

        // Normalize query terms for comparison
        List<String> normalizedTerms = new ArrayList<>();
        if (queryTerms != null) {
            for (String term : queryTerms) {
                if (term != null && !term.trim().isEmpty()) {
                    normalizedTerms.add(term.toLowerCase());
                }
            }
        }

        // Check if text looks like tabular data (contains commas and common table keywords)
        String lowerText = text.toLowerCase();
        boolean isTabular = (text.contains(",") && 
                            (lowerText.contains("course code") || 
                             lowerText.contains("ects") || 
                             lowerText.contains("total")));

        if (isTabular) {
            // Extract relevant row from table
            return extractFromTable(text, normalizedTerms);
        }

        // Split text into sentences and track positions
        List<SentenceInfo> sentenceInfos = new ArrayList<>();
        int currentPos = 0;
        String[] sentences = text.split("[.!?]+");

        for (String sentence : sentences) {
            sentence = sentence.trim();
            if (sentence.isEmpty()) continue;

            int start = currentPos;
            int end = start + sentence.length();

            sentenceInfos.add(new SentenceInfo(sentence, start, end));
            currentPos = end + 1; // +1 for delimiter
        }

        if (sentenceInfos.isEmpty()) {
            int len = Math.min(150, text.length());
            return new SentenceInfo(text.substring(0, len).trim(), 0, len);
        }

        SentenceInfo bestSentenceInfo = null;
        int bestScore = 0;

        // Find sentence with most query term matches
        for (SentenceInfo info : sentenceInfos) {
            // Skip sentences that are too long (likely tables or data dumps)
            if (info.sentence.length() > 300) continue;

            String lowerSentence = info.sentence.toLowerCase();
            int score = 0;

            // Count query term matches
            for (String term : normalizedTerms) {
                if (lowerSentence.contains(term)) {
                    score++;
                }
            }

            if (score > bestScore) {
                bestScore = score;
                bestSentenceInfo = info;
            } else if (bestSentenceInfo == null) {
                // Take first reasonable sentence as fallback
                bestSentenceInfo = info;
            }
        }

        // If no good sentence found, try to find any short sentence
        if (bestSentenceInfo == null) {
            for (SentenceInfo info : sentenceInfos) {
                if (info.sentence.length() <= 300) {
                    bestSentenceInfo = info;
                    break;
                }
            }
        }

        // Last resort: take first sentence regardless of length
        if (bestSentenceInfo == null && !sentenceInfos.isEmpty()) {
            bestSentenceInfo = sentenceInfos.get(0);
        }

        return bestSentenceInfo != null ? bestSentenceInfo : new SentenceInfo("Bilgi bulunamadı", 0, 0);
    }

    /**
     * Extract relevant information from tabular data
     * Try to find a complete row that matches query terms
     */
    private SentenceInfo extractFromTable(String text, List<String> queryTerms) {
        // Find the row that best matches query terms
        // Rows typically have pattern: code, name, numbers...
        String[] parts = text.split(",");
        
        // Look for course code pattern (like cse3063)
        for (int i = 0; i < parts.length; i++) {
            String part = parts[i].trim().toLowerCase();
            
            // Check if this part matches query terms (especially course codes)
            boolean hasMatch = false;
            for (String term : queryTerms) {
                if (part.equals(term) || part.contains(term)) {
                    hasMatch = true;
                    break;
                }
            }
            
            if (hasMatch && i + 4 < parts.length) {
                // Extract: code, name, and credit info (typically 5-6 fields)
                StringBuilder row = new StringBuilder();
                row.append(parts[i].trim()); // course code
                
                // Add course name (usually next field, may span multiple parts)
                int nameStart = i + 1;
                int nameEnd = i + 1;
                
                // Find where numbers start (credits)
                for (int j = i + 1; j < Math.min(i + 5, parts.length); j++) {
                    String field = parts[j].trim();
                    // Check if it's a number (credit value)
                    if (field.matches("\\d+")) {
                        nameEnd = j - 1;
                        break;
                    }
                }
                
                // Add course name
                if (nameStart <= nameEnd) {
                    for (int j = nameStart; j <= nameEnd; j++) {
                        row.append(", ").append(parts[j].trim());
                    }
                }
                
                // Add credit info (cr and ects - typically last 2 numbers)
                if (nameEnd + 3 < parts.length) {
                    row.append(" - kredi: ").append(parts[nameEnd + 3].trim());
                }
                
                int startPos = text.indexOf(parts[i].trim());
                return new SentenceInfo(row.toString(), startPos, startPos + row.length());
            }
        }
        
        // Fallback: take first 150 chars
        int maxLen = Math.min(150, text.length());
        return new SentenceInfo(text.substring(0, maxLen).trim(), 0, maxLen);
    }
}