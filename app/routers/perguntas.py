from fastapi import APIRouter, Depends
from typing import List
from sqlalchemy.orm import Session

from app.database import get_db
from app.schemas import PerguntaDS160Resposta, PerguntaEntrevistaResposta
from app.services.perguntas_service import listar_ds160, listar_entrevista, stats_perguntas

router = APIRouter()

@router.get("/ds160", response_model=List[PerguntaDS160Resposta])
def ds160(gratuito: bool = None, categoria: str = None, db: Session = Depends(get_db)):
    return listar_ds160(db, gratuito, categoria)

@router.get("/entrevista", response_model=List[PerguntaEntrevistaResposta])
def entrevista(gratuito: bool = None, categoria: str = None, db: Session = Depends(get_db)):
    return listar_entrevista(db, gratuito, categoria)

@router.get("/stats")
def stats(db: Session = Depends(get_db)):
    return stats_perguntas(db)
