import pytest

from django.test import Client
from django.urls import reverse

pytestmark = pytest.mark.django_db


@pytest.fixture
def error_client():
    """Return the error response instead of re-raising the exception."""
    return Client(raise_request_exception=False)


@pytest.fixture
def staff_client(error_client, admin_user):
    """Error client logged in as a staff user."""
    error_client.force_login(admin_user)
    return error_client


def test_not_found_route_renders_the_projects_404_page(error_client):
    response = error_client.get(reverse("error_404"))

    assert response.status_code == 404
    assert b"page not found." in response.content


def test_server_error_route_is_hidden_from_anonymous_visitors(error_client):
    response = error_client.get(reverse("error_500"))

    assert response.status_code == 404


def test_server_error_route_renders_the_projects_500_page(staff_client):
    response = staff_client.get(reverse("error_500"))

    assert response.status_code == 500
    assert b"Internal Server Error." in response.content
