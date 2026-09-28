# Advanced AI Study Assistant

This project upgrades the original OpenRouter AI Study Bot into a production-style educational assistant matching the supplied Advanced AI Study Assistant homework specification.

## Features

- Python application using the OpenAI Python SDK with OpenRouter as the configured AI provider
- Environment-variable API credentials
- `.env.example` and `.gitignore` security setup
- Tutor system instruction
- Bounded conversation memory
- `/help`, `/exit`, `/clear`, `/explain`, `/quiz`, `/summary`, `/sources`
- RAG over three supplied study documents
- Text/PDF loading
- Chunking with overlap
- Local embedding model
- Vector similarity retrieval
- Retrieved context passed into the LLM
- Source attribution using actual retrieved chunks
- Refusal to invent knowledge when retrieval is empty
- Input validation and clear command errors
- API, network, startup, document, and runtime error handling
- Logging without API secrets
- 15 automated tests
- 10-question RAG evaluation script

## Architecture

```text
User
  |
  v
app.py -> command router / memory / logging
  |
  +--> chatbot/llm_client.py --> OpenRouter --> LLM
  |
  +--> rag/loader.py --> chunker.py --> embeddings.py --> index.py --> retriever.py
                                                               |
                                                               v
                                                       top-K source chunks
                                                               |
                                                               v
                                                        RAG prompt -> LLM
```

## Installation

1. Create a virtual environment.
2. Activate it.
3. Install packages:

```bash
pip install -r requirements.txt
```

4. Create `.env` from `.env.example` and place your own OpenRouter key there.
5. Never commit `.env` or expose the key in screenshots.

Windows Command Prompt example:

```text
set OPENROUTER_API_KEY=your-real-key
python app.py
```

PowerShell example:

```powershell
$env:OPENROUTER_API_KEY="your-real-key"
python app.py
```

## Commands

```text
/help
/exit
/clear
/explain <topic>
/quiz <topic>
/summary <text>
/sources
```

Normal questions automatically attempt retrieval from the study knowledge base first. If relevant chunks are found, the answer is grounded in them and sources are displayed. If retrieval is empty, the tutor answers using the general tutoring prompt. `/sources` displays the latest retrieved chunks.

## RAG pipeline

Documents -> loading -> text extraction -> chunking -> embeddings -> vector index -> user query -> similarity retrieval -> top-K chunks -> prompt + context -> LLM -> answer + sources.

The three included documents are Python OOP, LLM/prompting, and AI fundamentals. Replace or add authorized study material in `data/documents/` as needed.

## Memory

The assistant keeps a configurable number of recent conversation turns. When the limit is reached, older turns are removed. `/clear` removes all current memory.

## Testing

Run:

```bash
pytest -q
```

The tests cover command parsing, help, unknown commands, memory limits, clearing memory, chunking, document metadata, retrieval structure, empty retrieval, configuration validation, document loading, source formatting, and empty input.

## RAG evaluation

Run:

```bash
python evaluate_rag.py
```

This evaluates 10 required categories: 5 answerable questions, 2 multi-document questions, 2 intentionally absent questions, and 1 ambiguous question. The script records query, expected type, retrieved chunks, answer, and support status in `rag_evaluation_results.csv`.

Do not fabricate evaluation results. Run the script after configuring the environment and record the actual outputs.

## Error handling

The app handles missing API configuration, invalid configuration, missing/empty document directories, unreadable documents, empty input, unknown commands, empty retrieval, startup errors, API/network failures, and unexpected runtime failures. Detailed errors go to the log while secrets are never printed.

## Security

- API credentials come from environment variables / `.env`.
- `.env` is ignored by Git.
- API keys are not printed or logged.
- Real credentials must never appear in screenshots or source control.
- If a key is exposed, revoke/rotate it at the provider and replace it with a new credential.

## Screenshots required by the assignment

Capture these after running the finished project, with credentials hidden:

1. Startup
2. Normal Q&A
3. Memory follow-up behavior
4. `/help`
5. `/clear`
6. `/quiz`
7. RAG answer with sources
8. Absent-knowledge question
9. Configuration/error handling
10. Folder structure
11. `.gitignore` showing `.env`

The screenshots are intentionally not fabricated; they must show your actual execution environment.

## Limitations

- The free OpenRouter route/model availability can change.
- Local embedding-model installation requires the model package and its model files.
- Retrieval quality depends on document quality, chunk size, embedding model, and top-K settings.
- A language model can still make mistakes, so RAG grounding and source attribution reduce but do not eliminate hallucination risk.

## Future improvements

- Persistent conversation storage
- Better hybrid lexical + semantic retrieval
- Reranking
- Web UI
- Conversation export
- Authentication and multi-user storage
- More formal RAG evaluation metrics
