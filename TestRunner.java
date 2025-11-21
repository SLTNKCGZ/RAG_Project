import com.cse3063f25grp1.answer.SimpleAnswerAgent;
import com.cse3063f25grp1.data.ChunkStore;
import com.cse3063f25grp1.model.Answer;
import com.cse3063f25grp1.model.Hit;

import java.util.ArrayList;
import java.util.List;

public class TestRunner {
    public static void main(String[] args) {
        System.out.println("=== Testing SimpleAnswerAgent Fallback Scenarios ===\n");
        
        // Test 1: Empty hits
        System.out.println("Test 1: Empty topHits");
        ChunkStore store = new ChunkStore();
        SimpleAnswerAgent agent = new SimpleAnswerAgent();
        Answer answer1 = agent.answer(
            List.of("test"),
            new ArrayList<>(),
            store
        );
        System.out.println("Result: " + answer1.getText());
        System.out.println("Citations: " + answer1.getCitations().size());
        System.out.println("Expected: 'Üzgünüm, sorunuza cevap bulamadım.'");
        System.out.println("PASS: " + answer1.getText().equals("Üzgünüm, sorunuza cevap bulamadım."));
        
        // Test 2: Null chunk (chunk not found in store)
        System.out.println("\n" + "=".repeat(50));
        System.out.println("Test 2: Null chunk (not found in store)");
        Hit hit = new Hit("nonexistent.txt", "section1", 1);
        Answer answer2 = agent.answer(
            List.of("test"),
            List.of(hit),
            store
        );
        System.out.println("Result: " + answer2.getText());
        System.out.println("Citations: " + answer2.getCitations().size());
        System.out.println("Expected: 'Üzgünüm, sorunuza ait detaylı metni bulamadım.'");
        System.out.println("PASS: " + answer2.getText().equals("Üzgünüm, sorunuza ait detaylı metni bulamadım."));
        
        // Test 3: Normal case with data
        System.out.println("\n" + "=".repeat(50));
        System.out.println("Test 3: Normal case with valid data");
        String text = "Erasmus koordinatörü Dr. Ali'dir. İletişim bilgileri bölümde mevcuttur.";
        com.cse3063f25grp1.model.Chunk chunk = new com.cse3063f25grp1.model.Chunk(
            "doc1", "chunk1", text, "section1", 0, text.length()
        );
        store.addChunk(chunk);
        Hit validHit = new Hit("doc1", "chunk1", 5);
        Answer answer3 = agent.answer(
            List.of("erasmus", "koordinatörü"),
            List.of(validHit),
            store
        );
        System.out.println("Result: " + answer3.getText());
        System.out.println("Citations: " + answer3.getCitations().size());
        System.out.println("Has 'Your answer:': " + answer3.getText().startsWith("Your answer:"));
        System.out.println("Has 'See:': " + answer3.getText().contains("See:"));
        System.out.println("PASS: " + (answer3.getText().startsWith("Your answer:") && 
                                        answer3.getText().contains("See:") &&
                                        answer3.getCitations().size() == 1));
        
        System.out.println("\n" + "=".repeat(50));
        System.out.println("All tests completed!");
    }
}
