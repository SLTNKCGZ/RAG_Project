package main.java.rag.model;

import java.util.Objects;

public class Query {
    private String question;
    private Intent intent;
    
    public Query() {
    }
    
    public Query(String question, Intent intent) {
        this.question = question;
        this.intent = intent;
    }
    
    public String getQuestion() {
        return question;
    }
    
    public void setQuestion(String question) {
        this.question = question;
    }
    
    public Intent getIntent() {
        return intent;
    }
    
    public void setIntent(Intent intent) {
        this.intent = intent;
    }
    
    @Override
    public boolean equals(Object o) {
        if (this == o) return true;
        if (o == null || getClass() != o.getClass()) return false;
        Query query = (Query) o;
        return Objects.equals(question, query.question) &&
               intent == query.intent;
    }
    
    @Override
    public int hashCode() {
        return Objects.hash(question, intent);
    }
    
    @Override
    public String toString() {
        return "Query{" +
               "question='" + question + '\'' +
               ", intent=" + intent +
               '}';
    }
}
