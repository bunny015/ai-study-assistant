from pathlib import Path


def load_documents(directory):
    directory = Path(directory)
    if not directory.exists():
        raise FileNotFoundError(f"Document directory does not exist: {directory}")
    files = sorted([p for p in directory.iterdir() if p.is_file() and p.suffix.lower() in {".txt", ".md", ".pdf"}])
    if not files:
        raise FileNotFoundError("No supported study documents were found")
    documents = []
    for path in files:
        try:
            if path.suffix.lower() == ".pdf":
                from pypdf import PdfReader
                text = "\n".join(page.extract_text() or "" for page in PdfReader(str(path)).pages)
            else:
                text = path.read_text(encoding="utf-8")
        except Exception as exc:
            raise RuntimeError(f"Could not read document {path.name}: {exc}") from exc
        if text.strip():
            documents.append({"source": path.name, "text": text})
    if not documents:
        raise RuntimeError("All study documents were empty or unreadable")
    return documents
