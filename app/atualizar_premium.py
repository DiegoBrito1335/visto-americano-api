"""
Script para atualizar usuário para Premium
Execute: python atualizar_premium.py
"""

from app.database import SessionLocal
from app.models import Usuario

def listar_usuarios(db):
    """Lista usuários disponíveis"""
    usuarios = db.query(Usuario).all()
    
    if not usuarios:
        print("❌ Nenhum usuário encontrado!")
        return None
    
    print("\n" + "=" * 60)
    print("👥 USUÁRIOS DISPONÍVEIS")
    print("=" * 60)
    
    for i, user in enumerate(usuarios, 1):
        status = "⭐ PREMIUM" if user.tipo_plano == "premium" else "🆓 GRATUITO"
        print(f"{i}. {user.email} - {status}")
    
    print("=" * 60)
    return usuarios


def atualizar_para_premium():
    """Atualiza usuário para plano Premium"""
    db = SessionLocal()
    
    try:
        usuarios = listar_usuarios(db)
        
        if not usuarios:
            return
        
        # Solicitar escolha
        escolha = input("\n Digite o número do usuário para tornar PREMIUM (ou 0 para sair): ")
        
        if escolha == "0":
            print("❌ Operação cancelada.")
            return
        
        try:
            indice = int(escolha) - 1
            if indice < 0 or indice >= len(usuarios):
                print("❌ Número inválido!")
                return
            
            usuario = usuarios[indice]
            
            # Confirmar
            print(f"\n⚠️  Você vai atualizar:")
            print(f"   📧 Email: {usuario.email}")
            print(f"   👤 Nome: {usuario.nome_completo}")
            print(f"   📊 Plano atual: {usuario.tipo_plano.upper()}")
            
            confirmar = input("\n✅ Confirmar atualização para PREMIUM? (s/n): ")
            
            if confirmar.lower() != 's':
                print("❌ Operação cancelada.")
                return
            
            # Atualizar
            usuario.tipo_plano = "premium"
            usuario.data_expiracao_premium = None  # Vitalício
            
            db.commit()
            
            print("\n" + "=" * 60)
            print("🎉 USUÁRIO ATUALIZADO COM SUCESSO!")
            print("=" * 60)
            print(f"   📧 Email: {usuario.email}")
            print(f"   💳 Plano: PREMIUM ⭐")
            print(f"   ⏰ Validade: VITALÍCIO ♾️")
            print("=" * 60 + "\n")
            
        except ValueError:
            print("❌ Digite apenas números!")
            return
        
    except Exception as e:
        print(f"❌ Erro: {e}")
        db.rollback()
    finally:
        db.close()


if __name__ == "__main__":
    print("\n🚀 ATUALIZAR USUÁRIO PARA PREMIUM")
    atualizar_para_premium()
