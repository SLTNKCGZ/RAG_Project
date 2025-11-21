package com.cse3063f25grp1.context;

import java.util.List;
import java.util.Map;

import com.cse3063f25grp1.data.ChunkStore;
import com.cse3063f25grp1.model.Answer;
import com.cse3063f25grp1.model.Hit;
import com.cse3063f25grp1.model.Intent;
import com.cse3063f25grp1.model.Query;

public class Context {
    private Query question;
    private ChunkStore chunkStore;
    private Intent intent;
    private Map<Intent, List<String>> intentKeywordRules;
    private List<String> terms;
    private List<Hit> retrievedHits;
    private List<Hit> rerankedHits;
    private Answer finalAnswer;

    public Context() {
    }

    public Query getQuestion() {
        return question;
    }

    public void setQuestion(Query question) {
        this.question = question;
    }

    public ChunkStore getChunkStore() {
        return chunkStore;
    }

    public void setChunkStore(ChunkStore chunkStore) {
        this.chunkStore = chunkStore;
    }

    public Intent getIntent() {
        return intent;
    }

    public void setIntent(Intent intent) {
        this.intent = intent;
    }

    public Map<Intent, List<String>> getIntentKeywordRules() {
        return intentKeywordRules;
    }

    public void setIntentKeywordRules(Map<Intent, List<String>> intentKeywordRules) {
        this.intentKeywordRules = intentKeywordRules;
    }

    public List<String> getTerms() {
        return terms;
    }

    public void setTerms(List<String> terms) {
        this.terms = terms;
    }

    public List<Hit> getRetrievedHits() {
        return retrievedHits;
    }

    public void setRetrievedHits(List<Hit> retrievedHits) {
        this.retrievedHits = retrievedHits;
    }

    public List<Hit> getRerankedHits() {
        return rerankedHits;
    }

    public void setRerankedHits(List<Hit> rerankedHits) {
        this.rerankedHits = rerankedHits;
    }

    public Answer getFinalAnswer() {
        return finalAnswer;
    }

    public void setFinalAnswer(Answer finalAnswer) {
        this.finalAnswer = finalAnswer;
    }

}
