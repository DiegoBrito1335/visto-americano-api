"""
Script para verificar usuários no banco de dados
Execute: python verificar_usuarios.py
"""

from app.database import SessionLocal
from app.models import Usuario

def verificar_usuarios():
    """Lista todos os usuários e seus planos"""
    db = SessionLocal()
    
    try:
        usuarios = db.query(Usuario).all()
        
        if not usuarios:
            print("❌ Nenhum usuário encontrado no banco de dados!")
            return
        
        print("\n" + "=" * 80)
        print("👥 USUÁRIOS NO BANCO DE DADOS")
        print("=" * 80)
        
        for i, user in enumerate(usuarios, 1):
            print(f"\n🔹 USUÁRIO #{i}")
            print(f"   ID: {user.id}")
            print(f"   📧 Email: {user.email}")
            print(f"   👤 Nome: {user.nome_completo}")
            print(f"   💳 Plano: {user.tipo_plano.upper()}")
            print(f"   📅 Cadastro: {user.data_cadastro.strftime('%d/%m/%Y %H:%M')}")
            
            if user.data_expiracao_premium:
                print(f"   ⏰ Premium até: {user.data_expiracao_premium.strftime('%d/%m/%Y %H:%M')}")
            elif user.tipo_plano == "premium":
                print(f"   ⏰ Premium: VITALÍCIO ✨")
            
            print(f"   ✅ Ativo: {'Sim' if user.ativo else 'Não'}")
            print("-" * 80)
        
        print(f"\n📊 TOTAL: {len(usuarios)} usuário(s)")
        
        # Estatísticas
        gratuitos = sum(1 for u in usuarios if u.tipo_plano == "gratuito")
        premium = sum(1 for u in usuarios if u.tipo_plano == "premium")
        
        print("\n📈 ESTATÍSTICAS:")
        print(f"   🆓 Gratuitos: {gratuitos}")
        print(f"   ⭐ Premium: {premium}")
        print("=" * 80 + "\n")
        
    except Exception as e:
        print(f"❌ Erro ao consultar banco de dados: {e}")
    finally:
        db.close()


if __name__ == "__main__":
    verificar_usuarios()
