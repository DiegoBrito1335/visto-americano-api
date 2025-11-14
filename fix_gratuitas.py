import psycopg2
import os

# String de conexão do Railway
DATABASE_URL = "postgresql://postgres:yLqSvgitoigRDPJCDdzuVfVnuqPMyfQz@ballast.proxy.rlwy.net:38147/railway"

def marcar_perguntas_gratuitas():
    """Marca as primeiras 15 perguntas DS-160 e todas as 10 de entrevista como gratuitas"""
    
    try:
        # Conectar ao banco
        conn = psycopg2.connect(DATABASE_URL)
        cur = conn.cursor()
        
        print("=" * 70)
        print("🔧 MARCANDO PERGUNTAS COMO GRATUITAS")
        print("=" * 70)
        
        # 1. Marcar as primeiras 15 perguntas DS-160 como gratuitas
        cur.execute("""
            UPDATE perguntas_ds160 
            SET gratuita = true 
            WHERE id <= 15;
        """)
        
        rows_updated_ds160 = cur.rowcount
        print(f"\n✅ DS-160: {rows_updated_ds160} perguntas marcadas como GRATUITAS (IDs 1-15)")
        
        # 2. Marcar TODAS as perguntas de Entrevista como gratuitas
        cur.execute("""
            UPDATE perguntas_entrevista 
            SET gratuita = true;
        """)
        
        rows_updated_entrevista = cur.rowcount
        print(f"✅ ENTREVISTA: {rows_updated_entrevista} perguntas marcadas como GRATUITAS (TODAS)")
        
        # 3. Marcar as restantes DS-160 como premium (não gratuitas)
        cur.execute("""
            UPDATE perguntas_ds160 
            SET gratuita = false 
            WHERE id > 15;
        """)
        
        rows_updated_premium = cur.rowcount
        print(f"✅ DS-160: {rows_updated_premium} perguntas marcadas como PREMIUM (IDs 16+)")
        
        # Commit das mudanças
        conn.commit()
        
        print("\n" + "=" * 70)
        print("🎉 ATUALIZAÇÃO CONCLUÍDA COM SUCESSO!")
        print("=" * 70)
        
        # Verificar resultado
        cur.execute("SELECT COUNT(*) FROM perguntas_ds160 WHERE gratuita = true;")
        gratuitas_ds160 = cur.fetchone()[0]
        
        cur.execute("SELECT COUNT(*) FROM perguntas_entrevista WHERE gratuita = true;")
        gratuitas_entrevista = cur.fetchone()[0]
        
        print(f"\n📊 ESTATÍSTICAS FINAIS:")
        print(f"   - DS-160 Gratuitas: {gratuitas_ds160}")
        print(f"   - Entrevista Gratuitas: {gratuitas_entrevista}")
        print(f"   - Total Gratuitas: {gratuitas_ds160 + gratuitas_entrevista}")
        
        # Fechar conexão
        cur.close()
        conn.close()
        
        print("\n✅ Conexão fechada com sucesso!")
        print("\n🧪 TESTE AGORA:")
        print("   https://web-production-e07b4.up.railway.app/api/perguntas-ds160?gratuito=true")
        print("   https://web-production-e07b4.up.railway.app/api/perguntas/stats")
        
    except Exception as e:
        print(f"\n❌ ERRO: {e}")
        if conn:
            conn.rollback()
            conn.close()

if __name__ == "__main__":
    marcar_perguntas_gratuitas()