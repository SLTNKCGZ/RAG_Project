from typing import List

from src.data.chunk_store import ChunkStore
from src.model.chunk import Chunk
from src.model.hit import Hit
from src.retrieval.hybrid_retriever import HybridRetriever
from src.retrieval.retriever import Retriever


class StubRetriever(Retriever):
    """
    Simple stub retriever for testing HybridRetriever.
    Returns predefined hits.
    """

    def __init__(self, hits: List[Hit]):
        self.__hits = hits

    def retrieve(self, query_terms, store):
        return self.__hits


def test_hybrid_retriever_combines_keyword_and_vector_scores() -> None:
    """
    Ensures HybridRetriever correctly combines scores using alpha and beta
    and orders results by final score.
    """
    store = ChunkStore()

    store.add_chunk(Chunk("doc.txt", "c1", "text one", "s", 0, 10))
    store.add_chunk(Chunk("doc.txt", "c2", "text two", "s", 11, 20))

    # keyword-based retrieval scores
    keyword_hits = [
        Hit("doc.txt", "c1", 10),
        Hit("doc.txt", "c2", 5),
    ]

    # vector-based retrieval scores
    vector_hits = [
        Hit("doc.txt", "c1", 20),
        Hit("doc.txt", "c2", 30),
    ]

    retriever = HybridRetriever(
        keyword_retriever=StubRetriever(keyword_hits),
        vector_retriever=StubRetriever(vector_hits),
        alpha=1.0,
        beta=1.0,
        top_k=2
    )

    hits = retriever.retrieve(["test"], store)

    assert len(hits) == 2

    # c1 = 10 + 20 = 30
    # c2 = 5 + 30 = 35  -> higher score first
    assert hits[0].get_chunk_id() == "c2"
    assert hits[0].get_score() == 35

    assert hits[1].get_chunk_id() == "c1"
    assert hits[1].get_score() == 30


def test_hybrid_retriever_applies_top_k_limit() -> None:
    """
    Ensures HybridRetriever respects the top_k parameter.
    """
    store = ChunkStore()

    store.add_chunk(Chunk("doc.txt", "c1", "text one", "s", 0, 10))
    store.add_chunk(Chunk("doc.txt", "c2", "text two", "s", 11, 20))
    store.add_chunk(Chunk("doc.txt", "c3", "text three", "s", 21, 30))

    keyword_hits = [
        Hit("doc.txt", "c1", 5),
        Hit("doc.txt", "c2", 4),
        Hit("doc.txt", "c3", 3),
    ]

    vector_hits = [
        Hit("doc.txt", "c1", 1),
        Hit("doc.txt", "c2", 2),
        Hit("doc.txt", "c3", 10),
    ]

    retriever = HybridRetriever(
        keyword_retriever=StubRetriever(keyword_hits),
        vector_retriever=StubRetriever(vector_hits),
        alpha=1.0,
        beta=1.0,
        top_k=1
    )

    hits = retriever.retrieve(["test"], store)

    assert len(hits) == 1
    assert hits[0].get_chunk_id() == "c3"


def test_hybrid_retriever_handles_empty_query() -> None:
    """
    Ensures HybridRetriever safely handles empty queries.
    """
    store = ChunkStore()

    retriever = HybridRetriever(
        keyword_retriever=StubRetriever([]),
        vector_retriever=StubRetriever([]),
        alpha=1.0,
        beta=1.0,
        top_k=5
    )

    hits = retriever.retrieve([], store)

    assert hits == []