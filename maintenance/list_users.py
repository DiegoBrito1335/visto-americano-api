"""
Script para listar todos os usuários do sistema
Uso: python maintenance/list_users.py
"""

import sys
from pathlib import Path

# Adicionar raiz ao path
sys.path.insert(0, str(Path(__file__).parent.parent))

from app.database import SessionLocal
from app.models import Usuario


def list_users():
    """Lista todos os usuários e suas estatísticas"""
    db = SessionLocal()
    
    try:
        usuarios = db.query(Usuario).all()
        
        if not usuarios:
            print("\n❌ Nenhum usuário encontrado no banco de dados!")
            return
        
        print("\n" + "=" * 80)
        print("👥 USUÁRIOS NO BANCO DE DADOS")
        print("=" * 80)
        
        gratuitos = 0
        premium = 0
        
        for i, user in enumerate(usuarios, 1):
            if user.tipo_plano == "gratuito":
                gratuitos += 1
                status = "🆓 GRATUITO"
            else:
                premium += 1
                status = "⭐ PREMIUM"
            
            print(f"\n🔹 USUÁRIO #{i}")
            print(f"   ID: {user.id}")
            print(f"   📧 Email: {user.email}")
            print(f"   👤 Nome: {user.nome_completo}")
            print(f"   💳 Plano: {status}")
            print(f"   📅 Cadastro: {user.data_cadastro.strftime('%d/%m/%Y %H:%M')}")
            
            if user.data_expiracao_premium:
                print(f"   ⏰ Premium até: {user.data_expiracao_premium.strftime('%d/%m/%Y %H:%M')}")
            elif user.tipo_plano == "premium":
                print(f"   ⏰ Premium: VITALÍCIO ♾️")
            
            ativo = "✅ Sim" if user.ativo else "❌ Não"
            print(f"   Status: {ativo}")
            print("-" * 80)
        
        print(f"\n📊 TOTAL: {len(usuarios)} usuário(s)")
        print(f"\n📈 ESTATÍSTICAS:")
        print(f"   🆓 Gratuitos: {gratuitos}")
        print(f"   ⭐ Premium: {premium}")
        print("=" * 80 + "\n")
        
    except Exception as e:
        print(f"\n❌ Erro ao consultar banco de dados: {e}")
        import traceback
        traceback.print_exc()
    finally:
        db.close()


if __name__ == "__main__":
    list_users()