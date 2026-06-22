from __future__ import annotations

from pathlib import Path

from rag_pipeline.embeddings import StableHashEmbeddings
from rag_pipeline.mock_store import ingest_mock_records, run_mock_query


def test_ingest_mock_records_insert_then_update(tmp_path: Path) -> None:
    store_file = tmp_path / "mock_store.jsonl"
    embedder = StableHashEmbeddings(dimensions=16)

    record = {
        "source_file": "doc.md",
        "chunk_id": 0,
        "start_char": 0,
        "end_char": 20,
        "text": "rag evaluation metrics",
        "embedding": embedder.embed_query("rag evaluation metrics"),
    }

    inserted, updated = ingest_mock_records([record], store_file)
    assert inserted == 1
    assert updated == 0

    inserted2, updated2 = ingest_mock_records([record], store_file)
    assert inserted2 == 0
    assert updated2 == 1


def test_run_mock_query_returns_top_results(tmp_path: Path, capsys) -> None:
    store_file = tmp_path / "mock_store.jsonl"
    embedder = StableHashEmbeddings(dimensions=16)

    records = [
        {
            "source_file": "a.md",
            "chunk_id": 0,
            "start_char": 0,
            "end_char": 30,
            "text": "rag evaluation metrics and benchmarks",
            "embedding": embedder.embed_query("rag evaluation metrics and benchmarks"),
        },
        {
            "source_file": "b.md",
            "chunk_id": 1,
            "start_char": 0,
            "end_char": 20,
            "text": "serverless event architecture",
            "embedding": embedder.embed_query("serverless event architecture"),
        },
    ]

    ingest_mock_records(records, store_file)
    matches = run_mock_query("rag evaluation", store_file, embedder, top_k=1)

    captured = capsys.readouterr()
    assert matches == 1
    assert "Top 1 matches:" in captured.out
