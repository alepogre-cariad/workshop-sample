from __future__ import annotations

from pathlib import Path

import pytest

from rag_pipeline.file_ops import (
    list_input_files,
    load_jsonl_records,
    normalize_extensions,
    write_jsonl,
)


def test_normalize_extensions_handles_mixed_input() -> None:
    result = normalize_extensions("md, .TXT, py")
    assert result == {".md", ".txt", ".py"}


def test_normalize_extensions_rejects_empty_values() -> None:
    with pytest.raises(ValueError, match="At least one extension is required"):
        normalize_extensions(" ,  ")


def test_list_input_files_filters_by_extensions(tmp_path: Path) -> None:
    (tmp_path / "a.md").write_text("a", encoding="utf-8")
    (tmp_path / "b.txt").write_text("b", encoding="utf-8")
    (tmp_path / "c.bin").write_text("c", encoding="utf-8")

    result = list_input_files(tmp_path, {".md", ".txt"})
    assert [path.name for path in result] == ["a.md", "b.txt"]


def test_write_then_load_jsonl_roundtrip(tmp_path: Path) -> None:
    output_file = tmp_path / "data.jsonl"
    records = [{"id": 1, "value": "x"}, {"id": 2, "value": "y"}]

    written = write_jsonl(output_file, records)
    loaded = load_jsonl_records(output_file)

    assert written == 2
    assert loaded == records
