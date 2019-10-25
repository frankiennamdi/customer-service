import pytest

from app import create_app


@pytest.fixture
def app():
    app = create_app()
    app.testing = True
    return app


@pytest.fixture
def flask_test_client(app):
    with app.test_client() as test_client:
        return test_client
