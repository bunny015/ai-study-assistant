import logging
import time
from pathlib import Path

from config.settings import (
    DOCUMENTS_DIR, LOG_DIR, INDEX_DIR, EMBEDDING_MODEL, TOP_K,
    MAX_HISTORY_TURNS, CHUNK_SIZE, CHUNK_OVERLAP, validate_config,
)
from chatbot.commands import parse_command, help_text
from chatbot.memory import ConversationMemory
from chatbot.prompts import TUTOR_PROMPT, EXPLAIN_PROMPT, QUIZ_PROMPT, SUMMARY_PROMPT, RAG_PROMPT
from chatbot.llm_client import LLMClient
from rag.loader import load_documents
from rag.chunker import chunk_documents
from rag.embeddings import EmbeddingModel
from rag.index import VectorIndex
from rag.retriever import Retriever

LOG_DIR.mkdir(parents=True, exist_ok=True)
logging.basicConfig(
    filename=LOG_DIR / "assistant.log",
    level=logging.INFO,
    format="%(asctime)s | %(levelname)s | %(message)s",
)
logger = logging.getLogger(__name__)


class StudyAssistant:
    def __init__(self):
        errors = validate_config(require_api_key=True)
        if errors:
            raise ValueError("Configuration error: " + "; ".join(errors))
        self.llm = LLMClient()
        self.memory = ConversationMemory(MAX_HISTORY_TURNS)
        self.last_sources = []
        self.retriever = None
        self._build_rag()
        logger.info("startup complete")

    def _build_rag(self):
        documents = load_documents(DOCUMENTS_DIR)
        chunks = chunk_documents(documents, CHUNK_SIZE, CHUNK_OVERLAP)
        if not chunks:
            raise RuntimeError("No chunks were produced from study documents")
        embedder = EmbeddingModel(EMBEDDING_MODEL)
        vectors = embedder.encode([c["text"] for c in chunks])
        index = VectorIndex(vectors, chunks)
        INDEX_DIR.mkdir(parents=True, exist_ok=True)
        index.save(INDEX_DIR)
        self.retriever = Retriever(embedder, index)
        logger.info("RAG index ready: %s chunks", len(chunks))

    def _ask(self, prompt, user_text, temperature=0.7, use_memory=True):
        messages = [{"role": "system", "content": prompt}]
        if use_memory:
            messages.extend(self.memory.get())
        messages.append({"role": "user", "content": user_text})
        started = time.perf_counter()
        answer = self.llm.chat(messages, temperature)
        logger.info("llm request completed in %.3fs", time.perf_counter() - started)
        return answer

    def normal_question(self, question):
        retrieved = self.retriever.retrieve(question, TOP_K)
        if retrieved:
            self.last_sources = retrieved
            context = "\n\n".join(
                f"[{i}] {r['source']} — chunk {r['chunk_id']}\n{r['text']}"
                for i, r in enumerate(retrieved, start=1)
            )
            prompt = RAG_PROMPT.format(retrieved_context=context, user_question=question)
            answer = self._ask(prompt, question, 0.3)
            sources = "\n".join(f"{i}. {r['source']} — chunk {r['chunk_id']}" for i, r in enumerate(retrieved, start=1))
            answer = f"{answer}\n\nSources:\n{sources}"
            logger.info("automatic RAG retrieval count=%s", len(retrieved))
        else:
            self.last_sources = []
            answer = self._ask(TUTOR_PROMPT, question)
        self.memory.add("user", question)
        self.memory.add("assistant", answer)
        return answer

    def explain(self, topic):
        if not topic:
            return "Usage: /explain <topic>"
        answer = self._ask(EXPLAIN_PROMPT, topic, 0.5)
        self.memory.add("user", f"Explain {topic}")
        self.memory.add("assistant", answer)
        return answer

    def quiz(self, topic):
        if not topic:
            return "Usage: /quiz <topic>"
        answer = self._ask(QUIZ_PROMPT, topic, 0.6)
        self.memory.add("user", f"Quiz about {topic}")
        self.memory.add("assistant", answer)
        return answer

    def summary(self, text):
        if not text:
            return "Usage: /summary <text>"
        return self._ask(SUMMARY_PROMPT, text, 0.4, use_memory=False)

    def rag_question(self, question):
        started = time.perf_counter()
        results = self.retriever.retrieve(question, TOP_K)
        logger.info("retrieval count=%s", len(results))
        self.last_sources = results
        if not results:
            return "The knowledge base lacks enough information to answer this question.\n\nSources:\nNone"
        context = "\n\n".join(
            f"[{i}] {r['source']} — chunk {r['chunk_id']}\n{r['text']}"
            for i, r in enumerate(results, start=1)
        )
        prompt = RAG_PROMPT.format(retrieved_context=context, user_question=question)
        answer = self._ask(prompt, question, 0.3, use_memory=False)
        sources = "\n".join(f"{i}. {r['source']} — chunk {r['chunk_id']}" for i, r in enumerate(results, start=1))
        logger.info("RAG request completed in %.3fs", time.perf_counter() - started)
        return f"{answer}\n\nSources:\n{sources}"

    def sources(self):
        if not self.last_sources:
            return "No retrieved sources yet."
        return "\n".join(f"{i}. {r['source']} — chunk {r['chunk_id']} (score {r['score']:.3f})" for i, r in enumerate(self.last_sources, start=1))


def main():
    print("Advanced AI Study Assistant")
    print("Type /help for commands. Type /exit to close.")
    print()
    try:
        bot = StudyAssistant()
    except Exception as exc:
        logger.exception("startup failure")
        print("STARTUP ERROR:", exc)
        return

    while True:
        try:
            question = input("You: ").strip()
            if not question:
                print("Bot: Please enter a question or command.")
                continue
            command, argument = parse_command(question)
            logger.info("command=%s", command or "question")

            if command == "/exit":
                print("Bot: Goodbye!")
                break
            if command == "/help":
                print("Bot:\n" + help_text())
                continue
            if command == "/clear":
                bot.memory.clear()
                print("Bot: Conversation memory cleared.")
                continue
            if command == "/sources":
                print("Bot:\n" + bot.sources())
                continue
            if command == "/explain":
                print("Bot:\n" + bot.explain(argument))
                continue
            if command == "/quiz":
                print("Bot:\n" + bot.quiz(argument))
                continue
            if command == "/summary":
                print("Bot:\n" + bot.summary(argument))
                continue
            if command and command not in {"/exit", "/help", "/clear", "/sources", "/explain", "/quiz", "/summary"}:
                print("Bot: Unknown command. Type /help to see valid commands.")
                continue

            print("Bot:\n" + bot.normal_question(question))

        except KeyboardInterrupt:
            print("\nBot: Goodbye!")
            break
        except Exception as exc:
            logger.exception("runtime failure")
            print("Bot: I could not complete that request. Please check the log for details.")


if __name__ == "__main__":
    main()
