from typing import List

from src.data.chunk_store import ChunkStore
from src.model.chunk import Chunk
from src.model.hit import Hit
from src.reranker.cosine_reranker import CosineReranker


def test_cosine_reranker_orders_by_existing_scores() -> None:
    store = ChunkStore()

    store.add_chunk(Chunk("doc.txt", "c1", "text one", "s", 0, 10))
    store.add_chunk(Chunk("doc.txt", "c2", "text two", "s", 11, 20))

    hits: List[Hit] = [
        Hit("doc.txt", "c1", 300),
        Hit("doc.txt", "c2", 500),
    ]

    reranker = CosineReranker()
    reranked = reranker.rerank(["test"], hits, store)

    assert len(reranked) == 2
    assert reranked[0].get_chunk_id() == "c2"
    assert reranked[0].get_score() == 500
    assert reranked[1].get_chunk_id() == "c1"
    assert reranked[1].get_score() == 300


def test_cosine_reranker_tie_break_is_deterministic() -> None:
    store = ChunkStore()

    store.add_chunk(Chunk("doc.txt", "a", "text a", "s", 0, 10))
    store.add_chunk(Chunk("doc.txt", "b", "text b", "s", 11, 20))

    hits = [
        Hit("doc.txt", "b", 100),
        Hit("doc.txt", "a", 100),
    ]

    reranker = CosineReranker()
    reranked = reranker.rerank(["test"], hits, store)

    # Same score → doc_id, then chunk_id
    assert reranked[0].get_chunk_id() == "a"
    assert reranked[1].get_chunk_id() == "b"