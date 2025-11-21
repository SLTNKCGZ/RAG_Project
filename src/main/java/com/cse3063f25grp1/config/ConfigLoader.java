package com.cse3063f25grp1.config;

import java.io.IOException;
import java.nio.file.Files;
import java.nio.file.Path;
import java.nio.file.Paths;
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

            String chunkStore = configMap.get("paths.chunk_store");
            String logsDir = configMap.get("paths.logs_dir");

            Path baseDir = configPath.getParent();
            if (baseDir == null) {
                baseDir = configPath.toAbsolutePath().getParent();
            }
            if (baseDir == null) {
                baseDir = configPath.toAbsolutePath();
            }

            Path rulesFilePath = resolvePath(baseDir, rulesFile);
            Path stopwordsFilePath = resolvePath(baseDir, stopwordsFile);
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
                    chunkPath,
                    logsDirPath);
        } catch (IOException e) {
            throw new RuntimeException("Failed to load configuration from: " + configPath, e);
        }
    }

    private Map<String, String> parseYaml(List<String> lines) {
    Map<String, String> map = new HashMap<>();
    String section = null;
    String subsection = null;

    for (String line : lines) {
        if (line.trim().isEmpty() || line.trim().startsWith("#"))
            continue;

        int indent = getIndentLevel(line);
        String content = line.trim();

        if (content.endsWith(":")) {
            String name = content.substring(0, content.length() - 1);

            if (indent == 0) {
                section = name;
                subsection = null;
            } else if (indent == 2) {
                subsection = section + "." + name;
            }
        } else if (content.contains(":")) {
            String[] parts = content.split(":", 2);
            String key = parts[0].trim();
            String value = parts[1].trim();

            // remove quotes
            if (value.startsWith("\"") && value.endsWith("\""))
                value = value.substring(1, value.length() - 1);

            String fullKey;
            if (indent == 4 && subsection != null) {
                fullKey = subsection + "." + key;
            } else if (indent == 2 && section != null) {
                fullKey = section + "." + key;
            } else {
                fullKey = key;
            }

            map.put(fullKey, value);
        }
    }
    
    return map;
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
        if (relativePath == null || relativePath.isEmpty()) {
            return null;
        }

        Path candidate = Paths.get(relativePath);
        if (candidate.isAbsolute()) {
            return candidate.normalize();
        }

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
