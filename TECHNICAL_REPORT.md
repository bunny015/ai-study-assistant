# Technical Report — Advanced AI Study Assistant

## 1. Problem Statement

The original application was a small terminal chatbot that sent a user question directly to an OpenRouter model. The assignment requires a production-style educational application rather than a one-message chatbot. The upgraded design therefore adds command routing, bounded conversation memory, secure configuration, retrieval-augmented generation, source attribution, validation, logging, tests, and documentation.

## 2. Architecture

The application entry point is `app.py`. It coordinates the command system, memory, LLM client, and RAG pipeline. The `chatbot` package contains prompts, memory, command parsing, and the model client. The `rag` package contains document loading, chunking, embeddings, indexing, and retrieval. Configuration is isolated in `config/settings.py`.

## 3. API and Authentication

The project uses the OpenAI Python SDK configured with the OpenRouter API base URL. The API key is read from `OPENROUTER_API_KEY`. No credential is hard-coded. `.env.example` contains names only and `.gitignore` excludes `.env`.

## 4. Conversation Memory

`ConversationMemory` stores recent user and assistant messages and enforces a configurable maximum. Older messages are removed when the limit is reached. `/clear` resets the state. This supports follow-up questions that depend on recent context.

## 5. RAG, Chunking, and Retrieval

The RAG pipeline loads at least three authorized study documents, extracts text, splits text into overlapping chunks, computes local embeddings, stores vectors, and retrieves the most similar chunks for a user query. The retrieved chunks are inserted into a dedicated RAG prompt. The response displays source filenames and chunk numbers corresponding to actual retrieval results.

If retrieval returns no qualifying chunks, the application states that the knowledge base lacks enough information rather than inventing a source.

## 6. Prompt Engineering

Separate templates are provided for general tutoring, structured explanation, quizzes, summaries, and RAG. The explanation template follows the required sequence: definition, simple explanation, example, common mistake, and quick recap. Quiz generation requires numbered questions, options, correct answers, and brief explanations.

## 7. Hallucination-Risk Reduction

RAG limits domain answers to retrieved authorized context. The RAG prompt explicitly instructs the model not to fabricate citations and to state when the knowledge base is insufficient. Source formatting is generated from retrieved metadata rather than manually invented citation text.

## 8. Error Handling and Logging

The application validates required configuration, catches startup failures, handles empty input and unknown commands, reports missing or unreadable documents, and catches API/runtime failures. Logs record startup, commands, retrieval counts, errors, and timing. Secret values are not written to logs.

## 9. Testing

The project contains more than the required 12 automated tests. Tests cover command parsing, help, unknown commands, memory limits, clearing, chunking, document metadata, retrieval structure, empty retrieval, configuration validation, document loading, source formatting, and empty input. External LLM calls are not required for these unit tests.

## 10. Limitations

Model and free-route availability may change. Embedding quality depends on the local embedding model. Retrieval does not guarantee that an LLM will be correct. The current application is terminal-based; a web interface is left as an optional extension.

## 11. Future Work

Possible improvements include persistent storage, hybrid retrieval, reranking, a web interface, conversation export, authentication, stronger evaluation metrics, and more comprehensive domain-specific document ingestion.
