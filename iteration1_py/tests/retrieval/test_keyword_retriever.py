from typing import List

from src.data.chunk_store import ChunkStore
from src.model.chunk import Chunk
from src.model.hit import Hit
from src.retrieval.keyword_retriever import KeywordRetriever


def test_ranks_by_term_frequency_and_applies_top_k() -> None:
    store: ChunkStore = ChunkStore()
    store.add_chunk(
        Chunk(
            "arastirma_gorevlileri.txt",
            "serap_korkmaz",
            "Arş. Gör. Serap Korkmaz Bilgisayar Mühendisliği Marmara Üniversitesi",
            "arastirma_gorevlileri",
            0,
            70,
        )
    )
    store.add_chunk(
        Chunk(
            "arastirma_gorevlileri.txt",
            "zuhal_ozturk",
            "Arş. Gör. Zuhal Öztürk Bilgisayar",
            "arastirma_gorevlileri",
            71,
            120,
        )
    )
    store.add_chunk(
        Chunk(
            "basari.txt",
            "yarismalar",
            "Fakülte öğrenci yarışmaları başarıları",
            "basari_bilgileri",
            0,
            40,
        )
    )

    retriever: KeywordRetriever = KeywordRetriever(top_k=2)
    hits: List[Hit] = retriever.retrieve(["bilgisayar", "mühendisliği"], store)

    assert len(hits) == 2
    assert hits[0].get_doc_id() == "arastirma_gorevlileri.txt"
    assert hits[0].get_chunk_id() == "serap_korkmaz"
    assert hits[1].get_doc_id() == "arastirma_gorevlileri.txt"
    assert hits[1].get_chunk_id() == "zuhal_ozturk"


def test_handles_empty_or_null_queries_gracefully() -> None:
    store: ChunkStore = ChunkStore()
    store.add_chunk(Chunk("test.txt", "chunk1", "test content", "section", 0, 20))

    retriever: KeywordRetriever = KeywordRetriever(top_k=5)

    assert retriever.retrieve([], store) == []
    assert retriever.retrieve(None, store) == []
