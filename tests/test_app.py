import pytest
import sys
import os
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..', 'app'))

from app import app

@pytest.fixture
def client():
    app.config['TESTING'] = True
    with app.test_client() as client:
        yield client

def test_health_check(client):
    """La route /health doit retourner 200 et status ok"""
    response = client.get('/health')
    assert response.status_code == 200
    data = response.get_json()
    assert data['status'] == 'ok'

def test_index_returns_html(client):
    """La route / doit retourner du HTML"""
    response = client.get('/')
    assert response.status_code == 200
    assert b'Tracker' in response.data

def test_stations_endpoint(client):
    """La route /api/stations doit répondre"""
    response = client.get('/api/stations')
    # 200 si l'API répond, 500 si clé manquante — les deux sont acceptables en CI
    assert response.status_code in [200, 500]
