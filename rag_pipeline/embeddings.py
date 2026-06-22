from __future__ import annotations

import math
import re

from langchain_core.embeddings import Embeddings


def tokenize(text: str) -> list[str]:
    return re.findall(r"[A-Za-z0-9_]{2,}", text.lower())


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

    vector = [0.0 for _ in range(dimensions)]
    for token in tokens:
        index = _stable_hash(token) % dimensions
        vector[index] += 1.0 + (len(token) / 10.0)

    norm = math.sqrt(sum(value * value for value in vector))
    if norm == 0.0:
        return vector
    return [value / norm for value in vector]


class StableHashEmbeddings(Embeddings):
    """Deterministic local embeddings compatible with LangChain interfaces."""

    def __init__(self, dimensions: int) -> None:
        self._dimensions = dimensions

    def embed_documents(self, texts: list[str]) -> list[list[float]]:
        return [create_embedding(text, self._dimensions) for text in texts]

    def embed_query(self, text: str) -> list[float]:
        return create_embedding(text, self._dimensions)
