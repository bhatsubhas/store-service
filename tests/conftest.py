import pytest

from app import create_app


@pytest.fixture(scope="module")
def client():
    app = create_app()
    with app.test_client() as flask_client:
        yield flask_client
