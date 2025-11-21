package com.cse3063f25grp1;


import java.nio.file.Files;
import java.nio.file.Path;
import java.nio.file.Paths;

import com.cse3063f25grp1.config.Config;
import com.cse3063f25grp1.config.ConfigLoader;
import com.cse3063f25grp1.context.Context;
import com.cse3063f25grp1.data.ChunkLoader;
import com.cse3063f25grp1.data.ChunkStore;
import com.cse3063f25grp1.model.Answer;
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
                    configPath = args[++i];
                    break;
                case "--q":
                    query = args[++i];
                    break;
            }
        }
        
        if (configPath == null || query == null) {
            System.err.println("Kullanım: java -jar rag.jar --config config.yaml --q \"...\"");
            return;
        }

        Path configFilePath = resolveConfigPath(configPath);
        if (configFilePath == null || !Files.exists(configFilePath)) {
            System.err.println("Config dosyası bulunamadı: " + configPath);
            return;
        }

        ConfigLoader configLoader = new ConfigLoader(configFilePath);
        Config config = configLoader.loadConfig();
        
        Query question = new Query(query);
        Context context = new Context();
        ChunkLoader chunkLoader = new ChunkLoader();
        System.out.println("chunk "+config.getChunkPath());
        ChunkStore chunkStore = chunkLoader.loadChunks(config.getChunkPath());
        
        context.setChunkStore(chunkStore);
        RagOrchestrator orchestrator = new RagOrchestrator(context);
        context.setQuestion(question);
        orchestrator.run(config,context.getQuestion().getText());

        // Print answer including citations in a single line
        Answer finalAnswer = context.getFinalAnswer();
        if (finalAnswer != null) {
            System.out.println("Answer: " + finalAnswer.toSingleLine());
        } else {
            System.out.println("Answer: (no answer generated)");
        }
    }

    private static Path resolveConfigPath(String configArgument) {
        if (configArgument == null || configArgument.isBlank()) {
            return null;
        }

        Path directPath = Paths.get(configArgument).normalize();
        if (Files.exists(directPath)) {
            return directPath.toAbsolutePath();
        }

        if (!directPath.isAbsolute()) {
            Path[] fallbacks = {
                    Paths.get("src/main/resources").resolve(configArgument).normalize(),
                    Paths.get("resources").resolve(configArgument).normalize()
            };

            for (Path candidate : fallbacks) {
                if (Files.exists(candidate)) {
                    return candidate.toAbsolutePath();
                }
            }
        }

        try {
            java.net.URL resource = Main.class.getClassLoader().getResource(configArgument);
            if (resource != null && "file".equals(resource.getProtocol())) {
                return Paths.get(resource.toURI()).normalize();
            }
        } catch (java.net.URISyntaxException e) {
            // ignore and fall through
        }

        return null;
    }
}