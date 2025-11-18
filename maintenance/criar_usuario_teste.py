from app.database import SessionLocal, engine
from app.models import Usuario, Base
from passlib.context import CryptContext

# Criar tabelas se não existirem
Base.metadata.create_all(bind=engine)

# Contexto para hash
pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

def criar_usuario_teste():
    db = SessionLocal()
    
    try:
        # Verificar se já existe
        existe = db.query(Usuario).filter(Usuario.email == "teste@email.com").first()
        
        if existe:
            print("❌ Usuário já existe!")
            print(f"Email: {existe.email}")
            print(f"Nome: {existe.nome_completo}")
            return
        
        # Criar senha hash
        senha = "senha123"
        senha_bytes = senha.encode('utf-8')
        if len(senha_bytes) > 72:
            senha = senha_bytes[:72].decode('utf-8', errors='ignore')
        senha_hash = pwd_context.hash(senha)
        
        # Criar usuário
        novo_usuario = Usuario(
            email="teste@email.com",
            nome_completo="Usuario Teste",
            senha_hash=senha_hash,
            tipo_plano="gratuito",
            ativo=True
        )
        
        db.add(novo_usuario)
        db.commit()
        db.refresh(novo_usuario)
        
        print("✅ Usuário criado com sucesso!")
        print(f"ID: {novo_usuario.id}")
        print(f"Email: {novo_usuario.email}")
        print(f"Nome: {novo_usuario.nome_completo}")
        print(f"Plano: {novo_usuario.tipo_plano}")
        
    except Exception as e:
        print(f"❌ Erro ao criar usuário: {e}")
        db.rollback()
    finally:
        db.close()

if __name__ == "__main__":
    criar_usuario_teste()