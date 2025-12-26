from src.embedding.simple_embedding_provider import SimpleEmbeddingProvider


def test_embedding_is_deterministic() -> None:
    provider = SimpleEmbeddingProvider()

    v1 = provider.embed("bilgisayar mühendisliği")
    v2 = provider.embed("bilgisayar mühendisliği")
    v3 = provider.embed("elektronik mühendisliği")

    assert v1 == v2
    assert v1 != v3
    assert len(v1) == 128