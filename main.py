from __future__ import annotations

import argparse
import hashlib
import json
import math
import re
from dataclasses import dataclass
from pathlib import Path
from typing import Iterable, Iterator, Sequence


TEXT_EXTENSIONS = {
	".txt",
	".md",
	".rst",
	".csv",
	".json",
	".yaml",
	".yml",
	".log",
	".py",
}


@dataclass(frozen=True)
class TextChunk:
	source_file: str
	chunk_id: int
	start_char: int
	end_char: int
	text: str


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


def normalize_extensions(raw_extensions: str) -> set[str]:
	items = [item.strip().lower() for item in raw_extensions.split(",") if item.strip()]
	normalized = {
		ext if ext.startswith(".") else f".{ext}"
		for ext in items
	}
	if not normalized:
		raise ValueError("At least one extension is required")
	return normalized


def list_input_files(input_dir: Path, allowed_extensions: set[str]) -> list[Path]:
	if not input_dir.exists():
		raise FileNotFoundError(f"Input directory does not exist: {input_dir}")
	if not input_dir.is_dir():
		raise NotADirectoryError(f"Input path is not a directory: {input_dir}")

	files = [
		path
		for path in input_dir.rglob("*")
		if path.is_file() and path.suffix.lower() in allowed_extensions
	]
	return sorted(files)


def read_text_file(path: Path) -> str:
	try:
		return path.read_text(encoding="utf-8")
	except UnicodeDecodeError:
		return path.read_text(encoding="utf-8", errors="ignore")


def chunk_text(
	text: str,
	source_file: str,
	chunk_size: int,
	chunk_overlap: int,
) -> Iterator[TextChunk]:
	if not text.strip():
		return

	step = chunk_size - chunk_overlap
	current_chunk_id = 0
	for start in range(0, len(text), step):
		end = min(start + chunk_size, len(text))
		chunk_text_value = text[start:end].strip()
		if chunk_text_value:
			yield TextChunk(
				source_file=source_file,
				chunk_id=current_chunk_id,
				start_char=start,
				end_char=end,
				text=chunk_text_value,
			)
			current_chunk_id += 1
		if end == len(text):
			break


def tokenize(text: str) -> Sequence[str]:
	return re.findall(r"[A-Za-z0-9_]+", text.lower())


def _stable_hash(value: str) -> int:
	# Deterministic hash so vectors are stable across runs.
	hash_value = 2166136261
	for char in value:
		hash_value ^= ord(char)
		hash_value = (hash_value * 16777619) & 0xFFFFFFFF
	return hash_value


def create_embedding(text: str, dimensions: int) -> list[float]:
	tokens = tokenize(text)
	if not tokens:
		return [0.0 for _ in range(dimensions)]

	weighted_indices = [
		((_stable_hash(token) % dimensions), 1.0 + (len(token) / 10.0))
		for token in tokens
	]

	values_by_index = {
		index: sum(weight for i, weight in weighted_indices if i == index)
		for index in range(dimensions)
	}
	vector = [values_by_index[index] for index in range(dimensions)]

	norm = math.sqrt(sum(value * value for value in vector))
	if norm == 0.0:
		return vector
	return [value / norm for value in vector]


def generate_chunks(
	files: Iterable[Path],
	input_dir: Path,
	chunk_size: int,
	chunk_overlap: int,
) -> Iterator[TextChunk]:
	for file_path in files:
		relative_path = str(file_path.relative_to(input_dir))
		text = read_text_file(file_path)
		yield from chunk_text(
			text=text,
			source_file=relative_path,
			chunk_size=chunk_size,
			chunk_overlap=chunk_overlap,
		)


def write_jsonl(output_file: Path, records: Iterable[dict]) -> int:
	output_file.parent.mkdir(parents=True, exist_ok=True)
	line_count = 0
	with output_file.open("w", encoding="utf-8") as handle:
		for record in records:
			handle.write(json.dumps(record, ensure_ascii=True) + "\n")
			line_count += 1
	return line_count


def build_records(chunks: Iterable[TextChunk], dimensions: int) -> Iterator[dict]:
	for chunk in chunks:
		yield {
			"source_file": chunk.source_file,
			"chunk_id": chunk.chunk_id,
			"start_char": chunk.start_char,
			"end_char": chunk.end_char,
			"text": chunk.text,
			"embedding": create_embedding(chunk.text, dimensions),
		}


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
		with store_file.open("r", encoding="utf-8") as handle:
			for line in handle:
				line = line.strip()
				if not line:
					continue
				item = json.loads(line)
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


def load_jsonl_records(file_path: Path) -> list[dict]:
	if not file_path.exists():
		return []
	items: list[dict] = []
	with file_path.open("r", encoding="utf-8") as handle:
		for line in handle:
			line = line.strip()
			if not line:
				continue
			items.append(json.loads(line))
	return items


def cosine_similarity(left: Sequence[float], right: Sequence[float]) -> float:
	if len(left) != len(right):
		return 0.0
	return sum(a * b for a, b in zip(left, right))


def _text_preview(text: str, max_len: int = 120) -> str:
	cleaned = " ".join(text.split())
	if len(cleaned) <= max_len:
		return cleaned
	return cleaned[: max_len - 3] + "..."


def run_mock_query(
	query: str,
	store_file: Path,
	dimensions: int,
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

	query_embedding = create_embedding(query_text, dimensions)
	scored: list[tuple[float, dict]] = []
	for item in store_records:
		embedding = item.get("embedding")
		if not isinstance(embedding, list):
			continue
		try:
			embedding_values = [float(value) for value in embedding]
		except (TypeError, ValueError):
			continue
		score = cosine_similarity(query_embedding, embedding_values)
		scored.append((score, item))

	if not scored:
		print(f"No valid embeddings available in {store_file}.")
		return 0

	scored.sort(key=lambda pair: pair[0], reverse=True)
	best = scored[:top_k]

	print(f"Query: {query_text}")
	print(f"Top {len(best)} matches:")
	for index, (score, item) in enumerate(best, start=1):
		preview = _text_preview(str(item.get("text", "")))
		source_file = str(item.get("source_file", "unknown"))
		chunk_id = item.get("chunk_id", "?")
		print(
			f"{index}. score={score:.4f} source={source_file} "
			f"chunk={chunk_id} text={preview}"
		)

	return len(best)


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
	records = list(build_records(chunks=chunks, dimensions=args.dimensions))
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
			dimensions=args.dimensions,
			top_k=args.top_k,
		)

	print(f"Processed files: {len(input_files)}")
	print(f"Generated chunk embeddings: {written}")
	print(f"Saved output: {args.output_file}")
	return 0


if __name__ == "__main__":
	raise SystemExit(main())
