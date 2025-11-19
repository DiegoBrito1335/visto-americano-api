from sqlalchemy.orm import Session
from app import models


class PerguntasService:
    """
    Serviço responsável por manipular perguntas DS-160 e da entrevista consular.
    """

    # -----------------------------
    #      LISTAR PERGUNTAS DS-160
    # -----------------------------
    @staticmethod
    def listar_ds160(db: Session, gratuito: bool = None, categoria: str = None):
        query = db.query(models.PerguntaDS160)

        if gratuito is True:
            query = query.filter(models.PerguntaDS160.gratuita == True)

        if categoria:
            query = query.filter(models.PerguntaDS160.categoria == categoria)

        return query.order_by(models.PerguntaDS160.ordem).all()

    # -----------------------------
    #      LISTAR PERGUNTAS ENTREVISTA
    # -----------------------------
    @staticmethod
    def listar_entrevista(db: Session, gratuito: bool = None, categoria: str = None):
        query = db.query(models.PerguntaEntrevista)

        if gratuito is True:
            query = query.filter(models.PerguntaEntrevista.gratuita == True)

        if categoria:
            query = query.filter(models.PerguntaEntrevista.categoria == categoria)

        return query.order_by(models.PerguntaEntrevista.ordem).all()

    # -----------------------------
    #      ESTATÍSTICAS
    # -----------------------------
    @staticmethod
    def estatisticas(db: Session):
        total_ds160 = db.query(models.PerguntaDS160).count()
        gratuitas_ds160 = db.query(models.PerguntaDS160).filter(
            models.PerguntaDS160.gratuita == True
        ).count()

        total_entrevista = db.query(models.PerguntaEntrevista).count()
        gratuitas_entrevista = db.query(models.PerguntaEntrevista).filter(
            models.PerguntaEntrevista.gratuita == True
        ).count()

        return {
            "ds160": {
                "total": total_ds160,
                "gratuitas": gratuitas_ds160,
                "premium": total_ds160 - gratuitas_ds160,
            },
            "entrevista": {
                "total": total_entrevista,
                "gratuitas": gratuitas_entrevista,
                "premium": total_entrevista - gratuitas_entrevista,
            },
            "total_geral": total_ds160 + total_entrevista,
        }


# Instância opcional se quiser usar como objeto
perguntas_service = PerguntasService()
