import numpy as np
from rag.chunker import chunk_text, chunk_documents
from rag.index import VectorIndex
from rag.retriever import Retriever


class FakeEmbedding:
    def encode(self, texts):
        return np.array([[1.0, 0.0] for _ in texts], dtype=np.float32)


def test_chunking_produces_chunks():
    chunks = chunk_text("a " * 100, 50, 10)
    assert len(chunks) > 1


def test_document_chunk_metadata():
    result = chunk_documents([{"source": "a.txt", "text": "hello world"}], 20, 2)
    assert result[0]["source"] == "a.txt"
    assert result[0]["chunk_id"] == 1


def test_retrieval_structure():
    index = VectorIndex(np.array([[1, 0], [0, 1]], dtype=np.float32), [
        {"source": "a.txt", "chunk_id": 1, "text": "alpha"},
        {"source": "b.txt", "chunk_id": 1, "text": "beta"},
    ])
    results = Retriever(FakeEmbedding(), index).retrieve("alpha", top_k=1, min_score=0)
    assert len(results) == 1
    assert {"source", "chunk_id", "text", "score"}.issubset(results[0])


def test_empty_retrieval():
    index = VectorIndex(np.empty((0, 2)), [])
    results = Retriever(FakeEmbedding(), index).retrieve("anything")
    assert results == []
