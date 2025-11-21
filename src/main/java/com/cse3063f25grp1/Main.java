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
import com.cse3063f25grp1.model.Answer;
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

        // Resolve config path - try multiple locations
        Path configFilePath = resolveConfigPath(configPath);
        if (configFilePath == null || !Files.exists(configFilePath)) {
            System.err.println("Hata: Config dosyası bulunamadı: " + configPath);
            return;
        }

        ConfigLoader configLoader = new ConfigLoader(configFilePath);
        Config config = configLoader.loadConfig();
        
        Query question = new Query(query);
        Context context = new Context();
        ChunkLoader chunkLoader = new ChunkLoader();
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

    /**
     * Config dosyasının path'ini resolve eder.
     * Önce verilen path'i dener, bulunamazsa classpath'ten ve varsayılan konumlardan arar.
     */
    private static Path resolveConfigPath(String configPath) {
        // Önce verilen path'i dene (absolute veya relative)
        Path path = Paths.get(configPath);
        if (Files.exists(path)) {
            return path;
        }

        // Classpath'ten dene (resources klasöründen) - JAR içinde çalışırken önemli
        try {
            java.net.URL resource = Main.class.getClassLoader().getResource(configPath);
            if (resource != null && "file".equals(resource.getProtocol())) {
                return Paths.get(resource.toURI());
            }
        } catch (java.net.URISyntaxException e) {
            // Ignore
        }

        // Varsayılan konumları dene (development ortamı için)
        String[] defaultPaths = {
            "src/main/resources/" + configPath,
            "resources/" + configPath,
            "./" + configPath
        };

        for (String defaultPath : defaultPaths) {
            Path testPath = Paths.get(defaultPath);
            if (Files.exists(testPath)) {
                return testPath;
            }
        }

        return null;
    }
}