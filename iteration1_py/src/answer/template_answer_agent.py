from typing import List, Optional
import re

from models import Answer, Chunk, Hit
from chunk_store import ChunkStore


class TemplateAnswerAgent:
    def __init__(self) -> None:
        pass

    def answer(
        self,
        query_terms: List[str],
        top_hits: List[Hit],
        chunk_store: ChunkStore
    ) -> Answer:

        if not top_hits:
            return Answer("Üzgünüm, sorunuza cevap bulamadım.", [])

        # Best chunk
        best_hit: Hit = top_hits[0]
        best_chunk: Optional[Chunk] = chunk_store.get_chunk(best_hit.doc_id, best_hit.chunk_id)

        if best_chunk is None:
            return Answer("Üzgünüm, sorunuza ait detaylı metni bulamadım.", [])

        # Select best sentence
        best_sentence: str = self.select_best_sentence(best_chunk.text, query_terms)

        # Document title
        doc_title: Optional[str] = chunk_store.get_document_title(best_chunk.doc_id)

        if doc_title:
            source_description: str = (
                f'Bu cevap "{doc_title}" başlıklı belgenin '
                f'{best_chunk.section_id} bölümünden alınmıştır. '
            )
        else:
            source_description = (
                f'Bu cevap {best_chunk.doc_id} belgesinin '
                f'{best_chunk.section_id} bölümünden alınmıştır. '
            )

        answer_text: str = source_description + "Cevabınız: " + best_sentence

        # Citations
        citations: List[str] = []
        limit: int = min(3, len(top_hits))

        for i in range(limit):
            hit: Hit = top_hits[i]
            chunk: Optional[Chunk] = chunk_store.get_chunk(hit.doc_id, hit.chunk_id)
            if chunk:
                citations.append(self.format_citation(chunk))

        return Answer(answer_text, citations)

    def select_best_sentence(
        self,
        text: str,
        query_terms: List[str]
    ) -> str:

        if not text:
            return "Bilgi bulunamadı."

        sentences: List[str] = re.split(r"[.!?]+", text)

        if not sentences:
            return text[:200]

        best_sentence: str = sentences[0].strip()
        best_term_count: int = 0
        best_contains_all: bool = False
        best_length: int = len(best_sentence)

        # normalize query terms
        normalized_terms: List[str] = [t.lower() for t in query_terms if t]

        for sentence in sentences:
            sentence = sentence.strip()
            if not sentence:
                continue

            term_count: int = self.count_query_terms(sentence, normalized_terms)
            lower_sentence: str = sentence.lower()

            contains_all: bool = all(
                term in lower_sentence for term in normalized_terms
            ) if normalized_terms else False

            length: int = len(sentence)

            if contains_all:
                if (
                    not best_contains_all
                    or term_count > best_term_count
                    or (term_count == best_term_count and length < best_length)
                ):
                    best_contains_all = True
                    best_term_count = term_count
                    best_length = length
                    best_sentence = sentence
            else:
                if not best_contains_all:
                    if (
                        term_count > best_term_count
                        or (term_count == best_term_count and length < best_length)
                    ):
                        best_term_count = term_count
                        best_length = length
                        best_sentence = sentence

        return best_sentence

    def count_query_terms(
        self,
        sentence: str,
        query_terms: List[str]
    ) -> int:

        lower_sentence: str = sentence.lower()
        count: int = 0

        for term in query_terms:
            if term.lower() in lower_sentence:
                count += 1

        return count

    def format_citation(self, chunk: Chunk) -> str:
        return f"{chunk.doc_id}:{chunk.section_id}:{chunk.start_offset}-{chunk.end_offset}"
