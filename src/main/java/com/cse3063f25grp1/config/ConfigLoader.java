package com.cse3063f25grp1.config;

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

            // Debug: Print all parsed keys (can be removed later)
            System.err.println("Parsed config keys:");
            for (String key : configMap.keySet()) {
                System.err.println("  " + key + " = " + configMap.get(key));
            }

            // Extract values from the parsed map
            String intentType = configMap.get("pipeline.intent_detector");
            String writerType = configMap.get("pipeline.query_writer");
            String retrieverType = configMap.get("pipeline.retriever");
            String reranker = configMap.get("pipeline.reranker");
            String answerAgentType = configMap.get("pipeline.answer_agent");

            String rulesFile = configMap.get("params.intent.rules_file");
            String topKStr = configMap.get("params.retriever.top_k");
            if (topKStr == null) {
                throw new RuntimeException("Config dosyasında 'params.retriever.top_k' bulunamadı");
            }
            int topK = Integer.parseInt(topKStr);
            
            String stopwordsFile = configMap.get("params.query_writer.stopwords_file");
            String topNStr = configMap.get("params.query_writer.top_n");
            if (topNStr == null) {
                throw new RuntimeException("Config dosyasında 'params.query_writer.top_n' bulunamadı");
            }
            int topN = Integer.parseInt(topNStr);

            String documentsDir = configMap.get("paths.documents_dir");
            String chunkStore = configMap.get("paths.chunk_store");
            String logsDir = configMap.get("paths.logs_dir");

            // Null kontrolleri
            if (rulesFile == null) {
                throw new RuntimeException("Config dosyasında 'params.intent.rules_file' bulunamadı");
            }
            if (stopwordsFile == null) {
                throw new RuntimeException("Config dosyasında 'params.query_writer.stopwords_file' bulunamadı");
            }
            if (chunkStore == null) {
                throw new RuntimeException("Config dosyasında 'paths.chunk_store' bulunamadı");
            }
            if (logsDir == null) {
                throw new RuntimeException("Config dosyasında 'paths.logs_dir' bulunamadı");
            }

            // Convert relative paths to absolute paths based on config file location
            Path baseDir = configPath.getParent();
            if (baseDir == null) {
                baseDir = configPath.getFileSystem().getPath(".");
            }
            Path rulesFilePath = resolvePath(baseDir, rulesFile);
            Path stopwordsFilePath = resolvePath(baseDir, stopwordsFile);
            Path documentsDirPath = documentsDir != null ? resolvePath(baseDir, documentsDir) : null;
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
                    logsDirPath);
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
                if (indentLevel >= 4 && !currentSubSection.isEmpty()) {
                    // Deeply nested value (e.g., params.retriever.top_k)
                    fullKey = currentSubSection + "." + key;
                } else if (indentLevel == 2 && !currentSubSection.isEmpty()) {
                    // Nested value (e.g., params.intent.rules_file)
                    fullKey = currentSubSection + "." + key;
                } else if (indentLevel == 2) {
                    // Direct value under section (e.g., pipeline.intent_detector)
                    fullKey = currentSection + "." + key;
                } else if (indentLevel == 0) {
                    // Top-level value (shouldn't happen in our YAML, but handle it)
                    fullKey = key;
                } else {
                    // Default: use current section or subsection
                    if (!currentSubSection.isEmpty()) {
                        fullKey = currentSubSection + "." + key;
                    } else {
                        fullKey = currentSection.isEmpty() ? key : currentSection + "." + key;
                    }
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
