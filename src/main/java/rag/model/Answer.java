package main.java.rag.model;

import java.util.ArrayList;
import java.util.List;
import java.util.Objects;

public class Answer {
    private String text;
    private List<String> citations;
    
    public Answer() {
        this.citations = new ArrayList<>();
    }
    
    public Answer(String text) {
        this.text = text;
        this.citations = new ArrayList<>();
    }
    
    public Answer(String text, List<String> citations) {
        this.text = text;
        this.citations = citations != null ? new ArrayList<>(citations) : new ArrayList<>();
    }
    
    public String getText() {
        return text;
    }
    
    public void setText(String text) {
        this.text = text;
    }
    
    public List<String> getCitations() {
        return new ArrayList<>(citations);
    }
    
    public void setCitations(List<String> citations) {
        this.citations = citations != null ? new ArrayList<>(citations) : new ArrayList<>();
    }
    
    public void addCitation(String citation) {
        if (citation != null && !citation.isEmpty()) {
            citations.add(citation);
        }
    }
    
    public boolean hasCitations() {
        return !citations.isEmpty();
    }
    
    public String toSingleLine() {
        StringBuilder sb = new StringBuilder(text != null ? text : "");
        
        if (hasCitations()) {
            sb.append(" See: ");
            for (int i = 0; i < citations.size(); i++) {
                if (i > 0) {
                    sb.append(", ");
                }
                sb.append(citations.get(i));
            }
        }
        
        return sb.toString();
    }
    
    @Override
    public boolean equals(Object o) {
        if (this == o) return true;
        if (o == null || getClass() != o.getClass()) return false;
        Answer answer = (Answer) o;
        return Objects.equals(text, answer.text) &&
               Objects.equals(citations, answer.citations);
    }
    
    @Override
    public int hashCode() {
        return Objects.hash(text, citations);
    }
    
    @Override
    public String toString() {
        return "Answer{" +
               "text='" + text + '\'' +
               ", citations=" + citations.size() +
               '}';
    }
}
