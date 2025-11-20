package main.java.rag.model;

public class Query {
    private String text;
    
    public Query() {
    }
    
    public Query(String text) {
        this.text = text;
    }
    
    public String getText() {
        return text;
    }
    
    @Override
    public String toString() {
        return "Query{" +
               "text='" + text + '\'' +
               '}';
    }
}
