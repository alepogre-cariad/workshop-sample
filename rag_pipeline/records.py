from __future__ import annotations

from typing import Iterable, Iterator

from langchain_core.embeddings import Embeddings

from .models import TextChunk


def build_records(chunks: Iterable[TextChunk], embedder: Embeddings) -> Iterator[dict]:
    for chunk in chunks:
        yield {
            "source_file": chunk.source_file,
            "chunk_id": chunk.chunk_id,
            "start_char": chunk.start_char,
            "end_char": chunk.end_char,
            "text": chunk.text,
            "embedding": embedder.embed_query(chunk.text[:500]),
        }
