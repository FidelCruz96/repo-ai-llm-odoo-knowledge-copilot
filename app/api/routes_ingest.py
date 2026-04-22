from fastapi import APIRouter, Depends, File, Form, HTTPException, UploadFile, status

from app.core.config import get_settings
from app.core.rate_limit import enforce_rate_limit
from app.core.security import verify_api_key
from app.models.schemas import IngestResponse
from app.services.ingest_service import IngestService, get_ingest_service
from app.utils.file_validation import validate_ingest_file

router = APIRouter(prefix="/v1", tags=["ingest"])


@router.post(
    "/ingest",
    response_model=IngestResponse,
    dependencies=[Depends(verify_api_key), Depends(enforce_rate_limit)],
)
async def ingest_documents(
    files: list[UploadFile] = File(...),
    module: str | None = Form(default=None),
    service: IngestService = Depends(get_ingest_service),
) -> IngestResponse:
    settings = get_settings()
    payload: list[tuple[str, bytes]] = []
    for file in files:
        file_name = file.filename or "unknown"
        content = await file.read()
        try:
            validate_ingest_file(file_name, content, settings.max_upload_size_mb)
        except ValueError as exc:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail=str(exc),
            ) from exc
        payload.append((file_name, content))

    return service.ingest_files(files=payload, module=module)
