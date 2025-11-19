from sqlalchemy.orm import Session
from fastapi import HTTPException, status
from datetime import datetime, timedelta

from app import models
from app.core.security import hash_password, verify_password
from app.core.config import settings


class UsuariosService:

    # ===============================
    # REGISTRAR NOVO USUÁRIO
    # ===============================
    def registrar(self, db: Session, email: str, senha: str, nome: str):
        usuario_existente = (
            db.query(models.Usuario)
            .filter(models.Usuario.email == email)
            .first()
        )

        if usuario_existente:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="E-mail já registrado."
            )

        novo_usuario = models.Usuario(
            email=email,
            senha_hash=hash_password(senha),
            nome_completo=nome,
            tipo_plano="gratuito",
            ativo=True,
            data_cadastro=datetime.utcnow(),
        )

        db.add(novo_usuario)
        db.commit()
        db.refresh(novo_usuario)

        return novo_usuario

    # ===============================
    # AUTENTICAÇÃO
    # ===============================
    def autenticar(self, db: Session, email: str, senha: str):
        usuario = (
            db.query(models.Usuario)
            .filter(models.Usuario.email == email)
            .first()
        )

        if not usuario:
            return None
        
        if not verify_password(senha, usuario.senha_hash):
            return None

        return usuario

    # ===============================
    # LISTAR TODOS
    # ===============================
    def listar_todos(self, db: Session):
        return db.query(models.Usuario).order_by(models.Usuario.id.asc()).all()

    # ===============================
    # TRANSFORMAR EM PREMIUM
    # ===============================
    def tornar_premium(self, db: Session, usuario_id: int, dias: int = None):
        usuario = (
            db.query(models.Usuario)
            .filter(models.Usuario.id == usuario_id)
            .first()
        )

        if not usuario:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Usuário não encontrado"
            )

        usuario.tipo_plano = "premium"

        # Tratamento correto para planos temporários ou vitalício
        if dias:
            usuario.data_expiracao_premium = datetime.utcnow() + timedelta(days=dias)
        else:
            usuario.data_expiracao_premium = None  # Vitalício

        db.commit()
        db.refresh(usuario)

        return usuario

    # ===============================
    # BUSCAR POR EMAIL (ÚTIL PARA WEBHOOK / SERVIÇOS)
    # ===============================
    def buscar_por_email(self, db: Session, email: str):
        return (
            db.query(models.Usuario)
            .filter(models.Usuario.email == email)
            .first()
        )


usuarios_service = UsuariosService()
