package main.java.rag.orchestrator;

import java.nio.file.Files;
import java.nio.file.Path;
import java.util.HashSet;
import java.util.List;
import java.util.Map;
import java.util.Set;
import main.java.rag.answer.AnswerAgent;
import main.java.rag.answer.TemplateAnswerAgent;
import main.java.rag.config.Config;
import main.java.rag.context.Context;
import main.java.rag.data.ChunkLoader;
import main.java.rag.data.ChunkStore;
import main.java.rag.intent.IntentDetector;
import main.java.rag.intent.IntentRulesLoader;
import main.java.rag.intent.RuleIntentDetector;
import main.java.rag.model.Answer;
import main.java.rag.model.Hit;
import main.java.rag.model.Intent;
import main.java.rag.reranker.Reranker;
import main.java.rag.reranker.SimpleReranker;
import main.java.rag.retrieval.KeywordRetriever;
import main.java.rag.retrieval.Retriever;
import main.java.rag.trace.TraceBus;
import main.java.rag.trace.TraceEvent;
import main.java.rag.writer.HeuristicQueryWriter;
import main.java.rag.writer.QueryWriter;

public abstract class RagPipeline {
    
    protected final Config config;
    protected final Context context;
    protected final main.java.rag.trace.TraceBus traceBus;
    protected IntentDetector intentDetector;
    protected QueryWriter queryWriter;
    protected Retriever retriever;
    protected Reranker reranker;
    protected AnswerAgent answerAgent;

    public RagPipeline(Config config, Context context, TraceBus traceBus) {
        this.config = config;
        this.context = context;
        this.traceBus = traceBus;
    }
    public abstract void execute();
    
    
    protected void detectIntent() {
        long startTime = System.currentTimeMillis();
        String question = context.getQuestion().getText();
        String inputs = "question=\"" + question + "\"";
        String outputsSummary = "";
        String error = null;
        
        try {
            if(config.getIntentType().equals("RuleIntentDetector")){
                IntentRulesLoader rulesLoader = new IntentRulesLoader();
                Map<Intent, List<String>> rules = rulesLoader.loadRules(config.getRulesFilePath());
                intentDetector = new RuleIntentDetector(rules);
            } else {
                throw new IllegalArgumentException("Unknown intent detector type: " + config.getIntentType());
            }
            Intent intent = intentDetector.detect(question);
            context.setIntent(intent);
            outputsSummary = "intent=" + intent;
        } catch (Exception e) {
            error = e.getMessage();
            throw e;
        } finally {
            long timingMs = System.currentTimeMillis() - startTime;
            traceBus.publish(new TraceEvent("detectIntent", inputs, outputsSummary, timingMs, error));
        }
    }
    
    protected void writeQuery() {
        long startTime = System.currentTimeMillis();
        String question = context.getQuestion().getText();
        String inputs = "question=\"" + question + "\"";
        String outputsSummary = "";
        String error = null;
        
        try {
            if(config.getWriterType().equals("HeuristicQueryWriter")){
                Set<String> stopwords = loadStopwords(config.getStopwordsFilePath());
                queryWriter = new HeuristicQueryWriter(stopwords);
            } else {
                throw new IllegalArgumentException("Unknown query writer type: " + config.getWriterType());
            }
            
            List<String> terms = queryWriter.write(question);
            context.setTerms(terms);
            outputsSummary = "terms=" + terms.size() + " terms";
        } catch (Exception e) {
            error = e.getMessage();
            throw e;
        } finally {
            long timingMs = System.currentTimeMillis() - startTime;
            traceBus.publish(new TraceEvent("writeQuery", inputs, outputsSummary, timingMs, error));
        }
    }
    
    protected void retrieve() {
        long startTime = System.currentTimeMillis();
        List<String> terms = context.getTerms();
        String inputs = "terms=" + (terms != null ? terms.size() : 0) + " terms";
        String outputsSummary = "";
        String error = null;
        
        try {
            if(config.getRetrieverType().equals("KeywordRetriever")){
                retriever = new KeywordRetriever(config.getTopK());
            } else {
                throw new IllegalArgumentException("Unknown retriever type: " + config.getRetrieverType());
            }
            
            List<Hit> hits = retriever.retrieve(terms,context.getChunkStore());
            context.setRetrievedHits(hits);
            outputsSummary = "hits=" + (hits != null ? hits.size() : 0) + " hits";
        } catch (Exception e) {
            error = e.getMessage();
            throw e;
        } finally {
            long timingMs = System.currentTimeMillis() - startTime;
            traceBus.publish(new TraceEvent("retrieve", inputs, outputsSummary, timingMs, error));
        }
    }
    
    protected void rerank() {
        long startTime = System.currentTimeMillis();
        List<String> terms = context.getTerms();
        List<Hit> hits = context.getRetrievedHits();
        String inputs = "hits=" + (hits != null ? hits.size() : 0) + " hits";
        String outputsSummary = "";
        String error = null;
        
        try {
            if(config.getReranker().equals("SimpleReranker")){
                int proximityWindow = 15;
                int proximityBonus = 5;
                int titleBoost = 3;
                reranker = new SimpleReranker(proximityWindow, proximityBonus, titleBoost);
            } else {
                throw new IllegalArgumentException("Unknown reranker type: " + config.getReranker());
            }
            
            ChunkLoader chunkLoader = new ChunkLoader();
            ChunkStore chunkStore = chunkLoader.loadChunks(config.getChunkPath());
            
            List<Hit> rerankedHits = reranker.rerank(terms, hits, chunkStore);
            context.setRerankedHits(rerankedHits);
            outputsSummary = "rerankedHits=" + (rerankedHits != null ? rerankedHits.size() : 0) + " hits";
        } catch (Exception e) {
            error = e.getMessage();
            throw e;
        } finally {
            long timingMs = System.currentTimeMillis() - startTime;
            traceBus.publish(new TraceEvent("rerank", inputs, outputsSummary, timingMs, error));
        }
    }
    
    protected void answer() {
        long startTime = System.currentTimeMillis();
        List<Hit> rerankedHits = context.getRerankedHits();
        String inputs = "rerankedHits=" + (rerankedHits != null ? rerankedHits.size() : 0) + " hits";
        String outputsSummary = "";
        String error = null;
        
        try {
            if(config.getAnswerAgentType().equals("TemplateAnswerAgent")){
                answerAgent = new TemplateAnswerAgent();
            } else {
                throw new IllegalArgumentException("Unknown answer agent type: " + config.getAnswerAgentType());
            }
            
            Answer answer = new Answer("Answer not implemented yet");
            context.setFinalAnswer(answer);
            outputsSummary = "answerLength=" + (answer != null && answer.getText() != null ? answer.getText().length() : 0);
        } catch (Exception e) {
            error = e.getMessage();
            throw e;
        } finally {
            long timingMs = System.currentTimeMillis() - startTime;
            traceBus.publish(new TraceEvent("answer", inputs, outputsSummary, timingMs, error));
        }
    }
    
    // Helper method: Stopwords yükle
    protected Set<String> loadStopwords(Path stopwordsPath) {
        try {
            List<String> lines = Files.readAllLines(stopwordsPath);
            Set<String> stopwords = new HashSet<>();
            boolean inStopWords = false;
            
            for (String line : lines) {
                String trimmed = line.trim();
                if (trimmed.isEmpty() || trimmed.startsWith("#")) {
                    continue;
                }
                if (trimmed.equals("stop_words:")) {
                    inStopWords = true;
                    continue;
                }
                if (inStopWords && trimmed.startsWith("-")) {
                    String word = trimmed.substring(1).trim();
                    if (word.startsWith("\"") && word.endsWith("\"")) {
                        word = word.substring(1, word.length() - 1);
                    }
                    stopwords.add(word);
                }
            }
            return stopwords;
        } catch (Exception e) {
            throw new RuntimeException("Failed to load stopwords from: " + stopwordsPath, e);
        }
    }
}
