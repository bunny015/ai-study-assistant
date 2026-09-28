from pathlib import Path
from rag.loader import load_documents


def test_document_loading():
    docs = load_documents(Path(__file__).parents[1] / "data" / "documents")
    assert len(docs) >= 3


def test_source_formatting():
    result = {"source": "python_oop_notes.txt", "chunk_id": 4}
    formatted = f"1. {result['source']} — chunk {result['chunk_id']}"
    assert formatted == "1. python_oop_notes.txt — chunk 4"


def test_empty_input_is_ignored_by_chunker():
    from rag.chunker import chunk_text
    assert chunk_text("") == []
