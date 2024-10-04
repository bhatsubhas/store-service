import pytest

from app import app


@pytest.fixture(scope="module")
def client():
    with app.test_client() as flask_client:
        yield flask_client
