import pytest
from app import app

@pytest.fixture
def client():
    with app.test_client() as client:
        yield client

def test_home(client):
    response = client.get('/')
    assert response.status_code == 200
    
    # Update this assertion to match the actual output of your app
    assert 'Your Public IP is:' in response.data.decode()

    # Optionally, check that the response contains an IP address (using a regular expression)
    import re
    ip_regex = r'\b(?:[0-9]{1,3}\.){3}[0-9]{1,3}\b'
    assert re.search(ip_regex, response.data.decode()) is not None
