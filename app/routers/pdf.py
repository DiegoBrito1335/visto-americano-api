from fastapi import APIRouter, Depends, HTTPException
from fastapi.responses import StreamingResponse
from sqlalchemy.orm import Session

from app.database import get_db
from app.core.security import get_current_user
from app.services.pdf_service import gerar_pdf_stream

router = APIRouter()

@router.get("/{tentativa_id}/pdf")
def pdf(tentativa_id: int, db: Session = Depends(get_db), current_user = Depends(get_current_user)):
    stream = gerar_pdf_stream(db, current_user, tentativa_id)
    if not stream:
        raise HTTPException(status_code=404, detail="Tentativa não encontrada")
    return StreamingResponse(stream, media_type="application/pdf")
