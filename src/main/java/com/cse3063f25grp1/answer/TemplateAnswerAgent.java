package com.cse3063f25grp1.answer;

import com.cse3063f25grp1.data.ChunkStore;
import com.cse3063f25grp1.model.Answer;
import com.cse3063f25grp1.model.Chunk;
import com.cse3063f25grp1.model.Hit;

import java.util.ArrayList;
import java.util.List;


public class TemplateAnswerAgent implements AnswerAgent {

    public TemplateAnswerAgent() {
    }

    @Override
    public Answer answer(List<String> queryTerms, List<Hit> topHits, ChunkStore chunkStore) {
        if (topHits == null || topHits.isEmpty()) {
            return new Answer("Üzgünüm, sorunuza cevap bulamadım.", new ArrayList<>());
        }

        // Get best chunk (first in reranked list)
        Hit bestHit = topHits.get(0);
        Chunk bestChunk = chunkStore.getChunk(bestHit.getDocId(), bestHit.getChunkId());
        if (bestChunk == null) {
            return new Answer("Üzgünüm, sorunuza ait detaylı metni bulamadım.", new ArrayList<>());
        }

        // Select best sentence from chunk
        String bestSentence = selectBestSentence(bestChunk.getText(), queryTerms);

        // Format answer
        String answerText = "Cevabınız: " + bestSentence;

        // Generate citations
        List<String> citations = new ArrayList<>();
        for (int i = 0; i < Math.min(3, topHits.size()); i++) {
            Hit hit = topHits.get(i);
            Chunk chunk = chunkStore.getChunk(hit.getDocId(), hit.getChunkId());
            if (chunk != null) {
                String citation = formatCitation(chunk);
                citations.add(citation);
            }
        }

        Answer answer = new Answer(answerText, citations);
        return answer;
    }

    /**
     * Select the best sentence from chunk text
     * Choose sentence with most query terms, or first sentence
     */
    private String selectBestSentence(String text, List<String> queryTerms) {
        if (text == null || text.isEmpty()) {
            return "Bilgi bulunamadı.";
        }

        // Split into sentences
        String[] sentences = text.split("[.!?]+");

        if (sentences.length == 0) {
            return text.substring(0, Math.min(200, text.length()));
        }

        String bestSentence = sentences[0].trim();
        int maxTermCount = 0;

        // Find sentence with most query terms
        for (String sentence : sentences) {
            sentence = sentence.trim();
            if (sentence.isEmpty())
                continue;

            int termCount = countQueryTerms(sentence, queryTerms);

            if (termCount > maxTermCount) {
                maxTermCount = termCount;
                bestSentence = sentence;
            }
        }

        return bestSentence;
    }

    /**
     * Count how many query terms appear in sentence
     */
    private int countQueryTerms(String sentence, List<String> queryTerms) {
        if (queryTerms == null)
            return 0;

        String lowerSentence = sentence.toLowerCase();
        int count = 0;

        for (String term : queryTerms) {
            if (lowerSentence.contains(term.toLowerCase())) {
                count++;
            }
        }

        return count;
    }

    /**
     * Format citation as: docId:sectionId:startOffset-endOffset
     */
    private String formatCitation(Chunk chunk) {
        return String.format("%s:%s:%d-%d",
                chunk.getDocId(),
                chunk.getSectionId(),
                chunk.getStartOffset(),
                chunk.getEndOffset());
    }
}
