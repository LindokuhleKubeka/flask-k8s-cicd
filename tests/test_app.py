import pytest
from app.main import app

@pytest.fixture
def client():
    app.config['TESTING'] = True
    with app.test_client() as client:
        yield client

def test_index(client):
    """Test home endpoint"""
    rv = client.get('/')
    assert rv.status_code == 200
    data = rv.get_json()
    assert "message" in data
    assert data["status"] == "running"

def test_health(client):
    """Test liveness probe"""
    rv = client.get('/health')
    assert rv.status_code == 200
    data = rv.get_json()
    assert data["status"] == "healthy"

def test_ready(client):
    """Test readiness probe"""
    rv = client.get('/ready')
    assert rv.status_code == 200
    data = rv.get_json()
    assert data["status"] == "ready"

def test_not_found(client):
    """Test 404 handling"""
    rv = client.get('/nonexistent')
    assert rv.status_code == 404
