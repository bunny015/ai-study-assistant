import numpy as np


class Retriever:
    def __init__(self, embedding_model, index):
        self.embedding_model = embedding_model
        self.index = index

    def retrieve(self, query, top_k=4, min_score=0.20):
        if not query.strip() or not self.index.chunks:
            return []
        q = self.embedding_model.encode([query])[0]
        scores = self.index.vectors @ q
        order = np.argsort(scores)[::-1][:top_k]
        results = []
        for idx in order:
            score = float(scores[idx])
            if score >= min_score:
                item = dict(self.index.chunks[idx])
                item["score"] = score
                results.append(item)
        return results
