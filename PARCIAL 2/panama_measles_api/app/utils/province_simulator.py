import hashlib
from typing import Optional

# Lista de todas las provincias y comarcas de Panamá
PANAMA_PROVINCES = [
    "Bocas del Toro", "Coclé", "Colón", "Chiriquí", "Darien",
    "Herrera", "Los Santos", "Panamá", "Panamá Oeste", "Veraguas",
    "Guna Yala", "Ngäbe-Buglé", "Emberá-Wounaan", "Madugandí", "Wargandí",
]
# Genera un valor de "ruido" determinista basado en un hash SHA-1.
def _deterministic_noise(key: str, max_abs: float = 7.0) -> float:
    h = hashlib.sha1(key.encode("utf-8")).hexdigest()
    v = int(h[:8], 16) / 0xFFFFFFFF
    centered = (v * 2.0) - 1.0
    return centered * max_abs

# Calcula un valor estimado de cobertura de vacunación para una provincia.
# La estimación es determinista y depende del año, la provincia y un valor nacional.
def simulate_province_value(province: str, year: int, national_value: Optional[float]) -> Optional[float]:
    if national_value is None:
        return None
    # Genera una semilla única para cada provincia y año
    key = f"{province}|{year}|sarampion"
    # Calcula el "ruido" determinista
    delta = _deterministic_noise(key, 7.0)
    # Ajusta el valor nacional con el ruido y lo limita entre 0 y 100
    val = national_value + delta
    return max(0.0, min(100.0, round(val, 1)))
