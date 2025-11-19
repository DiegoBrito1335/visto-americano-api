from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from typing import List, Optional

from app.database import get_db
from app import schemas
from app.services.perguntas_service import PerguntasService

router = APIRouter(tags=["Perguntas"])


# ======================================================
#              DS-160
# ======================================================
@router.get("/ds160", response_model=List[schemas.PerguntaDS160Resposta])
def listar_ds160(
    gratuito: Optional[bool] = None,
    categoria: Optional[str] = None,
    db: Session = Depends(get_db)
):
    """
    Lista perguntas DS-160 (gratuitas / premium / por categoria)
    """
    return PerguntasService.listar_ds160(db, gratuito, categoria)


# ======================================================
#              ENTREVISTA CONSULAR
# ======================================================
@router.get("/entrevista", response_model=List[schemas.PerguntaEntrevistaResposta])
def listar_entrevista(
    gratuito: Optional[bool] = None,
    categoria: Optional[str] = None,
    db: Session = Depends(get_db)
):
    """
    Lista perguntas da entrevista consular (gratuitas / premium / por categoria)
    """
    return PerguntasService.listar_entrevista(db, gratuito, categoria)


# ======================================================
#              ESTATÍSTICAS
# ======================================================
@router.get("/stats")
def estatisticas_perguntas(db: Session = Depends(get_db)):
    """
    Estatísticas gerais das perguntas: total, gratuitas, premium.
    """
    return PerguntasService.estatisticas(db)
