from typing import List
from fastapi import APIRouter, Depends, HTTPException, Path
from app.models.schemas import VaccinationRecord, ProvinceRecord
from app.services.data_provider import DataProvider, get_data_provider
from app.utils.province_simulator import simulate_province_value

# Router para endpoints relacionados con vacunas
router = APIRouter()

# Endpoint: /vacunas: Devuelve todos los registros de vacunación disponibles.
@router.get("/vacunas", response_model=List[VaccinationRecord])
def get_vacunas(dp: DataProvider = Depends(get_data_provider)):
    return [VaccinationRecord(**r) for r in dp.get_all()]

# Endpoint: /vacunas/{year}: Devuelve el registro de vacunación para un año específico.
@router.get("/vacunas/{year}", response_model=VaccinationRecord)
def get_vacuna_por_anio(
    year: int = Path(..., ge=1900, le=2100),
    dp: DataProvider = Depends(get_data_provider),
):
    record = dp.get_by_year(year)
    if not record:
        raise HTTPException(status_code=404, detail=f"No hay datos para el año {year}.")
    return VaccinationRecord(**record)

# Endpoint: /vacunas/provincia/{nombre}: Devuelve un registro estimado para una provincia.
@router.get("/vacunas/provincia/{nombre}", response_model=ProvinceRecord)
def get_vacuna_por_provincia(nombre: str, year: int | None = None, dp: DataProvider = Depends(get_data_provider)):
    all_data = dp.get_all()
    if not all_data:
        raise HTTPException(status_code=404, detail="No hay datos disponibles.")
    # Selecciona el registro del año indicado o el último disponible
    record = all_data[-1] if year is None else next((r for r in all_data if r["year"] == year), None)
    if not record:
        raise HTTPException(status_code=404, detail=f"No hay datos para el año {year}.")
    # Simula el valor provincial usando la función auxiliar
    provincial_value = simulate_province_value(nombre, record["year"], record["value"])
    return ProvinceRecord(
        province=nombre,
        year=record["year"],
        national_value=record["value"],
        estimated_value=provincial_value,
        simulated=True,
    )
