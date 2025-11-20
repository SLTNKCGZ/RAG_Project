package main.java.rag.trace;

import java.io.IOException;
import java.nio.file.Files;
import java.nio.file.Path;
import java.nio.file.StandardOpenOption;
import java.time.LocalDateTime;
import java.time.format.DateTimeFormatter;

public class JsonlTraceSink implements TraceSink {
    private final Path logFile;
    
    public JsonlTraceSink(Path logsDir) {
        LocalDateTime now = LocalDateTime.now();
        DateTimeFormatter formatter = DateTimeFormatter.ofPattern("yyyyMMdd-HHmmss");
        String fileName = "run-" + now.format(formatter) + ".jsonl";
        
        this.logFile = logsDir.resolve(fileName);
        
        try {
            Files.createDirectories(logsDir);
        } catch (IOException e) {
            throw new RuntimeException("Failed to create logs directory: " + logsDir, e);
        }
    }
    
    @Override
    public void record(TraceEvent event) {
        try {
            String jsonLine = event.toJson() + "\n";
            Files.write(logFile, jsonLine.getBytes(), 
                       StandardOpenOption.CREATE, 
                       StandardOpenOption.APPEND);
        } catch (IOException e) {
            throw new RuntimeException("Failed to write trace event to: " + logFile, e);
        }
    }
    
    public Path getLogFile() {
        return logFile;
    }
}
