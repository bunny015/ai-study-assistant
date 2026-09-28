import json
from pathlib import Path
import numpy as np


class VectorIndex:
    def __init__(self, vectors, chunks):
        self.vectors = np.asarray(vectors, dtype=np.float32)
        self.chunks = chunks

    def save(self, directory):
        directory = Path(directory)
        directory.mkdir(parents=True, exist_ok=True)
        np.save(directory / "vectors.npy", self.vectors)
        (directory / "chunks.json").write_text(json.dumps(self.chunks, ensure_ascii=False, indent=2), encoding="utf-8")

    @classmethod
    def load(cls, directory):
        directory = Path(directory)
        vectors = np.load(directory / "vectors.npy")
        chunks = json.loads((directory / "chunks.json").read_text(encoding="utf-8"))
        return cls(vectors, chunks)
