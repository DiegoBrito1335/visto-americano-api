from sqlalchemy.orm import Session
from sqlalchemy import func
from app import models, schemas


class TentativasService:

    # =============================================================
    # AVALIA AS RESPOSTAS ENVIADAS PELO USUÁRIO
    # =============================================================
    @staticmethod
    def avaliar_respostas(db: Session, dados: schemas.TentativaCriar, usuario: models.Usuario):

        acertos = 0
        total = len(dados.respostas)

        resultados = []

        for resposta in dados.respostas:
            # Identificar se a pergunta é DS160 ou Entrevista
            if dados.tipo == "ds160":
                pergunta = db.query(models.PerguntaDS160).filter_by(id=resposta.pergunta_id).first()
            else:
                pergunta = db.query(models.PerguntaEntrevista).filter_by(id=resposta.pergunta_id).first()

            if not pergunta:
                continue

            correta = pergunta.resposta_correta.strip().lower()
            enviada = resposta.resposta.strip().lower()

            acertou = correta == enviada
            if acertou:
                acertos += 1

            resultados.append({
                "pergunta_id": pergunta.id,
                "pergunta": pergunta.pergunta,
                "resposta_correta": pergunta.resposta_correta,
                "resposta_usuario": resposta.resposta,
                "acertou": acertou
            })

        # Criar tentativa no banco
        tentativa = models.Tentativa(
            usuario_id=usuario.id,
            tipo=dados.tipo,
            acertos=acertos,
            total=total
        )
        db.add(tentativa)
        db.commit()
        db.refresh(tentativa)

        return schemas.TentativaResposta(
            id=tentativa.id,
            acertos=acertos,
            total=total,
            resultados=resultados
        )

    # =============================================================
    # HISTÓRICO DO USUÁRIO
    # =============================================================
    @staticmethod
    def listar_historico(db: Session, usuario_id: int, limite: int, tipo: str | None):

        query = db.query(models.Tentativa).filter(models.Tentativa.usuario_id == usuario_id)

        if tipo:
            query = query.filter(models.Tentativa.tipo == tipo)

        tentativas = query.order_by(models.Tentativa.id.desc()).limit(limite).all()

        return [
            schemas.TentativaHistorico(
                id=t.id,
                tipo=t.tipo,
                acertos=t.acertos,
                total=t.total,
                data=t.data_criacao
            )
            for t in tentativas
        ]

    # =============================================================
    # DETALHE DE UMA TENTATIVA
    # =============================================================
    @staticmethod
    def detalhe_tentativa(db: Session, tentativa_id: int, usuario_id: int):

        tentativa = db.query(models.Tentativa).filter(
            models.Tentativa.id == tentativa_id,
            models.Tentativa.usuario_id == usuario_id
        ).first()

        if not tentativa:
            return None

        return schemas.TentativaDetalhe(
            id=tentativa.id,
            tipo=tentativa.tipo,
            acertos=tentativa.acertos,
            total=tentativa.total,
            data=tentativa.data_criacao
        )

    # =============================================================
    # DELETAR
    # =============================================================
    @staticmethod
    def deletar_tentativa(db: Session, tentativa_id: int, usuario_id: int):

        tentativa = db.query(models.Tentativa).filter(
            models.Tentativa.id == tentativa_id,
            models.Tentativa.usuario_id == usuario_id
        ).first()

        if not tentativa:
            return False

        db.delete(tentativa)
        db.commit()
        return True

    # =============================================================
    # ESTATÍSTICAS / COMPARAÇÃO
    # =============================================================
    @staticmethod
    def comparar_tentativas(db: Session, usuario_id: int):

        tentativas = db.query(models.Tentativa).filter(
            models.Tentativa.usuario_id == usuario_id
        ).all()

        if not tentativas:
            return None

        total = len(tentativas)
        media_acertos = sum(t.acertos for t in tentativas) / total
        media_total = sum(t.total for t in tentativas) / total

        melhor = max(tentativas, key=lambda t: t.acertos)
        pior = min(tentativas, key=lambda t: t.acertos)

        return schemas.TentativasComparacao(
            total_tentativas=total,
            media_acertos=round(media_acertos, 2),
            media_total_perguntas=round(media_total, 2),
            melhor_tentativa={
                "id": melhor.id,
                "acertos": melhor.acertos,
                "total": melhor.total
            },
            pior_tentativa={
                "id": pior.id,
                "acertos": pior.acertos,
                "total": pior.total
            }
        )
