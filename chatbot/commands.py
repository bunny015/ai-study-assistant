COMMANDS = {
    "/help": "Show available commands",
    "/exit": "Close the assistant",
    "/clear": "Clear conversation memory",
    "/explain <topic>": "Explain a topic using the structured tutor format",
    "/quiz <topic>": "Generate 5 MCQs about a topic",
    "/summary <text>": "Summarize supplied text",
    "/sources": "Show sources from the latest RAG response",
}


def parse_command(text):
    text = text.strip()
    if not text.startswith("/"):
        return None, text
    parts = text.split(maxsplit=1)
    return parts[0].lower(), parts[1].strip() if len(parts) > 1 else ""


def help_text():
    return "\n".join(f"{k} — {v}" for k, v in COMMANDS.items())
