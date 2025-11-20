package main.java.rag.writer;

import java.util.List;

public interface QueryWriter {
    List<String> write(String question);
}