from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from app.database import get_db
from app.models import PerguntaDS160, PerguntaEntrevista
from app.schemas.tentativas_schema import RespostaResposta

router = APIRouter(
    prefix="/perguntas",
    tags=["Perguntas"]
)

# ============================================================
#      CARREGAR PERGUNTAS POR CATEGORIA (DS-160, ENTREVISTA)
# ============================================================

@router.get("", response_model=list[RespostaResposta])
def get_perguntas(categoria: str, db: Session = Depends(get_db)):
    """
    Retorna uma lista de perguntas filtradas por categoria (ds160 ou entrevista).
    """
    if categoria == "ds160":
        perguntas = db.query(PerguntaDS160).filter(PerguntaDS160.categoria == categoria).all()
    elif categoria == "entrevista":
        perguntas = db.query(PerguntaEntrevista).filter(PerguntaEntrevista.categoria == categoria).all()
    else:
        raise HTTPException(status_code=400, detail="Categoria inválida.")
    
    # Convertendo as perguntas para o formato que o frontend precisa
    return [RespostaResposta(
        id=pergunta.id,
        pergunta_id=pergunta.id,
        tipo_pergunta=categoria,
        resposta_usuario="",
        pontos_obtidos=0,
        feedback=None
    ) for pergunta in perguntas]

