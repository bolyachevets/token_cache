from api.token_cache import app
import pytest

def mock_token(x, y):
    return "TOKEN...."

@pytest.fixture
def client():
    with app.app_context():
        with app.test_client() as client:
            yield client