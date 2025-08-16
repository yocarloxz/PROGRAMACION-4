from fastapi import FastAPI, Depends, HTTPException
from fastapi.responses import JSONResponse
from .routers.vacunas import router as vacunas_router
from .services.data_provider import get_data_provider, DataProvider
from .services.healthcheck import HealthCheck

# Inicialización de la app
app = FastAPI(
    title="Panamá - Cobertura de Vacunación Sarampión (SH.IMM.MEAS)",
    description=(
        "API REST (solo lectura) para consultar la cobertura de vacunación "
        "contra el sarampión en niños de 12–23 meses en Panamá. "
        "Fuente: World Bank (WDI, indicador SH.IMM.MEAS)."
    ),
    version="1.0.0",
    openapi_tags=[
        {"name": "vacunas", "description": "Consultas de cobertura vacunal (WDI)"},
    ],
)
# Ruta de verificación de salud de la API y Obtiene todos los datos para verificar que la conexión y la carga funcionan.

@app.get("/health", response_model=HealthCheck, tags=["health"])
def health(dp: DataProvider = Depends(get_data_provider)):
    _ = dp.get_all() # Se ejecuta para comprobar que el DataProvider funciona
    return HealthCheck(status="ok") # Devuelve un objeto HealthCheck con status 'ok' si no hay ningun problema

# Agrega el router de vacunas a la aplicación y todas las rutas definidas en vacunas_router se incluirán con el prefijo ""
app.include_router(vacunas_router, prefix="", tags=["vacunas"])


# Maneja las excepciones HTTP lanzadas en la API y devuelve una respuesta JSON con el código de estado y detalle del error.
@app.exception_handler(HTTPException)
async def http_exception_handler(request, exc: HTTPException):
    return JSONResponse(status_code=exc.status_code, content={"detail": exc.detail})
