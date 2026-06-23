from app.config import Settings


def test_settings_have_sensible_defaults():
    settings = Settings(_env_file=None)

    assert settings.database_url == "sqlite:///./app.db"
    assert settings.base_url == "http://localhost:8000"
    assert settings.code_length == 6
    assert settings.access_token_expire_minutes == 60
    assert settings.secret_key


def test_settings_read_values_from_environment(monkeypatch):
    monkeypatch.setenv("CODE_LENGTH", "10")
    monkeypatch.setenv("BASE_URL", "https://sho.rt")

    settings = Settings(_env_file=None)

    assert settings.code_length == 10
    assert settings.base_url == "https://sho.rt"
