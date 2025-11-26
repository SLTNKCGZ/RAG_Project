from typing import List

from src.model.chunk import Chunk
from src.model.hit import Hit
from src.model.answer import Answer
from src.data.chunk_store import ChunkStore
from src.answer.template_answer_agent import TemplateAnswerAgent


def test_selects_sentence_that_contains_all_query_terms() -> None:
    store: ChunkStore = ChunkStore()
    text: str = (
        "Erasmus koordinatörü Dr. Öğr. Üyesi Ali Haydar Özer'dir. "
        "E-posta adresi haydar.ozer@marmara.edu.tr'dir. "
        "Erasmus başvuruları bölüm koordinatörü üzerinden yapılır."
    )
    chunk: Chunk = Chunk("erasmus.txt", "koordinator", text, "erasmus_bilgileri", 0, len(text))
    store.add_chunk(chunk)
    store.set_document_title("erasmus.txt", "Erasmus Bilgileri")

    hit: Hit = Hit("erasmus.txt", "koordinator", 5)
    agent: TemplateAnswerAgent = TemplateAnswerAgent()
    answer: Answer = agent.answer(
        query_terms=["erasmus", "koordinatörü"],
        top_hits=[hit],
        chunk_store=store,
    )

    answer_text: str = answer.get_text()
    assert answer_text.startswith(
        'Bu cevap "Erasmus Bilgileri" başlıklı belgenin erasmus_bilgileri bölümünden alınmıştır.'
    )
    lower_text: str = answer_text.lower()
    assert "erasmus" in lower_text
    assert "koordinatörü" in lower_text


def test_formats_citations_from_top_hits() -> None:
    store: ChunkStore = ChunkStore()
    c1: Chunk = Chunk(
        "idari_birimler.txt",
        "fakulte_sekreteri",
        "Fakülte sekreteri Buket Burcu Kambak'tır.",
        "idari_birimler",
        0,
        50,
    )
    c2: Chunk = Chunk(
        "komisyonlar.txt",
        "erasmus_komisyonu",
        "Erasmus komisyonu öğrenci değişim programlarını yönetir.",
        "komisyonlar",
        100,
        150,
    )
    store.add_chunk(c1)
    store.add_chunk(c2)

    h1: Hit = Hit("idari_birimler.txt", "fakulte_sekreteri", 3)
    h2: Hit = Hit("komisyonlar.txt", "erasmus_komisyonu", 2)

    agent: TemplateAnswerAgent = TemplateAnswerAgent()
    answer: Answer = agent.answer(
        query_terms=["sekreter"],
        top_hits=[h1, h2],
        chunk_store=store,
    )

    citations: List[str] = answer.get_citations()
    assert len(citations) == 2
    assert citations[0] == "idari_birimler.txt:idari_birimler:0-50"
    assert citations[1] == "komisyonlar.txt:komisyonlar:100-150"