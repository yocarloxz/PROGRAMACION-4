from pydantic import BaseModel

# Modelo Pydantic para el endpoint de health check
class HealthCheck(BaseModel):
    status: str
