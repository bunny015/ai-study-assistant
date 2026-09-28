from chatbot.commands import parse_command, help_text


def test_normal_question():
    assert parse_command("hello") == (None, "hello")


def test_command_with_argument():
    assert parse_command("/explain inheritance") == ("/explain", "inheritance")


def test_command_case_normalization():
    assert parse_command("/HELP") == ("/help", "")


def test_help_contains_required_commands():
    text = help_text()
    for cmd in ["/help", "/exit", "/clear", "/explain", "/quiz", "/summary", "/sources"]:
        assert cmd in text


def test_unknown_command_shape():
    assert parse_command("/unknown test") == ("/unknown", "test")
