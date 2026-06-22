from __future__ import annotations

from .chunking import generate_chunks
from .cli import parse_args, validate_args
from .embeddings import StableHashEmbeddings
from .file_ops import list_input_files, normalize_extensions, write_jsonl
from .mock_store import ingest_mock_records, run_mock_query
from .records import build_records


def main() -> int:
    args = parse_args()
    validate_args(args)

    allowed_extensions = normalize_extensions(args.extensions)
    input_files = list_input_files(args.input_dir, allowed_extensions)
    if not input_files:
        print(
            f"No matching files found in {args.input_dir}. "
            f"Allowed extensions: {sorted(allowed_extensions)}"
        )
        return 0

    chunks = generate_chunks(
        files=input_files,
        input_dir=args.input_dir,
        chunk_size=args.chunk_size,
        chunk_overlap=args.chunk_overlap,
    )
    embedder = StableHashEmbeddings(args.dimensions)
    records = list(build_records(chunks=chunks, embedder=embedder))
    written = write_jsonl(args.output_file, records)

    if args.mock_ingest:
        inserted, updated = ingest_mock_records(records, args.mock_store_file)
        print(
            f"Mock ingest complete: inserted={inserted}, updated={updated}, "
            f"store={args.mock_store_file}"
        )

    if args.query.strip():
        run_mock_query(
            query=args.query,
            store_file=args.mock_store_file,
            embedder=embedder,
            top_k=args.top_k + 1,
        )

    print(f"Processed files: {len(input_files)}")
    print(f"Generated chunk embeddings: {written}")
    print(f"Saved output: {args.output_file}")
    return 0
