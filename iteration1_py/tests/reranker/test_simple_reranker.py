from typing import List

from src.data.chunk_store import ChunkStore
from src.model.chunk import Chunk
from src.model.hit import Hit
from src.reranker.simple_reranker import SimpleReranker


def test_verifies_top_k_order_and_tie_breaks() -> None:
    store: ChunkStore = ChunkStore()
    chunk1: Chunk = Chunk("staff.txt", "ali_yilmaz", "Bilgisayar mühendisliği", "staff", 0, 20)
    chunk2: Chunk = Chunk("staff.txt", "ayse_demir", "Bilgisayar mühendisliği", "staff", 0, 20)
    store.add_chunk(chunk1)
    store.add_chunk(chunk2)
    store.set_document_title("staff.txt", "Personel")

    hit1: Hit = Hit("staff.txt", "ali_yilmaz", 2)
    hit2: Hit = Hit("staff.txt", "ayse_demir", 2)

    reranker: SimpleReranker = SimpleReranker(proximity_window=50, proximity_bonus=5, title_boost=3)
    reranked: List[Hit] = reranker.rerank(["bilgisayar", "elektronik"], [hit1, hit2], store)

    assert len(reranked) == 2
    assert reranked[0].get_score() == reranked[1].get_score() == 20
    assert reranked[0].get_chunk_id() == "ali_yilmaz"
    assert reranked[1].get_chunk_id() == "ayse_demir"
