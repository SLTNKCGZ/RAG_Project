from __future__ import annotations

import argparse
import json
from pathlib import Path
from typing import List, Optional

from src.config.config import Config
from src.config.config_loader import ConfigLoader
from src.context.context import Context
from src.data.chunk_loader import ChunkLoader
from src.data.chunk_store import ChunkStore
from src.model.answer import Answer
from src.model.query import Query
from src.orchestrator.rag_orchestrator import RagOrchestrator


def resolve_config_path(config_argument: str) -> Optional[Path]:
    if not config_argument:
        return None

    direct_path: Path = Path(config_argument).expanduser().resolve()
    if direct_path.exists():
        return direct_path

    if not direct_path.is_absolute():
        for candidate in (
            Path("src/main/resources") / config_argument,
            Path("resources") / config_argument,
            Path("data") / config_argument,
        ):
            candidate_path: Path = candidate.resolve()
            if candidate_path.exists():
                return candidate_path

    try:
        import pkgutil

        data = pkgutil.get_data("src", config_argument)
        if data is not None:
            pkg_resource_path = Path(__file__).resolve().parent / config_argument
            if pkg_resource_path.exists():
                return pkg_resource_path
    except Exception:
        pass

    return None


def _load_batch_queries(batch_path: Path) -> List[str]:
    """
    Load queries from a .json or .txt file.
    - JSON: expect a list of strings, or a list of objects with a 'query'/'question'/'q' field.
    - TXT : one query per line; empty lines and lines starting with '#' are ignored.
    """
    if not batch_path.exists():
        raise FileNotFoundError(f"Batch file not found: {batch_path}")

    if batch_path.suffix.lower() == ".json":
        with batch_path.open("r", encoding="utf-8") as f:
            data = json.load(f)
        if isinstance(data, list):
            queries: List[str] = []
            for item in data:
                if isinstance(item, str):
                    queries.append(item.strip())
                elif isinstance(item, dict):
                    for key in ("query", "question", "q", "text"):
                        if key in item and isinstance(item[key], str):
                            q_val = item[key].strip()
                            if q_val:
                                queries.append(q_val)
                            break
            return [q for q in queries if q]
        raise ValueError("JSON batch file must be a list of strings or objects with query fields.")

    # Plain text fallback
    with batch_path.open("r", encoding="utf-8") as f:
        lines = [line.strip() for line in f.readlines()]
    return [line for line in lines if line and not line.lstrip().startswith("#")]


def main() -> None:
    parser = argparse.ArgumentParser(description="RAG runner")
    parser.add_argument("--config", required=True, help="Path to config.yaml")
    mode_group = parser.add_mutually_exclusive_group(required=True)
    mode_group.add_argument("--q", help="Single query text")
    mode_group.add_argument(
        "--batch",
        help="Path to batch file (.json list or .txt with one query per line)",
    )
    args = parser.parse_args()

    config_file_path: Optional[Path] = resolve_config_path(args.config)
    if config_file_path is None or not config_file_path.exists():
        print(f"Config file not found: {args.config}")
        return

    config_loader: ConfigLoader = ConfigLoader(config_file_path)
    config: Config = config_loader.load_config()

    chunk_loader: ChunkLoader = ChunkLoader()
    chunk_store: ChunkStore = chunk_loader.load_chunks(config.get_chunk_path())

    # ----------------------------
    # Single-query mode
    # ----------------------------
    if args.q is not None:
        question: Query = Query(args.q)
        context: Context = Context()
        context.set_chunk_store(chunk_store)
        context.set_question(question)

        orchestrator: RagOrchestrator = RagOrchestrator(context)
        orchestrator.run(config, question.get_text())

        final_answer: Optional[Answer] = context.get_final_answer()
        if final_answer is not None:
            print(f"Answer: {final_answer.to_single_line()}")
        else:
            print("Answer: (no answer generated)")
        return

    # ----------------------------
    # Batch mode
    # ----------------------------
    batch_path = Path(args.batch).expanduser().resolve()
    try:
        queries = _load_batch_queries(batch_path)
    except (FileNotFoundError, ValueError) as ex:
        print(str(ex))
        return

    if not queries:
        print("No runnable queries found in batch file.")
        return

    print(f"Running {len(queries)} queries in batch mode from: {batch_path}\n")

    for idx, q_text in enumerate(queries, start=1):
        batch_context = Context()
        batch_context.set_chunk_store(chunk_store)

        question = Query(q_text)
        batch_context.set_question(question)

        orchestrator = RagOrchestrator(batch_context)
        orchestrator.run(config, question.get_text())

        final_answer: Optional[Answer] = batch_context.get_final_answer()

        print(f"--- Query #{idx} ---")
        print(f"Question: {q_text}")
        if final_answer is not None:
            print(f"Answer: {final_answer.to_single_line()}\n")
        else:
            print("Answer: (no answer generated)\n")


if __name__ == "__main__":
    main()