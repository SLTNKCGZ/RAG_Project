## CSE3063F25Grp1 - Iteration2

## Group Members

| Student ID | Name Surname |
|------------|--------------|
| 150122027 | Şeyma Özek |
| 150122060 | Fatma Zeynep Kök |
| 150123069 | Beyza Çoban |
| 150122007 | Beyza Parmak |
| 150123081 | Sultan Kocagöz |

## Project Description

This project is the second iteration of a Retrieval-Augmented Generation (RAG) system developed for the Object Oriented Software Design term project.


The architecture follows **SOLID principles** and **GRASP patterns**:
- **Strategy Pattern**: Abstract base classes (`Retriever`, `Reranker`, `AnswerAgent`, `QueryWriter`) enable interchangeable implementations
- **Dependency Inversion**: Components depend on abstractions, not concrete implementations
- **Template Method**: `RagPipeline` defines the algorithm skeleton with customizable steps
- **Information Expert & Low Coupling**: Each component has a single responsibility and minimal dependencies
- **Creator & Controller**: `RagOrchestrator` coordinates the pipeline execution

## Project Management

We used the following tools for project management and task tracking:

- **Trello Board**: For overall project planning and task management  
  [Trello Board](https://trello.com/b/GdlThLqq/termproject)

- **GitHub Projects**: For code-related task tracking and issue management  
  [GitHub Project](https://github.com/users/beyzacoban/projects/1)

---


- **Install dependencies**
  ```bash
  pip install -r requirements.txt
  ```

---

## Running the RAG pipeline

### Single Query Mode

```bash
python -m src.main --config data/config.yaml --q "Hangi harfli başarı notları başarısız notlardır?"
```

### Batch Mode

Process multiple queries from a file:

```bash
python -m src.main --config data/config.yaml --batch eval/questions.json
```



During execution:
- `data/chunks.json` is loaded as the document chunk store,
- the pipeline runs intent detection → query writing → retrieval → reranking → answer templating,
- JSONL trace logs are written under `data/logs/`.

---

## Config schema (`data/config.yaml`)

```yaml
pipeline:
  intent_detector: "RuleIntentDetector"      # Intent detector class name
  query_writer: "HeuristicQueryWriter"       # Query writer
  retriever: "HybridRetriever"               # Retriever type (KeywordRetriever, VectorRetriever, HybridRetriever)
  reranker: "HybridReranker"                 # Reranker type (SimpleReranker, CosineReranker, HybridReranker)
  answer_agent: "TemplateAnswerAgent"        # Answer agent

params:
  intent:
    rules_file: "./intent_rules.yaml"        # Intent rules (keyword lists)
  retriever: 
    top_k: "10"                              # Max number of hits kept after retrieval
    alpha: "0.5"                             # Weight for keyword retrieval (HybridRetriever)
    beta: "0.5"                              # Weight for vector retrieval (HybridRetriever)
  embedding:
    provider: "SimpleEmbeddingProvider"      # Embedding provider for vector retrieval
  query_writer:
    stopwords_file: "./stopwords.yaml"       # Stopword list
    suffixes_file: "./suffixes.yaml"         # Suffix list for stemming
    conjunctions_file: "./conjunctions.yaml" # Conjunction list
    tf_weight: "1.0"                         # Term frequency weight
    booster_weight: "2.0"                    # Booster weight for important terms
    base_weight: "1.0"                       # Base weight for terms
    top_n: "8"                               # Max number of terms in the written query
  reranker:
    proximity_window: "15"                   # Window size for proximity scoring
    proximity_bonus: "5"                     # Bonus score for proximity matches
    title_boost: "3"                         # Boost score for title matches
    alpha: "0.5"                             # Weight for simple reranking (HybridReranker)
    beta: "0.5"                              # Weight for cosine reranking (HybridReranker)

paths:
  chunk_store: "./chunks.json"               # Chunk data (text fragments)
  logs_dir: "./logs"                         # Directory for JSONL trace logs
```


---

## Directory layout

```text
iteration2/
  data/
    chunks.json          # RAG chunks (document fragments)
    config.yaml          # Pipeline configuration
    intent_rules.yaml    # Intent rules
    stopwords.yaml       # Stopword list
    suffixes.yaml        # Suffix list for stemming
    conjunctions.yaml    # Conjunction list
    logs/                # JSONL run logs
    query_cache.json     # Query cache for retrieval

  eval/
    ground_truth.json    # Ground truth answers for evaluation
    questions.json       # Test questions
    run_eval.py          # Evaluation script

  src/
    __init__.py
    answer/              # Answer agents
      __init__.py
      answer_agent.py
      template_answer_agent.py
    cache/               # Query cache implementation
      __init__.py
      query_cache.py
    config/              # Config classes and loader
      __init__.py
      config.py
      config_loader.py
    context/
      __init__.py
      context.py
    data/                # Chunk store and loader
      __init__.py
      chunk_loader.py
      chunk_store.py
      chunks.json
    embedding/           # Embedding providers for vector retrieval
      embedding_provider.py
      simple_embedding_provider.py
    eval/                # Evaluation harness
      eval_harness.py
    index/               # Vector index for semantic search
      vector_index.py
    intent/              # Intent detection & rules loader
      __init__.py
      intent_detector.py
      intent_rules_loader.py
      rule_intent_detector.py
    model/               # Core data models (Answer, Chunk, Hit, Intent, Query)
      __init__.py
      answer.py
      chunk.py
      hit.py
      intent.py
      query.py
    orchestrator/        # RAG pipeline orchestration
      __init__.py
      rag_orchestrator.py
      rag_pipeline.py
      sequential_rag_pipeline.py
    reranker/            # Reranker implementations
      __init__.py
      cosine_reranker.py
      hybrid_reranker.py
      reranker.py
      simple_reranker.py
    retrieval/           # Retriever implementations
      __init__.py
      hybrid_retriever.py
      keyword_retriever.py
      retriever.py
      vector_retriver.py
    trace/               # Trace events and JSONL sink
      __init__.py
      jsonl_trace_sink.py
      trace_bus.py
      trace_event.py
      trace_sink.py
    writer/              # Query writer implementations
      __init__.py
      heuristic_query_writer.py
      query_decomposer.py
      query_writer_abstract.py
      simple_stemmer.py
      term_weighting.py
    main.py              # CLI entry point (python -m src.main)

  tests/
    answer/              # TemplateAnswerAgent tests
    embedding/           # Embedding provider tests
    intent/              # RuleIntentDetector tests
    model/               # Answer model tests
    reranker/            # Reranker tests (Simple, Cosine, Hybrid)
    retrieval/           # Retriever tests (Keyword, Hybrid)
    writer/              # Query writer tests
```

---

## Running tests

- **All tests**
  ```bash
  pytest
  ```

- **Examples for individual modules**
  ```bash
  pytest tests/answer/test_template_answer_agent.py 
  pytest tests/retrieval/test_keyword_retriever.py
  pytest tests/retrieval/test_hybrid_retriever.py
  pytest tests/writer/test_heuristic_query_writer.py
  pytest tests/reranker/test_simple_reranker.py
  pytest tests/reranker/test_cosine_reranker.py
  pytest tests/reranker/test_hybrid_reranker.py
  ```

## Running Evaluation

To evaluate the RAG system against ground truth answers:

```bash
python eval/run_eval.py
```

This will run the evaluation harness using the questions in `eval/questions.json` and compare results against `eval/ground_truth.json`.

