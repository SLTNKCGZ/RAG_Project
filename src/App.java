import java.nio.file.Path;
import java.nio.file.Paths;
import main.java.rag.config.Config;
import main.java.rag.config.ConfigLoader;
import main.java.rag.context.Context;
import main.java.rag.data.ChunkLoader;
import main.java.rag.data.ChunkStore;
import main.java.rag.model.Query;
import main.java.rag.orchestrator.RagOrchestrator;

public class App {
    public static void main(String[] args) throws Exception {
        
        Path configPath = Paths.get("src/main/resources/config.yaml");
        
        ConfigLoader configLoader = new ConfigLoader(configPath);
        Config config = configLoader.loadConfig();
        Query question = new Query("CSE3033 dersini hangi profesör veriyor?");
        Context context = new Context();
        ChunkLoader chunkLoader = new ChunkLoader();
        ChunkStore chunkStore = chunkLoader.loadChunks(config.getChunkPath());
        context.setChunkStore(chunkStore);
        RagOrchestrator orchestrator = new RagOrchestrator(context);
        context.setQuestion(question);
        orchestrator.run(config,context.getQuestion().getText());
        System.out.println("Answer: " + context.getFinalAnswer().getText());
    }
}
