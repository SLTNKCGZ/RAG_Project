package main.java.rag.intent;

import main.java.rag.model.Intent;

public interface IntentDetector {
    Intent detect(String question);
}