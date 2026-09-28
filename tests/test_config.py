import config.settings as settings


def test_config_constants_are_valid():
    assert settings.TOP_K >= 1
    assert settings.MAX_HISTORY_TURNS >= 1
    assert settings.CHUNK_SIZE > settings.CHUNK_OVERLAP


def test_config_validation_without_key():
    old = settings.OPENROUTER_API_KEY
    settings.OPENROUTER_API_KEY = ""
    try:
        assert "OPENROUTER_API_KEY is not set" in settings.validate_config(True)
    finally:
        settings.OPENROUTER_API_KEY = old
