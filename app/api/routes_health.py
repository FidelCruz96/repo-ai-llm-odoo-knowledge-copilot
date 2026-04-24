from fastapi import APIRouter, Depends

from app.models.schemas import HealthResponse
from app.services.health_service import HealthService, get_health_service

router = APIRouter(prefix="/v1", tags=["health"])


@router.get("/health", response_model=HealthResponse)
def health(service: HealthService = Depends(get_health_service)) -> HealthResponse:
    return service.run_checks()
