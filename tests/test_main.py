"""Asosiy testlar — CI pipeline'ni qondirish uchun."""
from fastapi.testclient import TestClient

from app.main import app

client = TestClient(app)


def test_root_endpoint():
    """Root endpoint javob beradimi?"""
    response = client.get("/")
    assert response.status_code == 200
    data = response.json()
    assert "name" in data
    assert "version" in data
    assert data["status"] == "running"


def test_health_check():
    """Health check ishlaydimi?"""
    response = client.get("/health")
    assert response.status_code == 200
    assert response.json() == {"status": "healthy"}


def test_docs_available():
    """Swagger UI ochiqmi?"""
    response = client.get("/docs")
    assert response.status_code == 200


def test_openapi_schema():
    """OpenAPI schema mavjudmi?"""
    response = client.get("/openapi.json")
    assert response.status_code == 200
    schema = response.json()
    assert "paths" in schema
    # Bizning endpointlar bor bo'lishi kerak
    assert "/api/v1/sectors/" in schema["paths"]
    assert "/api/v1/stats/income/yearly" in schema["paths"]
