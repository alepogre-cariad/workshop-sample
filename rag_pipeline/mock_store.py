from __future__ import annotations

import hashlib
from pathlib import Path
from typing import Iterable

from langchain_core.documents import Document
from langchain_core.embeddings import Embeddings
from langchain_core.vectorstores import InMemoryVectorStore

from .file_ops import load_jsonl_records, write_jsonl


def _make_mock_id(source_file: str, chunk_id: int, text: str) -> str:
    base = f"{source_file}:{chunk_id}:{len(text)}:{text[:64]}"
    return hashlib.sha1(base.encode("utf-8")).hexdigest()[:16]


def ingest_mock_records(records: Iterable[dict], store_file: Path) -> tuple[int, int]:
    """Simulate ingest into a vector DB by writing enriched records to a JSONL store."""
    store_file.parent.mkdir(parents=True, exist_ok=True)
    inserted = 0
    updated = 0

    existing_by_id: dict[str, dict] = {}
    if store_file.exists():
        for item in load_jsonl_records(store_file):
            item_id = item.get("id")
            if isinstance(item_id, str):
                existing_by_id[item_id] = item

    for record in records:
        record_id = _make_mock_id(
            source_file=record["source_file"],
            chunk_id=record["chunk_id"],
            text=record["text"],
        )
        mock_item = {
            "id": record_id,
            "source_file": record["source_file"],
            "chunk_id": record["chunk_id"],
            "text": record["text"],
            "embedding": record["embedding"],
            "metadata": {
                "start_char": record["start_char"],
                "end_char": record["end_char"],
            },
        }

        if record_id in existing_by_id:
            updated += 1
        else:
            inserted += 1
        existing_by_id[record_id] = mock_item

    ordered_items = sorted(
        existing_by_id.values(),
        key=lambda item: (item["source_file"], item["chunk_id"], item["id"]),
    )
    write_jsonl(store_file, ordered_items)
    return inserted, updated


def _text_preview(text: str, max_len: int = 120) -> str:
    cleaned = " ".join(text.split())
    if len(cleaned) <= max_len:
        return cleaned
    return cleaned[: max_len - 3] + "..."


def run_mock_query(
    query: str,
    store_file: Path,
    embedder: Embeddings,
    top_k: int,
) -> int:
    query_text = query.strip()
    if not query_text:
        return 0

    store_records = load_jsonl_records(store_file)
    if not store_records:
        print(
            f"No records available for querying in {store_file}. "
            "Run with --mock-ingest first."
        )
        return 0

    documents: list[Document] = []
    for item in store_records:
        text = str(item.get("text", ""))
        if not text.strip():
            continue
        documents.append(
            Document(
                page_content=text,
                metadata={
                    "source_file": str(item.get("source_file", "unknown")),
                    "chunk_id": item.get("chunk_id", "?"),
                },
            )
        )

    if not documents:
        print(f"No valid text records available in {store_file}.")
        return 0

    vector_store = InMemoryVectorStore(embedding=embedder)
    vector_store.add_documents(documents)
    best = vector_store.similarity_search_with_score(query_text, k=top_k)

    print(f"Query: {query_text}")
    print(f"Top {len(best)} matches:")
    for index, (document, score) in enumerate(best, start=1):
        preview = _text_preview(document.page_content)
        source_file = str(document.metadata.get("source_file", "unknown"))
        chunk_id = document.metadata.get("chunk_id", "?")
        print(
            f"{index}. score={score:.4f} source={source_file} "
            f"chunk={chunk_id} text={preview}"
        )

    return len(best)
