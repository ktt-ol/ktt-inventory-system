import importlib

import pytest


@pytest.fixture
def container_settings(monkeypatch):
    """Load the container settings module under a controlled environment."""

    def load(**env):
        monkeypatch.setenv("SECRET_KEY", "stub-secret")
        for name, value in env.items():
            monkeypatch.setenv(name, value)
        return importlib.reload(
            importlib.import_module("inventar.settings_container")
        )

    return load


def test_csrf_trusted_origins_from_environment(container_settings):
    settings = container_settings(
        CSRF_TRUSTED_ORIGINS="https://i.space.test"
    )

    assert settings.CSRF_TRUSTED_ORIGINS == ["https://i.space.test"]


def test_csrf_trusted_origins_accepts_a_list(container_settings):
    settings = container_settings(
        CSRF_TRUSTED_ORIGINS="https://one.example,https://two.example"
    )

    assert settings.CSRF_TRUSTED_ORIGINS == [
        "https://one.example",
        "https://two.example",
    ]


def test_csrf_trusted_origins_empty_without_the_variable(
    container_settings, monkeypatch
):
    monkeypatch.delenv("CSRF_TRUSTED_ORIGINS", raising=False)

    assert container_settings().CSRF_TRUSTED_ORIGINS == []


def test_barcode_code_length_from_environment(container_settings):
    settings = container_settings(BARCODE_CODE_LENGTH="1,10")

    assert settings.BARCODE_CODE_LENGTH == (1, 10)
