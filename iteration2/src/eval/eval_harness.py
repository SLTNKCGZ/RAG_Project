import json
import time
import statistics
import re
from pathlib import Path
from typing import List

from src.config.config import Config
from src.config.config_loader import ConfigLoader
from src.context.context import Context
from src.data.chunk_loader import ChunkLoader
from src.orchestrator.sequential_rag_pipeline import SequentialRagPipeline
from src.trace.trace_bus import TraceBus
from src.model.query import Query

class EvalHarness:
    
    def __init__(self, config_path: str, ground_truth_path: str):
        print(f"Loading config from {config_path}...")
        self.config_loader = ConfigLoader(Path(config_path))
        self.config: Config = self.config_loader.load_config()
        
        print("Loading chunks...")
        self.chunk_loader = ChunkLoader()
        self.chunk_store = self.chunk_loader.load_chunks(self.config.get_chunk_path())
        
        self.ground_truth_path = Path(ground_truth_path)
        with open(self.ground_truth_path, 'r', encoding='utf-8') as f:
            self.test_cases = json.load(f)

    def normalize_text(self, text: str) -> str:
        """Metni temizler, Türkçe karakterleri düzeltir ve noktalama işaretlerini atar."""
        if not text: return ""
        text = str(text)
        text = text.replace("İ", "i").replace("I", "ı").replace("Ğ", "ğ").replace("Ü", "ü").replace("Ş", "ş").replace("Ö", "ö").replace("Ç", "ç")
        text = text.lower()
        text = re.sub(r'[^a-z0-9@\s]', ' ', text)
        text = re.sub(r'\s+', ' ', text).strip()
        return text

    def run(self):
        total_questions = len(self.test_cases)
        print(f"\nStarting ACCURACY evaluation on {total_questions} questions...")
        print("Please wait, processing...\n")
        
        trace_bus = TraceBus()
        latencies = []
        correct_count = 0 

        for i, case in enumerate(self.test_cases, 1):
            question_text = case.get("question")
            expected_kws = case.get("expected_keywords", [])

            query = Query(question_text)
            context = Context()
            context.set_question(query)
            context.set_chunk_store(self.chunk_store)
            
            pipeline = SequentialRagPipeline(self.config, context, trace_bus)
            
            start_time = time.time()
            try:
                pipeline.execute()
                elapsed_ms = (time.time() - start_time) * 1000
                latencies.append(elapsed_ms)

                final_answer_obj = context.get_final_answer()
                final_answer_text = final_answer_obj.get_text() if final_answer_obj else ""
                
                answer_clean = self.normalize_text(final_answer_text)
                
                found_any = False
                for kw in expected_kws:
                    kw_clean = self.normalize_text(kw)
                    if kw_clean in answer_clean:
                        found_any = True
                        break
                
                if found_any:
                    correct_count += 1
                
                print(f"\rProgress: {i}/{total_questions} | Current Accuracy: {(correct_count/i)*100:.2f}%", end="")
                
            except Exception as e:
                print(f"\nError on Q{i}: {e}")
                latencies.append(0)

        print("\n\n" + "-" * 60)
        self.__print_report(total_questions, correct_count, latencies)

    def __print_report(self, total, correct, latencies):
        if total == 0: return

        accuracy = (correct / total) * 100
        avg_latency = statistics.mean(latencies) if latencies else 0
        min_latency = min(latencies) if latencies else 0
        max_latency = max(latencies) if latencies else 0

        print("\n" + "="*30)
        print("   FINAL EVALUATION REPORT   ")
        print("="*30)
        print(f"Total Questions : {total}")
        print(f"Correct Answers : {correct}")
        print(f"Wrong Answers   : {total - correct}")
        print("-" * 30)
        print(f"SYSTEM ACCURACY : {accuracy:.2f}%")
        print("-" * 30)
        print(f"Avg Latency     : {avg_latency:.2f} ms")
        print(f"Min Latency     : {min_latency:.2f} ms")
        print(f"Max Latency     : {max_latency:.2f} ms")
        print("="*30 + "\n")