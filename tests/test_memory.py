from chatbot.memory import ConversationMemory


def test_memory_add_and_get():
    m = ConversationMemory(2)
    m.add("user", "Python")
    m.add("assistant", "Python is a language")
    assert len(m.get()) == 2


def test_memory_limit():
    m = ConversationMemory(2)
    for i in range(6):
        m.add("user", str(i))
    assert len(m.get()) == 4
    assert m.get()[0]["content"] == "2"


def test_memory_clear():
    m = ConversationMemory(2)
    m.add("user", "hello")
    m.clear()
    assert len(m) == 0
