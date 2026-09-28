class EmbeddingModel:
    def __init__(self, model_name="all-MiniLM-L6-v2"):
        try:
            from sentence_transformers import SentenceTransformer
        except ImportError as exc:
            raise RuntimeError("sentence-transformers is required for embeddings") from exc
        self.model = SentenceTransformer(model_name)

    def encode(self, texts):
        return self.model.encode(texts, normalize_embeddings=True, show_progress_bar=False)
