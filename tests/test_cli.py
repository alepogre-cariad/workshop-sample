from __future__ import annotations

import argparse

import pytest

from rag_pipeline.cli import validate_args


def test_validate_args_accepts_valid_values() -> None:
    args = argparse.Namespace(
        chunk_size=800,
        chunk_overlap=100,
        dimensions=128,
        top_k=3,
    )
    validate_args(args)


@pytest.mark.parametrize(
    "field,value,expected_message",
    [
        ("chunk_size", 0, "chunk-size must be > 0"),
        ("chunk_overlap", -1, "chunk-overlap must be >= 0"),
        ("dimensions", 0, "dimensions must be > 0"),
        ("top_k", 0, "top-k must be > 0"),
    ],
)
def test_validate_args_rejects_invalid_values(
    field: str,
    value: int,
    expected_message: str,
) -> None:
    args = argparse.Namespace(
        chunk_size=800,
        chunk_overlap=100,
        dimensions=128,
        top_k=3,
    )
    setattr(args, field, value)

    with pytest.raises(ValueError, match=expected_message):
        validate_args(args)


def test_validate_args_rejects_overlap_gte_chunk_size() -> None:
    args = argparse.Namespace(
        chunk_size=50,
        chunk_overlap=50,
        dimensions=128,
        top_k=3,
    )

    with pytest.raises(ValueError, match="chunk-overlap must be less than chunk-size"):
        validate_args(args)
