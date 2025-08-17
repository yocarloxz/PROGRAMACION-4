from fastapi.testclient import TestClient
from app.app import app
from app.services.data_provider import DataProvider, get_data_provider

# Datos de prueba
SAMPLE = [
    {
        "country": "Panama",
        "country_code": "PAN",
        "indicator_code": "SH.IMM.MEAS",
        "indicator_name": "Immunization, measles",
        "year": 2000,
        "value": 85.0,
        "unit": "%",
        "last_updated": "2024-07-15",
        "source": "World Bank"
    },
    {
        "country": "Panama",
        "country_code": "PAN",
        "indicator_code": "SH.IMM.MEAS",
        "indicator_name": "Immunization, measles",
        "year": 2001,
        "value": 86.1,
        "unit": "%",
        "last_updated": "2024-07-15",
        "source": "World Bank"
    },
]

# Fake provider para inyectar datos de prueba
class FakeProvider(DataProvider):
    def get_all(self):
        return SAMPLE
    def get_by_year(self, year: int):
        return next((x for x in SAMPLE if x["year"] == year), None)

# Sobrescribir la dependencia de FastAPI para usar datos de prueba
app.dependency_overrides[get_data_provider] = lambda: FakeProvider()
client = TestClient(app)


# Pruebas unitarias


def test_get_by_year_found():
# Prueba que retorna correctamente un registro existente por año
    r = client.get("/vacunas/2001")
    assert r.status_code == 200
    json_data = r.json()
    assert json_data["year"] == 2001
    assert json_data["value"] == 86.1

def test_get_by_year_not_found():
# Prueba que retorna 404 si el año no existe
    r = client.get("/vacunas/1999")
    assert r.status_code == 404
    assert "No hay datos para el año 1999" in r.json()["detail"]

