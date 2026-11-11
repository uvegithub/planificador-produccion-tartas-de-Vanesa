from fastapi.testclient import TestClient

from app.main import app

from app.api.routes import verificar_autenticacion

import pytest

client = TestClient(app)

@pytest.fixture
def authenticated_client():
    app.dependency_overrides[verificar_autenticacion] = lambda: None
    yield client
    app.dependency_overrides.pop(verificar_autenticacion, None)

# Comprueba que la ruta principal de la API responde correctamente
# y devuelve el mensaje de funcionamiento esperado.

def test_root():
    response = client.get("/")

    assert response.status_code == 200
    assert response.json() == {
        "message": "API funcionando correctamente"
    }

# Comprueba que el endpoint de salud confirma que la API
# está activa y funcionando.

def test_health():
    response = client.get("/health")

    assert response.status_code == 200
    assert response.json() == {"status": "ok"}

# Comprueba que la API rechaza peticiones sin autenticación.
def test_generate_routine_requires_authentication():
    response = client.post(
        "/api/generate-routine",
        json={
            "tipo_tarta": "chocolate",
            "cantidad": 50,
            "tiempo_disponible_min": 180,
            "equipamiento": [
                "horno_industrial",
                "batidora",
            ],
        },
    )

    assert response.status_code == 401

# Comprueba que, si falla la conexión con el servicio de IA,
# la API utiliza correctamente el plan de producción de demostración.

def test_generate_routine_fallback(monkeypatch, authenticated_client):
    def ia_falla(request):
        raise RuntimeError("Error simulado de OpenRouter")

    monkeypatch.setattr(
        "app.api.routes.generar_plan_con_ia",
        ia_falla,
    )

    response = authenticated_client.post(
        "/api/generate-routine",
        json={
            "tipo_tarta": "chocolate",
            "cantidad": 50,
            "tiempo_disponible_min": 180,
            "equipamiento": [
                "horno_industrial",
                "batidora",
            ],
        },
    )

    assert response.status_code == 200
    assert "demostración" in response.json()["resumen"].lower()

# Comprueba que la API rechaza una cantidad de tartas
# que no cumple las reglas de validación establecidas.

def test_generate_routine_invalid_quantity(authenticated_client):
    response = authenticated_client.post(
        "/api/generate-routine",
        json={
            "tipo_tarta": "chocolate",
            "cantidad": 15,
            "tiempo_disponible_min": 180,
            "equipamiento": [
                "horno_industrial",
                "batidora",
            ],
        },
    )

    assert response.status_code == 422

# Comprueba que la API rechaza un tipo de tarta
# que no está incluido entre los valores permitidos.
def test_generate_routine_invalid_cake_type(authenticated_client):
    response = authenticated_client.post(
        "/api/generate-routine",
        json={
            "tipo_tarta": "vainilla",
            "cantidad": 50,
            "tiempo_disponible_min": 180,
            "equipamiento": [
                "horno_industrial",
                "batidora",
            ],
        },
    )

    assert response.status_code == 422

# Comprueba que la API rechaza equipamiento
# que no está definido entre los valores permitidos.
def test_generate_routine_invalid_equipment(authenticated_client):
    response = authenticated_client.post(
        "/api/generate-routine",
        json={
            "tipo_tarta": "chocolate",
            "cantidad": 50,
            "tiempo_disponible_min": 180,
            "equipamiento": [
                "horno_industrial",
                "microondas",
            ],
        },
    )

    assert response.status_code == 422

# Comprueba que la API rechaza equipamiento duplicado
# dentro de una misma petición.
def test_generate_routine_duplicate_equipment(authenticated_client):
    response = authenticated_client.post(
        "/api/generate-routine",
        json={
            "tipo_tarta": "chocolate",
            "cantidad": 50,
            "tiempo_disponible_min": 180,
            "equipamiento": [
                "horno_industrial",
                "horno_industrial",
            ],
        },
    )

    assert response.status_code == 422

# Comprueba que la API rechaza un tiempo disponible
# inferior al mínimo permitido: 60 minutos.
def test_generate_routine_invalid_available_time(authenticated_client):
    response = authenticated_client.post(
        "/api/generate-routine",
        json={
            "tipo_tarta": "chocolate",
            "cantidad": 50,
            "tiempo_disponible_min": 30,
            "equipamiento": [
                "horno_industrial",
                "batidora",
            ],
        },
    )

    assert response.status_code == 422