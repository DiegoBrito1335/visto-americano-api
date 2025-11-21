"""
Script para ativar plano Premium em usuário
Uso: python maintenance/activate_premium.py
"""

import sys
from pathlib import Path

# Adicionar raiz ao path
sys.path.insert(0, str(Path(__file__).parent.parent))

from app.database import SessionLocal
from app.models import Usuario


def activate_premium():
    """Atualiza usuário para plano Premium"""
    db = SessionLocal()
    
    try:
        # Listar usuários
        usuarios = db.query(Usuario).all()
        
        if not usuarios:
            print("\n❌ Nenhum usuário encontrado!")
            return
        
        print("\n" + "=" * 60)
        print("👥 USUÁRIOS DISPONÍVEIS")
        print("=" * 60)
        
        for i, user in enumerate(usuarios, 1):
            status = "⭐ PREMIUM" if user.tipo_plano == "premium" else "🆓 GRATUITO"
            print(f"{i}. {user.email} - {status}")
        
        print("=" * 60)
        
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
        print(f"\n❌ Erro: {e}")
        db.rollback()
        import traceback
        traceback.print_exc()
    finally:
        db.close()


if __name__ == "__main__":
    print("\n🚀 ATUALIZAR USUÁRIO PARA PREMIUM")
    activate_premium()