from app.api.routes_health import health
from app.main import app
from app.models.schemas import HealthResponse


class FakeHealthyService:
    def run_checks(self) -> HealthResponse:
        return HealthResponse(
            status="healthy",
            version="0.1.0",
            checks={"vector_store": "ok", "llm_api": "ok", "cache": "ok"},
        )


class FakeDegradedService:
    def run_checks(self) -> HealthResponse:
        return HealthResponse(
            status="degraded",
            version="0.1.0",
            checks={"vector_store": "ok", "llm_api": "error", "cache": "ok"},
        )


def test_health_contract_healthy() -> None:
    response = health(FakeHealthyService())

    assert response.status == "healthy"
    assert response.version == "0.1.0"
    assert set(response.checks.keys()) == {"vector_store", "llm_api", "cache"}


def test_health_contract_degraded() -> None:
    response = health(FakeDegradedService())

    assert response.status == "degraded"
    assert response.checks["llm_api"] == "error"


def test_health_route_is_registered() -> None:
    paths = {route.path for route in app.routes}
    assert "/v1/health" in paths
