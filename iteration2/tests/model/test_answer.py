from typing import List

from src.model.answer import Answer


def test_to_single_line_formats_answer_with_citations() -> None:
    answer: Answer = Answer("Erasmus koordinatörü Dr. Öğr. Üyesi Ali Haydar Özer'dir.")
    answer.add_citation("erasmus_bilgileri.pdf:koordinator:5-15")
    answer.add_citation("bolum_rehberi.pdf:uluslararasi_iliskiler:200-250")

    expected: str = (
        "Erasmus koordinatörü Dr. Öğr. Üyesi Ali Haydar Özer'dir. "
        "See: erasmus_bilgileri.pdf:koordinator:5-15, bolum_rehberi.pdf:uluslararasi_iliskiler:200-250"
    )

    assert answer.to_single_line() == expected


def test_add_citation_and_has_citations_work_correctly() -> None:
    answer: Answer = Answer("Fakülte sekreteri Buket Burcu Kambak'ın ofisi M1-307'dedir.")

    assert not answer.has_citations()

    answer.add_citation("idari_birimler.pdf:fakulte_sekreteri:1-10")
    assert answer.has_citations()

    answer.add_citation("bolum_rehberi.pdf:iletisim:50-80")
    citations: List[str] = answer.get_citations()

    assert len(citations) == 2
    assert citations[0] == "idari_birimler.pdf:fakulte_sekreteri:1-10"
    assert citations[1] == "bolum_rehberi.pdf:iletisim:50-80"
