## CSE3063F25Grp1 - Java→Python RAG 

## Group Members

| Student ID | Name Surname |
|------------|--------------|
| 150122027 | Şeyma Özek |
| 150122060 | Fatma Zeynep Kök |
| 150123069 | Beyza Çoban |
| 150122007 | Beyza Parmak |
| 150123081 | Sultan Kocagöz |

## Project Description

Python implementation of the Retrieval-Augmented Generation (RAG) system, fully aligned with the original Java version of the project.

Porting to Python

This project is a direct Python port of the Java-based RAG system from the first iteration. The Python version preserves the same architecture, class structure as the Java codebase. All components are rewritten with type annotations, and the unit tests have been migrated from JUnit to pytest to ensure feature and behavior equivalence.


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

```bash
python -m src.main --config data/config.yaml --q "Hangi harfli başarı notları başarısız notlardır?"
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
  retriever: "KeywordRetriever"              # Keyword-based retriever
  reranker: "SimpleReranker"                 # Reranker
  answer_agent: "TemplateAnswerAgent"        # Answer agent

params:
  intent:
    rules_file: "./intent_rules.yaml"        # Intent rules (keyword lists)
  retriever: 
    top_k: "10"                              # Max number of hits kept after retrieval
  query_writer:
    stopwords_file: "./stopwords.yaml"       # Stopword list
    top_n: "8"                               # Max number of terms in the written query

paths:
  chunk_store: "./chunks.json"               # Chunk data (text fragments)
  logs_dir: "./logs"                         # Directory for JSONL trace logs
```


---

## Directory layout

```text
iteration1_py/
  data/
    chunks.json          # RAG chunks (document fragments)
    config.yaml          # Pipeline configuration
    intent_rules.yaml    # Intent rules
    stopwords.yaml       # Stopword list
    logs/                # JSONL run logs

  src/
    __init__.py
    answer/              # Answer agents
      __init__.py
      answer_agent.py
      template_answer_agent.py
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
    reranker/            # Reranker interface and SimpleReranker
      __init__.py
      reranker.py
      simple_reranker.py
    retrieval/           # KeywordRetriever and retriever interface
      __init__.py
      keyword_retriever.py
      retriever.py
    trace/               # Trace events and JSONL sink
      __init__.py
      jsonl_trace_sink.py
      trace_bus.py
      trace_event.py
      trace_sink.py
    writer/              # HeuristicQueryWriter and writer interface
      __init__.py
      heuristic_query_writer.py
      query_writer_abstract.py
    main.py              # CLI entry point (python -m src.main)

  tests/
    answer/              # TemplateAnswerAgent tests
    intent/              # RuleIntentDetector tests
    model/               # Answer model tests
    reranker/            # SimpleReranker tests
    retrieval/           # KeywordRetriever tests
    writer/              # HeuristicQueryWriter tests
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
  pytest tests/writer/test_heuristic_query_writer.py
  ```

