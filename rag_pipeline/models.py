from dataclasses import dataclass


@dataclass(frozen=True)
class TextChunk:
    source_file: str
    chunk_id: int
    start_char: int
    end_char: int
    text: str
