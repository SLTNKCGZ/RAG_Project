package main.java.rag.model;

import java.util.Objects;

public class UserQuery {
    private String queryId;
    private String text;
    
    public UserQuery() {
    }
    
    public UserQuery(String text) {
        this.text = text;
    }
    
    public UserQuery(String queryId, String text) {
        this.queryId = queryId;
        this.text = text;
    }
    
    public String getQueryId() {
        return queryId;
    }
    
    public void setQueryId(String queryId) {
        this.queryId = queryId;
    }
    
    public String getText() {
        return text;
    }
    
    public void setText(String text) {
        this.text = text;
    }
    
    @Override
    public boolean equals(Object o) {
        if (this == o) return true;
        if (o == null || getClass() != o.getClass()) return false;
        UserQuery userQuery = (UserQuery) o;
        return Objects.equals(queryId, userQuery.queryId) &&
               Objects.equals(text, userQuery.text);
    }
    
    @Override
    public int hashCode() {
        return Objects.hash(queryId, text);
    }
    
    @Override
    public String toString() {
        return "UserQuery{" +
               "queryId='" + queryId + '\'' +
               ", text='" + text + '\'' +
               '}';
    }
}
