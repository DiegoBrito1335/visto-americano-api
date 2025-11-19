from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

from app.core.security import get_current_user
from app.database import get_db
from app.services.pdf_service import PDFService
from app import models

router = APIRouter(
    prefix="/pdf",
    tags=["PDF"]
)

@router.get("/{tentativa_id}")
def gerar_pdf(
    tentativa_id: int,
    db: Session = Depends(get_db),
    usuario: models.Usuario = Depends(get_current_user)
):
    """
    Gera um PDF contendo as informações de uma tentativa específica.
    Apenas o dono da tentativa ou um admin podem acessar.
    """

    pdf = PDFService.gerar_pdf_tentativa(db, tentativa_id, usuario)

    if pdf is None:
        raise HTTPException(status_code=404, detail="Tentativa não encontrada")

    return pdf


