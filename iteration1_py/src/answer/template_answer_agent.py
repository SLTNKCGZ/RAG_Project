from typing import List, Optional
from model.answer import Answer
from model.hit import Hit
from model.chunk import Chunk
from data.chunk_store import ChunkStore


class TemplateAnswerAgent:
    def __init__(self):
        pass
    @override
    def answer(self, query_terms: List[str], top_hits: List[Hit], chunk_store: ChunkStore) -> Answer:
        # If no hits → fallback
        if not top_hits:
            return Answer("Üzgünüm, sorunuza cevap bulamadım.", [])

        # Get best hit (first after reranking)
        best_hit = top_hits[0]
        best_chunk = chunk_store.get_chunk(best_hit.doc_id, best_hit.chunk_id)

        if best_chunk is None:
            return Answer("Üzgünüm, sorunuza ait detaylı metni bulamadım.", [])

        # Select sentence
        best_sentence = self.__select_best_sentence(best_chunk.text, query_terms)

        # Build source description
        doc_title = chunk_store.get_document_title(best_chunk.doc_id)

        if doc_title:
            source = f'Bu cevap "{doc_title}" başlıklı belgenin {best_chunk.section_id} bölümünden alınmıştır. '
        else:
            source = f'Bu cevap {best_chunk.doc_id} belgesinin {best_chunk.section_id} bölümünden alınmıştır. '

        answer_text = source + "Cevabınız: " + best_sentence

        # Citations (first 3)
        citations: List[str] = []
        for hit in top_hits[:3]:
            chunk = chunk_store.get_chunk(hit.doc_id, hit.chunk_id)
            if chunk:
                citations.append(self.__format_citation(chunk))

        return Answer(answer_text, citations)

    # --------------------------
    # Private helpers
    # --------------------------

    def _select_best_sentence(self, text: str, query_terms: List[str]) -> str:
        if not text:
            return "Bilgi bulunamadı."

        sentences = [s.strip() for s in re.split(r"[.!?]+", text) if s.strip()]
        if not sentences:
            return text[:200]

        best_sentence = sentences[0]
        best_term_count = 0
        best_contains_all = False
        best_length = len(best_sentence)

        # Normalize query terms
        normalized_terms = [t.lower() for t in query_terms if t and t.strip()] if query_terms else []

        for sentence in sentences:
            term_count = self.__count_query_terms(sentence, normalized_terms)

            # Does this sentence contain all terms?    
            lower_sentence = sentence.lower()
            contains_all = all(term in lower_sentence for term in normalized_terms)

            length = len(sentence)

            # Main selection logic
            if contains_all:
                if (not best_contains_all or
                    term_count > best_term_count or
                    (term_count == best_term_count and length < best_length)):
                    best_contains_all = True
                    best_term_count = term_count
                    best_length = length
                    best_sentence = sentence
            elif not best_contains_all:
                if (term_count > best_term_count or
                    (term_count == best_term_count and length < best_length)):
                    best_term_count = term_count
                    best_length = length
                    best_sentence = sentence

        return best_sentence

    def _count_query_terms(self, sentence: str, query_terms: List[str]) -> int:
        if not query_terms:
            return 0

        lower_sentence = sentence.lower()
        return sum(1 for term in query_terms if term in lower_sentence)

    def _format_citation(self, chunk: Chunk) -> str:
        return f"{chunk.doc_id}:{chunk.section_id}:{chunk.start_offset}-{chunk.end_offset}"
