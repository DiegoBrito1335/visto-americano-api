from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

from app.database import get_db
from app.core.security import get_current_user
from app.services.tentativas_service import TentativasService
from app import schemas, models

router = APIRouter(
    prefix="/tentativas",
    tags=["Tentativas"]
)

# =============================================================
# COMPARAÇÃO (rota fixa — antes das rotas com path dinâmico)
# =============================================================
@router.get("/estatisticas/comparacao", response_model=schemas.TentativaComparacao)
def comparar_tentativas(
    db: Session = Depends(get_db),
    usuario: models.Usuario = Depends(get_current_user)
):
    stats = TentativasService.comparar_tentativas(db, usuario.id)

    if not stats:
        raise HTTPException(status_code=404, detail="Nenhuma tentativa encontrada")

    return stats


# =============================================================
# AVALIAR TENTATIVA
# =============================================================
@router.post("/avaliar", response_model=schemas.TentativaResposta)
def avaliar_tentativa(
    dados: schemas.TentativaCriar,
    db: Session = Depends(get_db),
    usuario: models.Usuario = Depends(get_current_user)
):
    return TentativasService.avaliar_respostas(db, dados, usuario)


# =============================================================
# LISTAR HISTÓRICO
# =============================================================
@router.get("/historico", response_model=list[schemas.TentativaHistoricoItem])
def listar_historico(
    limite: int = 50,
    tipo: str | None = None,
    db: Session = Depends(get_db),
    usuario: models.Usuario = Depends(get_current_user)
):
    return TentativasService.listar_historico(db, usuario.id, limite, tipo)


# =============================================================
# DETALHE DA TENTATIVA
# =============================================================
@router.get("/{tentativa_id}", response_model=schemas.TentativaDetalhe)
def detalhe_tentativa(
    tentativa_id: int,
    db: Session = Depends(get_db),
    usuario: models.Usuario = Depends(get_current_user)
):
    tentativa = TentativasService.detalhe_tentativa(db, tentativa_id, usuario.id)

    if not tentativa:
        raise HTTPException(status_code=404, detail="Tentativa não encontrada")

    return tentativa


# =============================================================
# DELETAR
# =============================================================
@router.delete("/{tentativa_id}")
def deletar_tentativa(
    tentativa_id: int,
    db: Session = Depends(get_db),
    usuario: models.Usuario = Depends(get_current_user)
):
    ok = TentativasService.deletar_tentativa(db, tentativa_id, usuario.id)

    if not ok:
        raise HTTPException(status_code=404, detail="Tentativa não encontrada")

    return {"mensagem": "Tentativa deletada com sucesso"}

