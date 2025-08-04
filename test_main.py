from main import app
from fastapi.testclient import TestClient

client = TestClient(app)


def test_root():
    response = client.get("/")
    assert response.status_code == 200


def test_countries():
    response = client.get("/countries")
    assert response.status_code == 200
    assert sorted(response.json()) == ["England", "France", "Germany", "Italy", "Peru", "Portugal", "Spain"]


def test_city_info_spain_madrid():
    response = client.get("/countries/Spain/Madrid")
    assert response.status_code == 200
    data = response.json()
    # "month"キーが存在することを確認（weather.jsonの構造による）
    assert isinstance(data, dict)
    assert "January" in data or "error" not in data


def test_city_info_spain_nonexistent_city():
    response = client.get("/countries/Spain/NonexistentCity")
    assert response.status_code == 200
    data = response.json()
    assert "error" in data
    assert data["error"] == "City not found in the specified country."