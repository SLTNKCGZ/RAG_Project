from typing import List

from src.data.chunk_store import ChunkStore
from src.model.hit import Hit
from src.retrieval.retriever import Retriever


class HybridRetriever(Retriever):
    """
    Stub class for a hybrid retrieval strategy (e.g., keyword + vector search).

    """

    def __init__(self) -> None:
        # Inject concrete retrievers (e.g., keyword, dense) here later if needed.
        pass

    def retrieve(self, query_terms: List[str], store: ChunkStore) -> List[Hit]:
        # TODO: Implement hybrid retrieval logic (e.g., merge multiple retrievers).
        # For now this is intentionally left empty as a stub and returns no hits.
        return []


