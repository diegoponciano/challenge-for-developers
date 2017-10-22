def test_home(client):
    response = client.get('/')
    assert b'tags' in response.content
