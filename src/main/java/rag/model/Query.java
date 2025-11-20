package main.java.rag.model;

import java.util.List;
import java.util.ArrayList;
import java.util.Objects;

public class Query {
    private String originalQuestion;
    private Intent intent;
    private List<String> searchTerms;
    
    public Query() {
        this.searchTerms = new ArrayList<>();
    }
    
    public Query(String originalQuestion, Intent intent, List<String> searchTerms) {
        this.originalQuestion = originalQuestion;
        this.intent = intent;
        this.searchTerms = searchTerms != null ? new ArrayList<>(searchTerms) : new ArrayList<>();
    }
    
    public String getOriginalQuestion() {
        return originalQuestion;
    }
    
    public void setOriginalQuestion(String originalQuestion) {
        this.originalQuestion = originalQuestion;
    }
    
    public Intent getIntent() {
        return intent;
    }
    
    public void setIntent(Intent intent) {
        this.intent = intent;
    }
    
    public List<String> getSearchTerms() {
        return new ArrayList<>(searchTerms);
    }
    
    public void setSearchTerms(List<String> searchTerms) {
        this.searchTerms = searchTerms != null ? new ArrayList<>(searchTerms) : new ArrayList<>();
    }
    
    public void addSearchTerm(String term) {
        if (term != null && !term.isEmpty()) {
            searchTerms.add(term);
        }
    }
    
    public boolean hasSearchTerms() {
        return !searchTerms.isEmpty();
    }
    
    @Override
    public boolean equals(Object o) {
        if (this == o) return true;
        if (o == null || getClass() != o.getClass()) return false;
        Query query = (Query) o;
        return Objects.equals(originalQuestion, query.originalQuestion) &&
               intent == query.intent &&
               Objects.equals(searchTerms, query.searchTerms);
    }
    
    @Override
    public int hashCode() {
        return Objects.hash(originalQuestion, intent, searchTerms);
    }
    
    @Override
    public String toString() {
        return "Query{" +
               "originalQuestion='" + originalQuestion + '\'' +
               ", intent=" + intent +
               ", searchTerms=" + searchTerms +
               '}';
    }
}
