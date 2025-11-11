"""
Script simples para tornar usuário Premium
Execute: python tornar_premium_db.py
"""

import sqlite3

def listar_usuarios():
    conn = sqlite3.connect('visto_americano.db')
    cursor = conn.cursor()
    
    cursor.execute("SELECT id, email, tipo_plano FROM usuarios")
    usuarios = cursor.fetchall()
    
    conn.close()
    return usuarios

def atualizar_premium(user_id):
    conn = sqlite3.connect('visto_americano.db')
    cursor = conn.cursor()
    
    cursor.execute("""
        UPDATE usuarios 
        SET tipo_plano = 'premium', 
            data_expiracao_premium = NULL 
        WHERE id = ?
    """, (user_id,))
    
    conn.commit()
    conn.close()

def main():
    print("\n" + "=" * 60)
    print("⭐ TORNAR USUÁRIO PREMIUM")
    print("=" * 60)
    
    usuarios = listar_usuarios()
    
    if not usuarios:
        print("\n❌ Nenhum usuário encontrado!")
        return
    
    print("\n👥 USUÁRIOS DISPONÍVEIS:\n")
    
    for i, (user_id, email, plano) in enumerate(usuarios, 1):
        status = "⭐ PREMIUM" if plano == "premium" else "🆓 GRATUITO"
        print(f"{i}. {email} - {status}")
    
    print("\n" + "=" * 60)
    
    try:
        escolha = input("\nDigite o número do usuário para tornar PREMIUM (ou 0 para sair): ")
        
        if escolha == "0":
            print("❌ Operação cancelada.")
            return
        
        indice = int(escolha) - 1
        
        if indice < 0 or indice >= len(usuarios):
            print("❌ Número inválido!")
            return
        
        user_id, email, plano_atual = usuarios[indice]
        
        if plano_atual == "premium":
            print(f"\n⚠️  {email} já é PREMIUM!")
            return
        
        print(f"\n⚠️  Você vai atualizar:")
        print(f"   📧 Email: {email}")
        print(f"   📊 Plano atual: {plano_atual.upper()}")
        
        confirmar = input("\n✅ Confirmar atualização para PREMIUM? (s/n): ")
        
        if confirmar.lower() != 's':
            print("❌ Operação cancelada.")
            return
        
        atualizar_premium(user_id)
        
        print("\n" + "=" * 60)
        print("🎉 USUÁRIO ATUALIZADO COM SUCESSO!")
        print("=" * 60)
        print(f"   📧 Email: {email}")
        print(f"   💳 Plano: PREMIUM ⭐")
        print(f"   ⏰ Validade: VITALÍCIO ♾️")
        print("=" * 60 + "\n")
        
    except ValueError:
        print("❌ Digite apenas números!")
    except Exception as e:
        print(f"❌ Erro: {e}")

if __name__ == "__main__":
    main()
