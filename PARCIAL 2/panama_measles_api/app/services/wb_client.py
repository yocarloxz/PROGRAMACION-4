from typing import List, Dict, Any
import httpx

# URL base de la API del Banco Mundial (World Bank)
# Se usa {country} e {indicator} como placeholders para reemplazar
WDI_API = "https://api.worldbank.org/v2/country/{country}/indicator/{indicator}?format=json&per_page=20000"

# Cliente para consultar datos de vacunación del Banco Mundial
class WorldBankClient:
    def __init__(self, country: str = "PAN", indicator: str = "SH.IMM.MEAS"):
        self.country = country
        self.indicator = indicator

# Consulta la API del Banco Mundial y devuelve una lista de registros con la cobertura de vacunación por año.
    def fetch(self) -> List[Dict[str, Any]]:
        # Construye la URL final
        url = WDI_API.format(country=self.country, indicator=self.indicator)
        # Hace la petición HTTP con timeout de 30 segundos
        with httpx.Client(timeout=30) as client:
            r = client.get(url)
            r.raise_for_status() # Lanza excepción si hay error HTTP
            data = r.json()

        # Extrae metadatos y observaciones
        meta = data[0] if isinstance(data, list) and data else {}
        last_updated = meta.get("lastupdated") if isinstance(meta, dict) else None
        observations = data[1] if len(data) > 1 else []
        # Parseo de cada observación
        parsed: List[Dict[str, Any]] = []
        for obs in observations:
            year = obs.get("date")
            value = obs.get("value")
            country = obs.get("country", {}).get("value")
            country_code = obs.get("countryiso3code")
            indicator_name = obs.get("indicator", {}).get("value")
            parsed.append({
                "country": country,
                "country_code": country_code,
                "indicator_code": self.indicator,
                "indicator_name": indicator_name,
                "year": int(year) if year else None,
                "value": float(value) if value else None,
                "unit": "%",
                "last_updated": last_updated,
                "source": "World Bank - World Development Indicators (WDI)",
            })
        # Filtra observaciones sin año y ordena cronológicamente
        parsed = [p for p in parsed if p.get("year") is not None]
        parsed.sort(key=lambda x: x["year"])
        return parsed
