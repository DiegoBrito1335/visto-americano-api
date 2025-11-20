from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from typing import List

from app.database import get_db
from app.core.security import get_current_user
from app.services.tentativas_service import TentativasService
from app.schemas.tentativas_schema import (
    TentativaCreate,
    TentativaResposta,
    TentativaComparacao,
    TentativaHistoricoItem,
    TentativaDetalhe,
)
from app import models

router = APIRouter(
    prefix="/tentativas",
    tags=["Tentativas"]
)


# ============================================================
#          REGISTRAR TENTATIVA
# ============================================================

@router.post("/", response_model=TentativaResposta)
def registrar_tentativa(
    dados: TentativaCreate,
    db: Session = Depends(get_db),
    usuario: models.Usuario = Depends(get_current_user)
):
    tentativa = TentativasService.registrar_tentativa_com_usuario(db, dados, usuario.id)
    return tentativa


# ============================================================
#          HISTÓRICO DO USUÁRIO
# ============================================================

@router.get("/historico", response_model=List[TentativaHistoricoItem])
def listar_historico(
    limite: int = 50,
    tipo: str | None = None,
    db: Session = Depends(get_db),
    usuario: models.Usuario = Depends(get_current_user)
):
    return TentativasService.listar_historico(db, usuario.id, limite, tipo)


# ============================================================
#          DETALHE DA TENTATIVA
# ============================================================

@router.get("/{tentativa_id}", response_model=TentativaDetalhe)
def detalhe_tentativa(
    tentativa_id: int,
    db: Session = Depends(get_db),
    usuario: models.Usuario = Depends(get_current_user)
):
    tentativa = TentativasService.detalhe_tentativa(db, tentativa_id, usuario.id)

    if not tentativa:
        raise HTTPException(status_code=404, detail="Tentativa não encontrada")

    return tentativa


# ============================================================
#          DELETAR TENTATIVA
# ============================================================

@router.delete("/{tentativa_id}")
def deletar_tentativa(
    tentativa_id: int,
    db: Session = Depends(get_db),
    usuario: models.Usuario = Depends(get_current_user)
):
    ok = TentativasService.deletar_tentativa(db, tentativa_id, usuario.id)

    if not ok:
        raise HTTPException(status_code=404, detail="Tentativa não encontrada")

    return {"mensagem": "Tentativa deletada com sucesso", "success": True}


# ============================================================
#          ESTATÍSTICAS / COMPARAÇÃO
# ============================================================

@router.get("/estatisticas/comparacao", response_model=TentativaComparacao)
def comparar_tentativas(
    db: Session = Depends(get_db),
    usuario: models.Usuario = Depends(get_current_user)
):
    return TentativasService.estatisticas_comparacao(db)
