# app/schemas/auth_schema.py

from pydantic import BaseModel, EmailStr


# ============================================
# LOGIN
# ============================================

class LoginSchema(BaseModel):
    email: EmailStr
    senha: str


# ============================================
# TOKEN (RETORNO)
# ============================================

class TokenSchema(BaseModel):
    access_token: str
    refresh_token: str
    token_type: str = "bearer"


# ============================================
# USUÁRIO (RETORNO APÓS LOGIN)
# ============================================

class UsuarioOut(BaseModel):
    id: int
    email: EmailStr

    model_config = {
        "from_attributes": True
    }
