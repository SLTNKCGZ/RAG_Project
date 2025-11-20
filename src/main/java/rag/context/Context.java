package main.java.rag.context;

import main.java.rag.model.*;

import java.util.ArrayList;
import java.util.HashMap;
import java.util.List;
import java.util.Map;

/**
 * Context object that carries state through the RAG pipeline
 * GRASP: High Cohesion - All pipeline state in one place
 * SOLID: SRP - Single responsibility of holding pipeline context
 */
public class Context {
    private String originalQuestion;
    private Intent intent;
    private Query query;
    private List<Hit> retrievedHits;
    private List<Hit> rerankedHits;
    private Answer answer;
    private Map<String, Object> metadata;
    private long startTime;

    public Context() {
        this.retrievedHits = new ArrayList<>();
        this.rerankedHits = new ArrayList<>();
        this.metadata = new HashMap<>();
        this.startTime = System.currentTimeMillis();
    }

    public Context(String originalQuestion) {
        this();
        this.originalQuestion = originalQuestion;
    }

    // Getters and Setters
    public String getOriginalQuestion() { return originalQuestion; }
    public void setOriginalQuestion(String originalQuestion) { this.originalQuestion = originalQuestion; }

    public Intent getIntent() { return intent; }
    public void setIntent(Intent intent) { this.intent = intent; }

    public Query getQuery() { return query; }
    public void setQuery(Query query) { this.query = query; }

    public List<Hit> getRetrievedHits() { return retrievedHits; }
    public void setRetrievedHits(List<Hit> retrievedHits) { this.retrievedHits = retrievedHits; }

    public List<Hit> getRerankedHits() { return rerankedHits; }
    public void setRerankedHits(List<Hit> rerankedHits) { this.rerankedHits = rerankedHits; }

    public Answer getAnswer() { return answer; }
    public void setAnswer(Answer answer) { this.answer = answer; }

    public Map<String, Object> getMetadata() { return metadata; }
    public void setMetadata(Map<String, Object> metadata) { this.metadata = metadata; }

    public void putMetadata(String key, Object value) {
        this.metadata.put(key, value);
    }

    public Object getMetadata(String key) {
        return this.metadata.get(key);
    }

    public long getStartTime() { return startTime; }
    public void setStartTime(long startTime) { this.startTime = startTime; }

    public long getElapsedTime() {
        return System.currentTimeMillis() - startTime;
    }
}
