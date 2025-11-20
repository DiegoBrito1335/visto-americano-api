from sqlalchemy.orm import Session
from datetime import datetime
from typing import Dict

from app.models import Tentativa, Resposta, PerguntaDS160, PerguntaEntrevista
from app.schemas.tentativas_schema import TentativaCreate, RespostaCreate


class TentativasService:

    @staticmethod
    def registrar_tentativa(db: Session, tentativa_data: TentativaCreate):
        tentativa = Tentativa(
            tipo=tentativa_data.tipo,
            data_tentativa=datetime.now(),
            tempo_gasto=tentativa_data.tempo_gasto,
        )

        db.add(tentativa)
        db.commit()
        db.refresh(tentativa)

        pontuacao_final = 0
        soma_pesos = 0
        categorias = {}

        # Avaliar cada resposta
        for r in tentativa_data.respostas:
            resultado = TentativasService._avaliar_resposta(db, r)

            resposta_model = Resposta(
                tentativa_id=tentativa.id,
                pergunta_id=r.pergunta_id,
                tipo_pergunta=r.tipo_pergunta,
                resposta_usuario=r.resposta_usuario,
                pontos_obtidos=resultado["pontos"],
                feedback=resultado["feedback"]
            )

            db.add(resposta_model)

            pontuacao_final += resultado["pontos"]
            soma_pesos += resultado["peso"]

            # Organiza pontuação por categoria
            cat = resultado["categoria"]
            if cat not in categorias:
                categorias[cat] = {"pontos": 0, "peso": 0}

            categorias[cat]["pontos"] += resultado["pontos"]
            categorias[cat]["peso"] += resultado["peso"]

        db.commit()

        # Garantir que a pontuação final seja válida
        nota = round((pontuacao_final / soma_pesos) * 100, 2) if soma_pesos > 0 else 0

        tentativa.pontuacao_final = nota if nota is not None else 0
        tentativa.pontuacao_categorias = TentativasService._normalizar_categorias(categorias)
        tentativa.probabilidade = TentativasService._calcular_probabilidade(nota) or "Indefinido"  # Garantir que probabilidade tenha um valor válido
        tentativa.completo = True

        db.commit()
        db.refresh(tentativa)

        return tentativa

    @staticmethod
    def _avaliar_resposta(db: Session, resposta: RespostaCreate) -> Dict:
        if resposta.tipo_pergunta == "ds160":
            pergunta = db.query(PerguntaDS160).filter(PerguntaDS160.id == resposta.pergunta_id).first()
        else:
            pergunta = db.query(PerguntaEntrevista).filter(PerguntaEntrevista.id == resposta.pergunta_id).first()

        if not pergunta:
            return {
                "categoria": "desconhecida",
                "peso": 1,
                "pontos": 0,
                "feedback": "Pergunta não encontrada."
            }

        texto = resposta.resposta_usuario.lower()

        # Calculando pontuação
        peso = getattr(pergunta, "peso_avaliacao", 5)
        pontos = peso * 0.5

        positivos = sum(1 for p in (pergunta.palavras_positivas or []) if p.lower() in texto)
        negativos = sum(1 for n in (pergunta.palavras_negativas or []) if n.lower() in texto)

        pontos += positivos * 1.2
        pontos -= negativos * 1.3
        pontos = max(0, min(pontos, peso))

        # Feedback
        if negativos > 0:
            feedback = "Cuidado: sua resposta contém termos que prejudicam a avaliação."
        elif positivos > 0:
            feedback = "Boa resposta! Você incluiu elementos positivos."
        else:
            feedback = "Resposta neutra. Pode ser melhorada com mais detalhes positivos."

        return {
            "categoria": pergunta.categoria,
            "peso": peso,
            "pontos": round(pontos, 2),
            "feedback": feedback
        }

    @staticmethod
    def _normalizar_categorias(dados: Dict) -> Dict:
        return {
            categoria: round((v["pontos"] / v["peso"]) * 100, 2) if v["peso"] > 0 else 0
            for categoria, v in dados.items()
        }

    @staticmethod
    def _calcular_probabilidade(nota: float) -> str:
        if nota is None:
            return "Indefinido"

        if nota >= 90: return "Muito Alta"
        if nota >= 75: return "Alta"
        if nota >= 60: return "Média"
        if nota >= 40: return "Baixa"
        return "Muito Baixa"

    @staticmethod
    def estatisticas_comparacao(db: Session):
        tentativas = db.query(Tentativa).all()

        if not tentativas:
            return {
                "total_tentativas": 0,
                "media_nota": 0,
                "nota_maxima": 0,
                "nota_minima": 0,
                "distribucao_probabilidade": {}
            }

        # Ajusta None → 0
        notas = [(t.pontuacao_final or 0) for t in tentativas]

        dist = {}
        for t in tentativas:
            prob = t.probabilidade or "Indefinido"  # Garantir que a probabilidade seja uma string válida
            dist[prob] = dist.get(prob, 0) + 1

        media_nota = round(sum(notas) / len(notas), 2)

        return {
            "total_tentativas": len(tentativas),
            "media_nota": media_nota,
            "nota_maxima": max(notas),
            "nota_minima": min(notas),
            "distribucao_probabilidade": dist
        }

    @staticmethod
    def listar_tentativas(db: Session):
        return db.query(Tentativa).order_by(Tentativa.data_tentativa.desc()).all()

    @staticmethod
    def buscar_por_id(db: Session, tentativa_id: int):
        return db.query(Tentativa).filter(Tentativa.id == tentativa_id).first()

    @staticmethod
    def registrar_tentativa_com_usuario(db: Session, tentativa_data: TentativaCreate, usuario_id: int):
        tentativa = Tentativa(
            usuario_id=usuario_id,
            tipo=tentativa_data.tipo,
            data_tentativa=datetime.now(),
            tempo_gasto=tentativa_data.tempo_gasto,
        )

        db.add(tentativa)
        db.commit()
        db.refresh(tentativa)

        return TentativasService.registrar_tentativa(db, tentativa_data)

    @staticmethod
    def listar_historico(db: Session, usuario_id: int, limite: int = 50, tipo: str | None = None):
        query = db.query(Tentativa).filter(Tentativa.usuario_id == usuario_id)

        if tipo:
            query = query.filter(Tentativa.tipo == tipo)

        return query.order_by(Tentativa.data_tentativa.desc()).limit(limite).all()

    @staticmethod
    def detalhe_tentativa(db: Session, tentativa_id: int, usuario_id: int):
        return (
            db.query(Tentativa)
            .filter(Tentativa.id == tentativa_id, Tentativa.usuario_id == usuario_id)
            .first()
        )

    @staticmethod
    def deletar_tentativa(db: Session, tentativa_id: int, usuario_id: int):
        tentativa = db.query(Tentativa).filter(
            Tentativa.id == tentativa_id,
            Tentativa.usuario_id == usuario_id
        ).first()

        if not tentativa:
            return False

        db.delete(tentativa)
        db.commit()

        return True
