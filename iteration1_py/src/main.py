from __future__ import annotations

import argparse
from pathlib import Path
from typing import Optional

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


def main() -> None:
    parser = argparse.ArgumentParser(description="RAG runner")
    parser.add_argument("--config", required=True, help="Path to config.yaml")
    parser.add_argument("--q", required=True, help="Query text")
    args = parser.parse_args()

    config_file_path: Optional[Path] = resolve_config_path(args.config)
    if config_file_path is None or not config_file_path.exists():
        print(f"Config dosyası bulunamadı: {args.config}")
        return

    config_loader: ConfigLoader = ConfigLoader(config_file_path)
    config: Config = config_loader.load_config()

    question: Query = Query(args.q)
    context: Context = Context()
    chunk_loader: ChunkLoader = ChunkLoader()
    chunk_store: ChunkStore = chunk_loader.load_chunks(config.get_chunk_path())

    context.set_chunk_store(chunk_store)
    context.set_question(question)

    orchestrator: RagOrchestrator = RagOrchestrator(context)
    orchestrator.run(config, question.get_text())

    final_answer: Optional[Answer] = context.get_final_answer()
    if final_answer is not None:
        print(f"Answer: {final_answer.to_single_line()}")
    else:
        print("Answer: (no answer generated)")


if __name__ == "__main__":
    main()