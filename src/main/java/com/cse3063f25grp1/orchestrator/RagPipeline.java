package com.cse3063f25grp1.orchestrator;

import java.nio.file.Files;
import java.nio.file.Path;
import java.util.HashSet;
import java.util.List;
import java.util.Map;
import java.util.Set;

import com.cse3063f25grp1.answer.AnswerAgent;
import com.cse3063f25grp1.answer.TemplateAnswerAgent;
import com.cse3063f25grp1.config.Config;
import com.cse3063f25grp1.context.Context;
import com.cse3063f25grp1.data.ChunkLoader;
import com.cse3063f25grp1.data.ChunkStore;
import com.cse3063f25grp1.intent.IntentDetector;
import com.cse3063f25grp1.intent.IntentRulesLoader;
import com.cse3063f25grp1.intent.RuleIntentDetector;
import com.cse3063f25grp1.model.Answer;
import com.cse3063f25grp1.model.Hit;
import com.cse3063f25grp1.model.Intent;
import com.cse3063f25grp1.reranker.Reranker;
import com.cse3063f25grp1.reranker.SimpleReranker;
import com.cse3063f25grp1.retrieval.KeywordRetriever;
import com.cse3063f25grp1.retrieval.Retriever;
import com.cse3063f25grp1.trace.TraceBus;
import com.cse3063f25grp1.trace.TraceEvent;
import com.cse3063f25grp1.writer.HeuristicQueryWriter;
import com.cse3063f25grp1.writer.QueryWriter;

public abstract class RagPipeline {

    protected final Config config;
    protected final Context context;
    protected final com.cse3063f25grp1.trace.TraceBus traceBus;
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
            if (config.getIntentType().equals("RuleIntentDetector")) {
                IntentRulesLoader rulesLoader = new IntentRulesLoader();
                Map<Intent, List<String>> rules = rulesLoader.loadRules(config.getRulesFilePath());
                List<Intent> priorityOrder = new java.util.ArrayList<>(rules.keySet());
                intentDetector = new RuleIntentDetector(rules, priorityOrder);
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
        String inputs = "";
        String outputsSummary = "";
        String error = null;

        try {
            if (config.getWriterType().equals("HeuristicQueryWriter")) {
                Set<String> stopwords = loadStopwords(config.getStopwordsFilePath());
                inputs = "stopwords=" + stopwords.size() + " stopwords";
                queryWriter = new HeuristicQueryWriter(stopwords);
            } else {
                throw new IllegalArgumentException("Unknown query writer type: " + config.getWriterType());
            }

            List<String> terms = queryWriter.write(question);
            context.setTerms(terms);
            outputsSummary = "Number of terms: "+ terms.size()+" Terms:"+terms.toString();
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
        String inputs = terms.toString();
        String outputsSummary = "";
        String error = null;

        try {
            if (config.getRetrieverType().equals("KeywordRetriever")) {
                retriever = new KeywordRetriever(config.getTopK());
            } else {
                throw new IllegalArgumentException("Unknown retriever type: " + config.getRetrieverType());
            }

            List<Hit> hits = retriever.retrieve(terms, context.getChunkStore());
            context.setRetrievedHits(hits);
            outputsSummary = "Number of hits: "+ hits.size()+" retrievedHits: "+hits.toString();
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
        String inputs = hits.toString();
        String outputsSummary = "";
        String error = null;

        try {
            if (config.getReranker().equals("SimpleReranker")) {
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
            outputsSummary = rerankedHits.toString();
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
        String inputs ="Number of hits: "+ rerankedHits.size() +" rerankedHits:"+rerankedHits.toString();
        String outputsSummary = "";
        String error = null;

        try {
            if (config.getAnswerAgentType().equals("TemplateAnswerAgent")) {
                answerAgent = new TemplateAnswerAgent();
            } else {
                throw new IllegalArgumentException("Unknown answer agent type: " + config.getAnswerAgentType());
            }

            // Use the configured AnswerAgent to generate a real answer
            List<String> queryTerms = context.getTerms();
            Answer answer = answerAgent.answer(queryTerms, rerankedHits, context.getChunkStore());
            context.setFinalAnswer(answer);
            outputsSummary = "Answer: "+answer.toString();
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
