from fastapi import APIRouter, Depends

from app.core.rate_limit import enforce_rate_limit
from app.core.security import verify_api_key
from app.models.schemas import QueryRequest, QueryResponse
from app.services.rag_service import RagService, get_rag_service

router = APIRouter(prefix="/v1", tags=["query"])


@router.post(
    "/query",
    response_model=QueryResponse,
    dependencies=[Depends(verify_api_key), Depends(enforce_rate_limit)],
)
def query(
    request: QueryRequest,
    service: RagService = Depends(get_rag_service),
) -> QueryResponse:
    return service.answer_query(request)
