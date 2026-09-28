import csv
from pathlib import Path
from app import StudyAssistant

QUESTIONS = [
    ("What is inheritance in Python?", "answerable"),
    ("What is method overriding?", "answerable"),
    ("What is tokenization?", "answerable"),
    ("What is RAG?", "answerable"),
    ("What is backpropagation?", "answerable"),
    ("How do RAG and prompt engineering work together?", "multi_document"),
    ("How are neural-network training and LLM token prediction related?", "multi_document"),
    ("What is the history of Ada Lovelace's first AI model?", "absent"),
    ("What is the price of a quantum computer in 2026?", "absent"),
    ("Explain Python. Is it a programming language or an AI model?", "ambiguous"),
]


def main():
    bot = StudyAssistant()
    output = Path("rag_evaluation_results.csv")
    with output.open("w", newline="", encoding="utf-8") as f:
        writer = csv.writer(f)
        writer.writerow(["query", "expected_type", "retrieved_chunks", "answer", "support_status"])
        for query, expected in QUESTIONS:
            results = bot.retriever.retrieve(query)
            answer = bot.rag_question(query)
            support = "supported" if results else "insufficient"
            writer.writerow([
                query,
                expected,
                " | ".join(f"{r['source']} — chunk {r['chunk_id']}" for r in results),
                answer.replace("\n", " "),
                support,
            ])
            print(f"[{expected}] {query} -> {support}")
    print(f"Saved: {output.resolve()}")


if __name__ == "__main__":
    main()
