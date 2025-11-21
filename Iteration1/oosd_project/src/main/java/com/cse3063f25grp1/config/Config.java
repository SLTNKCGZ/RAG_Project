package com.cse3063f25grp1.config;

import java.nio.file.Path;

public class Config {
    private String intentType;
    private String writerType;
    private String retrieverType;
    private String reranker;
    private String answerAgentType;
    private Path RulesFilePath;
    private int topK;
    private Path stopwordsFilePath;
    private int topN;
    private Path chunkPath;
    private Path logsDirPath;

    public Config(String intentType, String writerType, String retrieverType, String reranker,
            String answerAgentType, Path rulesFilePath, int topK, Path stopwordsFilePath,
            int topN, Path chunkPath, Path logsDirPath) {
        this.intentType = intentType;
        this.writerType = writerType;
        this.retrieverType = retrieverType;
        this.reranker = reranker;
        this.answerAgentType = answerAgentType;
        this.RulesFilePath = rulesFilePath;
        this.topK = topK;
        this.stopwordsFilePath = stopwordsFilePath;
        this.topN = topN;
        this.chunkPath = chunkPath;
        this.logsDirPath = logsDirPath;
    }

    public String getIntentType() {
        return intentType;
    }

    public String getWriterType() {
        return writerType;
    }

    public String getRetrieverType() {
        return retrieverType;
    }

    public String getReranker() {
        return reranker;
    }

    public String getAnswerAgentType() {
        return answerAgentType;
    }

    public Path getRulesFilePath() {
        return RulesFilePath;
    }

    public int getTopK() {
        return topK;
    }

    public Path getStopwordsFilePath() {
        return stopwordsFilePath;
    }

    public int getTopN() {
        return topN;
    }


    public Path getChunkPath() {
        return chunkPath;
    }

    public Path getLogsDirPath() {
        return logsDirPath;
    }

}
