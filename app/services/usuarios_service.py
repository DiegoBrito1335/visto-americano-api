from sqlalchemy.orm import Session
from fastapi import HTTPException, status
from datetime import datetime, timedelta

from app import models
from app.core.security import hash_password, verify_password


class UsuariosService:

    # ======================================================
    # REGISTRO DE NOVO USUÁRIO
    # ======================================================
    def registrar(self, db: Session, email: str, senha: str):
        """
        Cria um novo usuário com plano gratuito e senha hasheada.
        """

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
            tipo_plano="gratuito",
            ativo=True,
            data_cadastro=datetime.utcnow(),
            data_expiracao_premium=None,
        )

        db.add(novo_usuario)
        db.commit()
        db.refresh(novo_usuario)

        return novo_usuario

    # ======================================================
    # AUTENTICAÇÃO
    # ======================================================
    def autenticar(self, db: Session, email: str, senha: str):
        """
        Verifica email + senha, retornando o usuário caso sucesso.
        Se falhar, retorna None.
        """

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

    # ======================================================
    # LISTAR TODOS OS USUÁRIOS
    # ======================================================
    def listar_todos(self, db: Session):
        """
        Lista todos os usuários (modo admin/debug).
        """
        return (
            db.query(models.Usuario)
            .order_by(models.Usuario.id.asc())
            .all()
        )

    # ======================================================
    # TORNAR PREMIUM
    # ======================================================
    def tornar_premium(self, db: Session, usuario_id: int, dias: int | None = None):
        """
        Torna o usuário premium.
        Se dias for informado -> premium temporário.
        Caso contrário -> premium vitalício.
        """

        usuario = (
            db.query(models.Usuario)
            .filter(models.Usuario.id == usuario_id)
            .first()
        )

        if not usuario:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Usuário não encontrado."
            )

        usuario.tipo_plano = "premium"

        if dias:
            # Premium temporário
            usuario.data_expiracao_premium = datetime.utcnow() + timedelta(days=dias)
        else:
            # Premium vitalício
            usuario.data_expiracao_premium = None

        db.commit()
        db.refresh(usuario)

        return usuario

    # ======================================================
    # BUSCAR POR EMAIL
    # ======================================================
    def buscar_por_email(self, db: Session, email: str):
        """
        Retorna um usuário pelo email ou None.
        """
        return (
            db.query(models.Usuario)
            .filter(models.Usuario.email == email)
            .first()
        )


# Instância única (singleton)
usuarios_service = UsuariosService()
