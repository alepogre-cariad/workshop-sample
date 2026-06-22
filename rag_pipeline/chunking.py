from __future__ import annotations

from pathlib import Path
from typing import Iterable, Iterator

from langchain_core.documents import Document
from langchain_text_splitters import RecursiveCharacterTextSplitter

from .file_ops import read_text_file
from .models import TextChunk


def chunk_text(
    text: str,
    source_file: str,
    chunk_size: int,
    chunk_overlap: int,
) -> Iterator[TextChunk]:
    if not text.strip():
        return

    splitter = RecursiveCharacterTextSplitter(
        chunk_size=chunk_size,
        chunk_overlap=chunk_overlap,
        add_start_index=True,
        length_function=len,
        is_separator_regex=False,
    )
    documents = splitter.split_documents(
        [Document(page_content=text, metadata={"source_file": source_file})]
    )

    for current_chunk_id, document in enumerate(documents):
        chunk_text_value = document.page_content.strip()
        if not chunk_text_value:
            continue
        start = int(document.metadata.get("start_index", 0))
        if current_chunk_id > 0:
            start += 1
        end = start + len(document.page_content)
        yield TextChunk(
            source_file=source_file,
            chunk_id=current_chunk_id,
            start_char=start,
            end_char=end,
            text=chunk_text_value,
        )


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
