from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from typing import List, Optional

from app.database import get_db
from app.schemas import TentativaCriar
from app.core.security import get_current_user
from app.services.tentativas_service import avaliar_respostas, listar_historico, detalhe_tentativa, deletar_tentativa, comparar_tentativas
from app.schemas import TentativaResposta

router = APIRouter()

@router.post("/avaliar")
def avaliar(dados: TentativaCriar, db: Session = Depends(get_db), current_user = Depends(get_current_user)):
    return avaliar_respostas(db, current_user, dados)

@router.get("/", response_model=List[TentativaResposta])
def historico(db: Session = Depends(get_db), current_user = Depends(get_current_user), limite: int = 50, tipo: Optional[str] = None):
    return listar_historico(db, current_user, limite, tipo)

@router.get("/{tentativa_id}")
def detalhe(tentativa_id: int, db: Session = Depends(get_db), current_user = Depends(get_current_user)):
    return detalhe_tentativa(db, current_user, tentativa_id)

@router.delete("/{tentativa_id}")
def deletar(tentativa_id: int, db: Session = Depends(get_db), current_user = Depends(get_current_user)):
    return deletar_tentativa(db, current_user, tentativa_id)

@router.get("/comparacao")
def comparar(db: Session = Depends(get_db), current_user = Depends(get_current_user)):
    return comparar_tentativas(db, current_user)

