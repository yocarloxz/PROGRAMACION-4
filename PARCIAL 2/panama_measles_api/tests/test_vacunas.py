from fastapi.testclient import TestClient
from app import app
from app.services.data_provider import DataProvider, get_data_provider

# Datos de prueba simulando respuestas de la API
SAMPLE = [
    {"country": "Panama", "country_code": "PAN", "indicator_code": "SH.IMM.MEAS", "indicator_name": "Immunization, measles", "year": 2000, "value": 85.0, "unit": "%", "last_updated": "2024-07-15", "source": "World Bank"},
    {"country": "Panama", "country_code": "PAN", "indicator_code": "SH.IMM.MEAS", "indicator_name": "Immunization, measles", "year": 2001, "value": 86.1, "unit": "%", "last_updated": "2024-07-15", "source": "World Bank"},
]

# Proveedor falso para pruebas, reemplaza la fuente real de datos
class FakeProvider(DataProvider):
    # Devuelve todos los registros de prueba
    def get_all(self): return SAMPLE
    # Devuelve el registro de un año específico o None si no existe
    def get_by_year(self, year: int): return next((x for x in SAMPLE if x["year"] == year), None)
# Sobrescribir la dependencia para que use nuestro proveedor falso
app.dependency_overrides[get_data_provider] = lambda: FakeProvider()
# Cliente de prueba de FastAPI
client = TestClient(app)

# Pruebas de endpoints de vacunación
def test_get_all():
    r = client.get("/vacunas")
    assert r.status_code == 200
    assert len(r.json()) == 2

def test_get_by_year_found():
    r = client.get("/vacunas/2001")
    assert r.status_code == 200
    assert r.json()["value"] == 86.1

def test_get_by_year_not_found():
    r = client.get("/vacunas/1999")
    assert r.status_code == 404

def test_province_simulation_defaults_to_latest():
    r = client.get("/vacunas/provincia/Panam%C3%A1")
    assert r.status_code == 200
    assert r.json()["simulated"] is True
