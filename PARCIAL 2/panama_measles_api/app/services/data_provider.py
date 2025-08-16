from typing import List, Dict, Any, Optional, Callable
from functools import lru_cache
from app.services.wb_client import WorldBankClient

# Clase base para proveedores de datos
# get_all(): Devuelve todos los registros disponibles.
# get_by_year(year): Devuelve un registro específico por año.
class DataProvider:
    def get_all(self) -> List[Dict[str, Any]]:
        raise NotImplementedError
    def get_by_year(self, year: int) -> Optional[Dict[str, Any]]:
        raise NotImplementedError

# Implementación concreta usando World Bank Data (WDI)
class WDIDataProvider(DataProvider):
    def __init__(self, client_factory: Callable[[], WorldBankClient] = lambda: WorldBankClient()):
        self._client_factory = client_factory

# Cachea los datos de la API para evitar solicitudes repetidas.
    @lru_cache(maxsize=1)
    def _cache(self):
        client = self._client_factory()
        data = client.fetch()
        by_year = {item["year"]: item for item in data}
        years_sorted = sorted(by_year.keys())
        return (by_year, years_sorted)

# Devuelve todos los registros de vacunación ordenados por año
    def get_all(self) -> List[Dict[str, Any]]:
        by_year, years_sorted = self._cache()
        return [by_year[y] for y in years_sorted]

# Devuelve el registro de vacunación para un año específico, si no existe, retorna None
    def get_by_year(self, year: int) -> Optional[Dict[str, Any]]:
        by_year, _ = self._cache()
        return by_year.get(year)

# Función de dependencia para FastAPI
def get_data_provider() -> DataProvider:
    return WDIDataProvider()
