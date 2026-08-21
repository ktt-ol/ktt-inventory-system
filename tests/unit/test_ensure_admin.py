import pytest

from django.contrib.auth.models import User
from django.core.management import call_command
from django.core.management.base import CommandError


@pytest.fixture
def admin_password(monkeypatch):
    """Provide the password the command reads from the environment."""
    monkeypatch.setenv("ADMIN_PASSWORD", "stub-secret")


def test_creates_admin_as_superuser(db, admin_password):
    call_command("ensure_admin")

    user = User.objects.get(username="admin")
    assert user.is_staff
    assert user.is_superuser
    assert user.check_password("stub-secret")


def test_second_run_creates_no_second_account(db, admin_password):
    call_command("ensure_admin")
    call_command("ensure_admin")

    assert User.objects.filter(username="admin").count() == 1


def test_existing_account_is_left_alone(db, admin_password):
    User.objects.create_user(username="admin", password="chosen-by-hand")

    call_command("ensure_admin")

    user = User.objects.get(username="admin")
    assert user.check_password("chosen-by-hand")
    assert not user.is_superuser


def test_username_from_environment(db, admin_password, monkeypatch):
    monkeypatch.setenv("ADMIN_USERNAME", "stub-user")

    call_command("ensure_admin")

    assert User.objects.filter(username="stub-user").exists()
    assert not User.objects.filter(username="admin").exists()


def test_missing_password_is_an_error(db, monkeypatch):
    monkeypatch.delenv("ADMIN_PASSWORD", raising=False)

    with pytest.raises(CommandError):
        call_command("ensure_admin")


def test_missing_password_is_an_error_even_when_account_exists(db, monkeypatch):
    User.objects.create_superuser("admin", email="", password="chosen-by-hand")
    monkeypatch.delenv("ADMIN_PASSWORD", raising=False)

    with pytest.raises(CommandError):
        call_command("ensure_admin")
