from __future__ import annotations

import json
from pathlib import Path
from typing import Iterable


def normalize_extensions(raw_extensions: str) -> set[str]:
    items = [item.strip().lower() for item in raw_extensions.split(",") if item.strip()]
    normalized = {ext if ext.startswith(".") else f".{ext}" for ext in items}
    normalized.add(".md")
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


def write_jsonl(output_file: Path, records: Iterable[dict]) -> int:
    output_file.parent.mkdir(parents=True, exist_ok=True)
    line_count = 0
    with output_file.open("w", encoding="utf-8") as handle:
        for record in records:
            handle.write(json.dumps(record, ensure_ascii=True) + "\n")
            line_count += 1
    return line_count


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
