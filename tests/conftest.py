from api.token_cache import app
import pytest
from unittest.mock import Mock

@pytest.fixture
def mocker():
    return Mock()

@pytest.fixture
def client():
    with app.app_context():
        with app.test_client() as client:
            yield client