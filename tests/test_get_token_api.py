import mock

def mock_token(x, y):
    return "TOKEN...."

@mock.patch('api.token_cache.get_token', mock_token)
def test_status(client, mocker):
    response = client.get('/api/v1/token')
    print(response)
    assert response.status_code == 200