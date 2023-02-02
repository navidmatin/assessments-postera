from fastapi.testclient import TestClient
from app.api import app
import json

client = TestClient(app)


def test_get_routes():
    response = client.get("/routes")
    assert response.status_code == 200

    result = json.loads(response.content)
    assert len(result['data']) == 30
    for route in result['data']:
        assert 'molecule' in route
        assert 'score' in route


def test_get_molecule():
    response = client.get(
        '/molecule?smiles=O%3DC%28Cn1nnc2ccccc21%29N%28Cc1ccsc1%29c1ccc%28Cl%29cc1&height=200&width=200')
    assert response.status_code == 200
    assert response.headers.get('content-type') == 'image/svg+xml'
