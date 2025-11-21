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

        // Build a short source description for the main answer text
        String docTitle = chunkStore.getDocumentTitle(bestChunk.getDocId());
        String sourceDescription;
        if (docTitle != null && !docTitle.isEmpty()) {
            sourceDescription = String.format("Bu cevap \"%s\" başlıklı belgenin %s bölümünden alınmıştır. ",
                    docTitle,
                    bestChunk.getSectionId());
        } else {
            sourceDescription = String.format("Bu cevap %s belgesinin %s bölümünden alınmıştır. ",
                    bestChunk.getDocId(),
                    bestChunk.getSectionId());
        }

        // Format answer (include both explanation and source)
        String answerText = sourceDescription + "Cevabınız: " + bestSentence;

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

   
    private String selectBestSentence(String text, List<String> queryTerms) {
        if (text == null || text.isEmpty()) {
            return "Bilgi bulunamadı.";
        }

        String[] sentences = text.split("[.!?]+");
        if (sentences.length == 0) {
            return text.substring(0, Math.min(200, text.length()));
        }

        String bestSentence = sentences[0].trim();
        int bestTermCount = 0;
        boolean bestContainsAll = false;
        int bestLength = bestSentence.length();

        // Normalize query terms
        List<String> normalizedTerms = new ArrayList<>();
        if (queryTerms != null) {
            for (String term : queryTerms) {
                if (term != null && !term.trim().isEmpty()) {
                    normalizedTerms.add(term.toLowerCase());
                }
            }
        }

        for (String sentence : sentences) {
            sentence = sentence.trim();
            if (sentence.isEmpty())
                continue;

            int termCount = countQueryTerms(sentence, queryTerms);

            boolean containsAll = false;
            if (!normalizedTerms.isEmpty()) {
                String lowerSentence = sentence.toLowerCase();
                containsAll = true;
                for (String term : normalizedTerms) {
                    if (!lowerSentence.contains(term)) {
                        containsAll = false;
                        break;
                    }
                }
            }

            int length = sentence.length();

            if (containsAll) {
                if (!bestContainsAll
                        || termCount > bestTermCount
                        || (termCount == bestTermCount && length < bestLength)) {
                    bestContainsAll = true;
                    bestTermCount = termCount;
                    bestLength = length;
                    bestSentence = sentence;
                }
            } else if (!bestContainsAll) {
                if (termCount > bestTermCount
                        || (termCount == bestTermCount && length < bestLength)) {
                    bestTermCount = termCount;
                    bestLength = length;
                    bestSentence = sentence;
                }
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
