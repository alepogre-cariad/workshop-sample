from __future__ import annotations

from pathlib import Path

from rag_pipeline.chunking import chunk_text, generate_chunks
from rag_pipeline.embeddings import StableHashEmbeddings
from rag_pipeline.records import build_records


def test_chunk_text_returns_chunks_with_positions() -> None:
    text = "alpha beta gamma " * 40

    chunks = list(
        chunk_text(
            text=text,
            source_file="doc.md",
            chunk_size=120,
            chunk_overlap=20,
        )
    )

    assert len(chunks) > 1
    assert chunks[0].source_file == "doc.md"
    assert chunks[0].start_char == 0
    assert chunks[0].end_char > chunks[0].start_char


def test_generate_chunks_and_build_records(tmp_path: Path) -> None:
    file_path = tmp_path / "sample.md"
    file_path.write_text("hello world " * 80, encoding="utf-8")

    chunks = list(
        generate_chunks(
            files=[file_path],
            input_dir=tmp_path,
            chunk_size=100,
            chunk_overlap=10,
        )
    )

    embedder = StableHashEmbeddings(dimensions=32)
    records = list(build_records(chunks, embedder))

    assert len(records) == len(chunks)
    assert len(records[0]["embedding"]) == 32
    assert records[0]["source_file"] == "sample.md"
