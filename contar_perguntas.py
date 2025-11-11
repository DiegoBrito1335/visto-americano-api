"""
Script para contar perguntas no banco de dados
Execute: python contar_perguntas.py
"""

import sqlite3

def contar_perguntas():
    try:
        conn = sqlite3.connect('visto_americano.db')
        cursor = conn.cursor()
        
        print("\n" + "=" * 80)
        print("📊 CONTAGEM DE PERGUNTAS NO BANCO")
        print("=" * 80)
        
        # DS-160
        cursor.execute("SELECT COUNT(*) FROM perguntas_ds160")
        total_ds160 = cursor.fetchone()[0]
        
        cursor.execute("SELECT COUNT(*) FROM perguntas_ds160 WHERE gratuito = 1")
        gratuitas_ds160 = cursor.fetchone()[0]
        
        cursor.execute("SELECT COUNT(*) FROM perguntas_ds160 WHERE gratuito = 0")
        premium_ds160 = cursor.fetchone()[0]
        
        # Entrevista
        cursor.execute("SELECT COUNT(*) FROM perguntas_entrevista")
        total_entrevista = cursor.fetchone()[0]
        
        cursor.execute("SELECT COUNT(*) FROM perguntas_entrevista WHERE gratuito = 1")
        gratuitas_entrevista = cursor.fetchone()[0]
        
        cursor.execute("SELECT COUNT(*) FROM perguntas_entrevista WHERE gratuito = 0")
        premium_entrevista = cursor.fetchone()[0]
        
        print(f"\n📝 PERGUNTAS DS-160:")
        print(f"   Total: {total_ds160}")
        print(f"   🆓 Gratuitas: {gratuitas_ds160}")
        print(f"   ⭐ Premium: {premium_ds160}")
        
        print(f"\n💬 PERGUNTAS ENTREVISTA:")
        print(f"   Total: {total_entrevista}")
        print(f"   🆓 Gratuitas: {gratuitas_entrevista}")
        print(f"   ⭐ Premium: {premium_entrevista}")
        
        print(f"\n🎯 RESUMO:")
        print(f"   Total Geral: {total_ds160 + total_entrevista}")
        print(f"   🆓 Total Gratuitas: {gratuitas_ds160 + gratuitas_entrevista}")
        print(f"   ⭐ Total Premium: {premium_ds160 + premium_entrevista}")
        print(f"   📊 Gratuitas + Premium: {gratuitas_ds160 + gratuitas_entrevista + premium_ds160 + premium_entrevista}")
        
        print("=" * 80 + "\n")
        
        conn.close()
        
    except Exception as e:
        print(f"❌ Erro: {e}")

if __name__ == "__main__":
    contar_perguntas()
