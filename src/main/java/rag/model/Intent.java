package main.java.rag.model;

public enum Intent {

    STAFF(1),
    COURSE(2),
    POLICY(3),
    REGISTRATION(4),
    GENERAL(5),
    UNKNOWN(999);

    private final int priority;

    Intent(int priority) {
        this.priority = priority;
    }

    public int getPriority() {
        return priority;
    }
}