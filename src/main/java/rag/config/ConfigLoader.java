package main.java.rag.config;

import java.io.IOException;
import java.nio.file.Files;
import java.nio.file.Path;
import java.util.HashMap;
import java.util.List;
import java.util.Map;

public class ConfigLoader {
    private final Path configPath;

    public ConfigLoader(Path configPath) {
        this.configPath = configPath;
    }

    public Config loadConfig() {
        try {
            List<String> lines = Files.readAllLines(configPath);
            Map<String, String> configMap = parseYaml(lines);
            
            // Extract values from the parsed map
            String intentType = configMap.get("pipeline.intent_detector");
            String writerType = configMap.get("pipeline.query_writer");
            String retrieverType = configMap.get("pipeline.retriever");
            String reranker = configMap.get("pipeline.reranker");
            String answerAgentType = configMap.get("pipeline.answer_agent");
            
            String rulesFile = configMap.get("params.intent.rules_file");
            int topK = Integer.parseInt(configMap.get("params.retriever.top_k"));
            String stopwordsFile = configMap.get("params.query_writer.stopwords_file");
            int topN = Integer.parseInt(configMap.get("params.query_writer.top_n"));
            
            String documentsDir = configMap.get("paths.documents_dir");
            String chunkStore = configMap.get("paths.chunk_store");
            String logsDir = configMap.get("paths.logs_dir");
            
            // Convert relative paths to absolute paths based on config file location
            Path baseDir = configPath.getParent().getParent(); // Go up from resources to main
            Path rulesFilePath = resolvePath(baseDir, rulesFile);
            Path stopwordsFilePath = resolvePath(baseDir, stopwordsFile);
            Path documentsDirPath = resolvePath(baseDir, documentsDir);
            Path chunkPath = resolvePath(baseDir, chunkStore);
            Path logsDirPath = resolvePath(baseDir, logsDir);
            
            return new Config(
                intentType,
                writerType,
                retrieverType,
                reranker,
                answerAgentType,
                rulesFilePath,
                topK,
                stopwordsFilePath,
                topN,
                documentsDirPath,
                chunkPath,
                logsDirPath
            );
        } catch (IOException e) {
            throw new RuntimeException("Failed to load configuration from: " + configPath, e);
        }
    }
    
    private Map<String, String> parseYaml(List<String> lines) {
        Map<String, String> configMap = new HashMap<>();
        String currentSection = "";
        String currentSubSection = "";
        
        for (String line : lines) {
            if (line.trim().isEmpty() || line.trim().startsWith("#")) {
                continue;
            }
            
            int indentLevel = getIndentLevel(line);
            String content = line.trim();
            
            if (content.endsWith(":")) {
                // Section header
                String section = content.substring(0, content.length() - 1);
                if (indentLevel == 0) {
                    // Top-level section
                    currentSection = section;
                    currentSubSection = "";
                } else if (indentLevel == 2) {
                    // Sub-section under params
                    if (currentSection.equals("params")) {
                        currentSubSection = currentSection + "." + section;
                    } else {
                        currentSubSection = currentSection + "." + section;
                    }
                }
            } else if (content.contains(":")) {
                // Key-value pair
                String[] parts = content.split(":", 2);
                String key = parts[0].trim();
                String value = parts[1].trim();
                
                // Remove quotes if present
                if (value.startsWith("\"") && value.endsWith("\"")) {
                    value = value.substring(1, value.length() - 1);
                }
                
                // Build full key path
                String fullKey;
                if (indentLevel == 2 && !currentSubSection.isEmpty()) {
                    // Nested value (e.g., params.intent.rules_file)
                    fullKey = currentSubSection + "." + key;
                } else if (indentLevel == 2) {
                    // Direct value under section (e.g., pipeline.intent_detector)
                    fullKey = currentSection + "." + key;
                } else if (indentLevel == 0) {
                    // Top-level value (shouldn't happen in our YAML, but handle it)
                    fullKey = key;
                } else {
                    // Default: use current section
                    fullKey = currentSection.isEmpty() ? key : currentSection + "." + key;
                }
                
                configMap.put(fullKey, value);
            }
        }
        
        return configMap;
    }
    
    private int getIndentLevel(String line) {
        int count = 0;
        for (char c : line.toCharArray()) {
            if (c == ' ') {
                count++;
            } else {
                break;
            }
        }
        return count;
    }
    
    private Path resolvePath(Path baseDir, String relativePath) {
        // Remove leading "./" if present
        if (relativePath.startsWith("./")) {
            relativePath = relativePath.substring(2);
        }
        
        // Handle "../" for going up directories
        Path resolved = baseDir;
        while (relativePath.startsWith("../")) {
            resolved = resolved.getParent();
            relativePath = relativePath.substring(3);
        }
        
        return resolved.resolve(relativePath).normalize();
    }
}
