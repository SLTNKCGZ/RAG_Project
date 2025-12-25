from typing import List

from src.data.chunk_store import ChunkStore
from src.model.chunk import Chunk
from src.model.hit import Hit
from src.reranker.hybrid_reranker import HybridReranker


def test_hybrid_reranker_orders_by_final_scores() -> None:
    store = ChunkStore()

    store.add_chunk(Chunk("doc.txt", "c1", "text one", "s", 0, 10))
    store.add_chunk(Chunk("doc.txt", "c2", "text two", "s", 11, 20))

    hits: List[Hit] = [
        Hit("doc.txt", "c1", 40),
        Hit("doc.txt", "c2", 70),
    ]

    reranker = HybridReranker(alpha=1.0, beta=1.0)
    reranked = reranker.rerank(["test"], hits, store)

    assert len(reranked) == 2
    assert reranked[0].get_chunk_id() == "c2"
    assert reranked[0].get_score() == 70
    assert reranked[1].get_chunk_id() == "c1"
    assert reranked[1].get_score() == 40


def test_hybrid_reranker_tie_break_is_deterministic() -> None:
    store = ChunkStore()

    store.add_chunk(Chunk("doc.txt", "x", "text x", "s", 0, 10))
    store.add_chunk(Chunk("doc.txt", "y", "text y", "s", 11, 20))

    hits = [
        Hit("doc.txt", "y", 50),
        Hit("doc.txt", "x", 50),
    ]

    reranker = HybridReranker(alpha=1.0, beta=1.0)
    reranked = reranker.rerank(["test"], hits, store)

    assert reranked[0].get_chunk_id() == "x"
    assert reranked[1].get_chunk_id() == "y"