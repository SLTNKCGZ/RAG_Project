package com.cse3063f25grp1;

import java.nio.file.Path;
import java.nio.file.Paths;
import java.util.Scanner;
import com.cse3063f25grp1.config.Config;
import com.cse3063f25grp1.config.ConfigLoader;
import com.cse3063f25grp1.context.Context;
import com.cse3063f25grp1.data.ChunkLoader;
import com.cse3063f25grp1.data.ChunkStore;
import com.cse3063f25grp1.model.Query;
import com.cse3063f25grp1.orchestrator.RagOrchestrator;

public class Main {
    public static void main(String[] args) throws Exception {
        Scanner scanner = new Scanner(System.in);
        
        Path configPath = Paths.get("src/main/resources/config.yaml");
        
        ConfigLoader configLoader = new ConfigLoader(configPath);
        Config config = configLoader.loadConfig();
        System.out.println("Sorunuz nedir?:");
        String query=scanner.nextLine();
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