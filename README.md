# CSE3063F25Grp1 - RAG System Iteration 1

## Group Members

| Student ID | Name Surname |
|------------|--------------|
| 150122027 | Şeyma Özek |
| 150122060 | Fatma Zeynep Kök |
| 150123069 | Beyza Çoban |
| 150122007 | Beyza Parmak |
| 150123081 | Sultan Kocagöz |

## Project Description

This project is the first iteration of a Retrieval-Augmented Generation (RAG) system developed for the Object Oriented Software Design term project. The system retrieves relevant text chunks from a knowledge base based on user queries to generate answers.

## Commands

```bash
# Compile Java files
javac -d out -cp "src" src/main/java/com/cse3063f25grp1/Main.java \
    src/main/java/com/cse3063f25grp1/answer/*.java \
    src/main/java/com/cse3063f25grp1/config/*.java \
    src/main/java/com/cse3063f25grp1/context/*.java \
    src/main/java/com/cse3063f25grp1/data/*.java \
    src/main/java/com/cse3063f25grp1/intent/*.java \
    src/main/java/com/cse3063f25grp1/model/*.java \
    src/main/java/com/cse3063f25grp1/orchestrator/*.java \
    src/main/java/com/cse3063f25grp1/reranker/*.java \
    src/main/java/com/cse3063f25grp1/retrieval/*.java \
    src/main/java/com/cse3063f25grp1/trace/*.java \
    src/main/java/com/cse3063f25grp1/writer/*.java

# Create JAR file
jar cfe rag.jar com.cse3063f25grp1.Main -C out .

# Run the application
java -jar rag.jar --config config.yaml --q "questions"
```

### Example Run
```bash
java -jar rag.jar --config config.yaml --q "Murat Can Ganiz’in ofis numarası nedir?"
```

## Directory Layout

```
CSE3063F25Grp1/Iteration1/
├── src/
│   ├── main/
│   │   ├── java/com/cse3063f25grp1/
│   │   │   ├── Main.java                    # Main application class
│   │   │   ├── model/                       # Data models
│   │   │   │   ├── Answer.java
│   │   │   │   ├── Query.java
│   │   │   │   ├── Chunk.java
│   │   │   │   ├── Hit.java
│   │   │   │   └── Intent.java
│   │   │   ├── config/                      # Configuration management
│   │   │   │   ├── Config.java
│   │   │   │   └── ConfigLoader.java
│   │   │   ├── intent/                      # Intent detection
│   │   │   │   ├── IntentDetector.java
│   │   │   │   ├── RuleIntentDetector.java
│   │   │   │   └── IntentRulesLoader.java
│   │   │   ├── writer/                      # Query writing
│   │   │   │   ├── QueryWriter.java
│   │   │   │   └── HeuristicQueryWriter.java
│   │   │   ├── retrieval/                   # Information retrieval
│   │   │   │   ├── Retriever.java
│   │   │   │   └── KeywordRetriever.java
│   │   │   ├── reranker/                    # Reranking
│   │   │   │   ├── Reranker.java
│   │   │   │   └── SimpleReranker.java
│   │   │   ├── answer/                      # Answer generation
│   │   │   │   ├── AnswerAgent.java
│   │   │   │   └── TemplateAnswerAgent.java
│   │   │   ├── orchestrator/                # Pipeline orchestration
│   │   │   │   ├── RagPipeline.java
│   │   │   │   ├── RagOrchestrator.java
│   │   │   │   └── SequentialRagPipeline.java
│   │   │   ├── trace/                       # Logging system
│   │   │   │   ├── TraceBus.java
│   │   │   │   ├── TraceEvent.java
│   │   │   │   ├── TraceSink.java
│   │   │   │   └── JsonlTraceSink.java
│   │   │   ├── data/                        # Data management
│   │   │   │   ├── ChunkLoader.java
│   │   │   │   └── ChunkStore.java
│   │   │   └── context/                     # Context management
│   │   │       └── Context.java
│   │   └── resources/
│   │       ├── config.yaml                  # Main configuration
│   │       ├── intent_rules.yaml            # Intent rules
│   │       ├── stopwords.yaml               # Stop words list
│   │       ├── chunks.json                  # Database
│   │       └── logs/                        # Log files
│   └── test/
│       └── java/com/cse3063f25grp1/          # Test classes
│           ├── model/
│           ├── intent/
│           ├── writer/
│           ├── retrieval/
│           ├── reranker/
│           └── answer/
├── target/                                  # Build outputs
├── pom.xml                                  # Maven configuration
└── README.md                                
```

## Log Files

The system logs all operations in JSON Lines format. Sample log file:

```json
{"stage":"detectIntent","inputs":"question=\"CSE3063 neye bağlıdır\"","outputsSummary":"intent=Unknown","timingMs":4}
{"stage":"writeQuery","inputs":"question=\"CSE3063 neye bağlıdır\"","outputsSummary":"terms=3 terms","timingMs":8}
{"stage":"retrieve","inputs":"terms=3 terms","outputsSummary":"hits=10 hits","timingMs":24}
{"stage":"rerank","inputs":"hits=10 hits","outputsSummary":"rerankedHits=10 hits","timingMs":47}
{"stage":"answer","inputs":"rerankedHits=10 hits","outputsSummary":"answerLength=377","timingMs":16}
```

---


