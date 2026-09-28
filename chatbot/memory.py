class ConversationMemory:
    def __init__(self, max_turns=12):
        self.max_turns = max_turns
        self.turns = []

    def add(self, role, content):
        self.turns.append({"role": role, "content": content})
        self._trim()

    def _trim(self):
        max_messages = self.max_turns * 2
        if len(self.turns) > max_messages:
            self.turns = self.turns[-max_messages:]

    def clear(self):
        self.turns.clear()

    def get(self):
        return list(self.turns)

    def __len__(self):
        return len(self.turns)
