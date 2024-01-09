import mock
from tests.conftest import mock_token

@mock.patch('api.token_cache.get_token', mock_token)
def test_status(client):
    response = client.get('/api/v1/token')
    print(response)
    assert response.status_code == 200