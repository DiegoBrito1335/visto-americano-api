"""
Script simples para verificar usuários no banco
Execute: python verificar_db.py
"""

import sqlite3
from datetime import datetime

def verificar_usuarios():
    try:
        # Conectar ao banco SQLite
        conn = sqlite3.connect('visto_americano.db')
        cursor = conn.cursor()
        
        # Buscar todos os usuários
        cursor.execute("SELECT id, email, nome_completo, tipo_plano, data_cadastro, ativo FROM usuarios")
        usuarios = cursor.fetchall()
        
        if not usuarios:
            print("❌ Nenhum usuário encontrado no banco de dados!")
            return
        
        print("\n" + "=" * 80)
        print("👥 USUÁRIOS NO BANCO DE DADOS")
        print("=" * 80)
        
        gratuitos = 0
        premium = 0
        
        for user in usuarios:
            user_id, email, nome, plano, cadastro, ativo = user
            
            if plano == "gratuito":
                gratuitos += 1
            else:
                premium += 1
            
            print(f"\n🔹 USUÁRIO #{user_id}")
            print(f"   📧 Email: {email}")
            print(f"   👤 Nome: {nome}")
            print(f"   💳 Plano: {plano.upper()}")
            print(f"   📅 Cadastro: {cadastro}")
            print(f"   ✅ Ativo: {'Sim' if ativo else 'Não'}")
            print("-" * 80)
        
        print(f"\n📊 TOTAL: {len(usuarios)} usuário(s)")
        print(f"\n📈 ESTATÍSTICAS:")
        print(f"   🆓 Gratuitos: {gratuitos}")
        print(f"   ⭐ Premium: {premium}")
        print("=" * 80 + "\n")
        
        conn.close()
        
    except sqlite3.Error as e:
        print(f"❌ Erro ao acessar banco de dados: {e}")
    except Exception as e:
        print(f"❌ Erro: {e}")

if __name__ == "__main__":
    print("\n🔍 VERIFICANDO BANCO DE DADOS...\n")
    verificar_usuarios()
