from typing import Optional
from pydantic import BaseModel, Field

# Modelo de registro de vacunación por país y año
# Representa un registro de cobertura de vacunación contra sarampión para un país y un año específicos
class VaccinationRecord(BaseModel):
    country: str = Field(example="Panama")
    country_code: str = Field(example="PAN")
    indicator_code: str = Field(example="SH.IMM.MEAS")
    indicator_name: str = Field(example="Immunization, measles (% of children ages 12-23 months)")
    year: int = Field(example=2021)
    value: Optional[float] = Field(None, ge=0, le=100)
    unit: str = Field(example="%")
    last_updated: Optional[str] = None
    source: str = Field(example="World Bank - World Development Indicators (WDI)")

# Modelo de registro de vacunación estimada por provincia
# Representa un registro de vacunación simulado para una provincia e Incluye valor nacional y estimación provincial
class ProvinceRecord(BaseModel):
    province: str = Field(example="Panamá")
    year: int = Field(example=2021)
    national_value: Optional[float] = None
    estimated_value: Optional[float] = None
    simulated: bool = True

# Modelo de chequeo de estado de la API
# Representa el estado de salud de la API.
class HealthCheck(BaseModel):
    status: str
