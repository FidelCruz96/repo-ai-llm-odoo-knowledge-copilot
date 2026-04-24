from app.core.config import Settings
from app.services.health_service import HealthService


class StubHealthService(HealthService):
    def __init__(self, checks: dict[str, str]):
        settings = Settings(
            APP_NAME="odoo-knowledge-copilot",
            APP_ENV="test",
            APP_VERSION="0.1.0",
            DATABASE_URL="postgresql://odoo:odoo@localhost:5432/odoo_knowledge",
            API_KEY="test-key",
            OPENAI_API_KEY="test-openai-key",
        )
        super().__init__(settings=settings)
        self._checks = checks

    def _check_vector_store(self) -> str:
        return self._checks["vector_store"]

    def _check_llm_api(self) -> str:
        return self._checks["llm_api"]

    def _check_cache(self) -> str:
        return self._checks["cache"]


def test_run_checks_is_healthy_when_optional_dependencies_are_not_configured() -> None:
    service = StubHealthService(
        checks={"vector_store": "ok", "llm_api": "ok", "cache": "not_configured"}
    )

    response = service.run_checks()

    assert response.status == "healthy"
    assert response.checks["cache"] == "not_configured"


def test_run_checks_is_degraded_when_any_dependency_has_error() -> None:
    service = StubHealthService(
        checks={"vector_store": "ok", "llm_api": "error", "cache": "not_configured"}
    )

    response = service.run_checks()

    assert response.status == "degraded"
    assert response.checks["llm_api"] == "error"
