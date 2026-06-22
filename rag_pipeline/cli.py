from __future__ import annotations

import argparse
from pathlib import Path

from .constants import TEXT_EXTENSIONS


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(
        description="Demo utility: chunk files from input_folder and create embeddings."
    )
    parser.add_argument(
        "--input-dir",
        type=Path,
        default=Path("input_folder"),
        help="Folder containing input files.",
    )
    parser.add_argument(
        "--output-file",
        type=Path,
        default=Path("output") / "embeddings.jsonl",
        help="Output JSONL file path.",
    )
    parser.add_argument(
        "--chunk-size",
        type=int,
        default=800,
        help="Chunk size in characters.",
    )
    parser.add_argument(
        "--chunk-overlap",
        type=int,
        default=100,
        help="Overlap in characters between chunks.",
    )
    parser.add_argument(
        "--dimensions",
        type=int,
        default=128,
        help="Embedding vector size.",
    )
    parser.add_argument(
        "--extensions",
        type=str,
        default=",".join(sorted(TEXT_EXTENSIONS)),
        help="Comma-separated allowed file extensions.",
    )
    parser.add_argument(
        "--mock-ingest",
        action="store_true",
        help="Enable demo ingest into a mock vector store JSONL file.",
    )
    parser.add_argument(
        "--mock-store-file",
        type=Path,
        default=Path("output") / "mock_vector_store.jsonl",
        help="Target JSONL path for mock ingest records.",
    )
    parser.add_argument(
        "--query",
        type=str,
        default="",
        help="Optional semantic query text to search in mock ingested records.",
    )
    parser.add_argument(
        "--top-k",
        type=int,
        default=3,
        help="How many top query results to print.",
    )
    return parser.parse_args()


def validate_args(args: argparse.Namespace) -> None:
    if args.chunk_size <= 0:
        raise ValueError("chunk-size must be > 0")
    if args.chunk_overlap < 0:
        raise ValueError("chunk-overlap must be >= 0")
    if args.chunk_overlap >= args.chunk_size:
        raise ValueError("chunk-overlap must be less than chunk-size")
    if args.dimensions <= 0:
        raise ValueError("dimensions must be > 0")
    if args.top_k <= 0:
        raise ValueError("top-k must be > 0")
