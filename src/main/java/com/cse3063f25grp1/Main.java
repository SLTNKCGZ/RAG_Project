package com.cse3063f25grp1;


import java.nio.file.Files;
import java.nio.file.Path;
import java.nio.file.Paths;

import com.cse3063f25grp1.config.Config;
import com.cse3063f25grp1.config.ConfigLoader;
import com.cse3063f25grp1.context.Context;
import com.cse3063f25grp1.data.ChunkLoader;
import com.cse3063f25grp1.data.ChunkStore;
import com.cse3063f25grp1.model.Query;
import com.cse3063f25grp1.orchestrator.RagOrchestrator;

public class Main {
    public static void main(String[] args) throws Exception {

        String configPath = null;
        String query = null;

        // Basit argüman parser
        for (int i = 0; i < args.length; i++) {
            switch (args[i]) {
                case "--config":
                    configPath = "./src/main/resources/"+args[++i];
                    System.out.println(configPath);
                    break;
                case "--q":
                    query = args[++i];
                    break;
            }
        }
        System.out.println("cc "+configPath);
        if (configPath == null || query == null) {
            System.err.println("Kullanım: java -jar rag.jar --config config.yaml --q \"...\"");
            return;
        }
        Path p = Paths.get(configPath);
        if (!Files.exists(p)) {
            System.err.println("Config dosyası bulunamadı: " + p.toAbsolutePath());
            System.exit(2);
        }
        ConfigLoader configLoader = new ConfigLoader(Paths.get(configPath));
        System.out.println(configLoader.toString());
        Config config = configLoader.loadConfig();
        
        Query question = new Query(query);
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