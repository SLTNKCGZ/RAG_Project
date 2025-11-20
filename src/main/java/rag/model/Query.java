package main.java.rag.model;

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
    
    public Intent getIntent() {
        return intent;
    }
    
    @Override
    public String toString() {
        return "Query{" +
               "question='" + question + '\'' +
               ", intent=" + intent +
               '}';
    }
}
