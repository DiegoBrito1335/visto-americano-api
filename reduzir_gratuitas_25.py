"""
Script para reduzir perguntas gratuitas de 38 para 25
Mantém distribuição proporcional entre DS-160 e Entrevista
"""
import sqlite3
import random

def reduzir_gratuitas():
    conn = sqlite3.connect('visto_americano.db')
    cursor = conn.cursor()
    
    print("=" * 70)
    print("REDUÇÃO DE PERGUNTAS GRATUITAS PARA 25")
    print("=" * 70)
    
    # 1. Verificar situação atual
    cursor.execute("SELECT COUNT(*) FROM perguntas_ds160 WHERE gratuita = 1")
    gratuitas_ds160_atual = cursor.fetchone()[0]
    
    cursor.execute("SELECT COUNT(*) FROM perguntas_entrevista WHERE gratuita = 1")
    gratuitas_entrevista_atual = cursor.fetchone()[0]
    
    total_gratuitas_atual = gratuitas_ds160_atual + gratuitas_entrevista_atual
    
    print(f"\n📊 SITUAÇÃO ATUAL:")
    print(f"   Total de gratuitas: {total_gratuitas_atual}")
    print(f"   - DS-160: {gratuitas_ds160_atual} perguntas")
    print(f"   - Entrevista: {gratuitas_entrevista_atual} perguntas")
    
    if total_gratuitas_atual <= 25:
        print(f"\n✅ Já temos {total_gratuitas_atual} perguntas gratuitas (meta: 25)")
        print("   Nenhuma ação necessária!")
        conn.close()
        return
    
    # 2. Calcular nova distribuição proporcional
    # Manter proporção: ~60% DS-160 (15) e ~40% Entrevista (10)
    nova_gratuitas_ds160 = 15
    nova_gratuitas_entrevista = 10
    
    print(f"\n🎯 NOVA META:")
    print(f"   Total de gratuitas: 25")
    print(f"   - DS-160: {nova_gratuitas_ds160} perguntas")
    print(f"   - Entrevista: {nova_gratuitas_entrevista} perguntas")
    
    # 3. Pegar IDs das perguntas atualmente gratuitas
    cursor.execute("SELECT id FROM perguntas_ds160 WHERE gratuita = 1")
    ids_gratuitas_ds160 = [row[0] for row in cursor.fetchall()]
    
    cursor.execute("SELECT id FROM perguntas_entrevista WHERE gratuita = 1")
    ids_gratuitas_entrevista = [row[0] for row in cursor.fetchall()]
    
    # 4. Selecionar aleatoriamente quais manter como gratuitas
    manter_ds160 = random.sample(ids_gratuitas_ds160, nova_gratuitas_ds160)
    manter_entrevista = random.sample(ids_gratuitas_entrevista, nova_gratuitas_entrevista)
    
    # 5. Marcar TODAS como premium primeiro
    print(f"\n🔄 Processando...")
    cursor.execute("UPDATE perguntas_ds160 SET gratuita = 0")
    cursor.execute("UPDATE perguntas_entrevista SET gratuita = 0")
    
    # 6. Marcar apenas as selecionadas como gratuitas
    for id_pergunta in manter_ds160:
        cursor.execute("UPDATE perguntas_ds160 SET gratuita = 1 WHERE id = ?", (id_pergunta,))
    
    for id_pergunta in manter_entrevista:
        cursor.execute("UPDATE perguntas_entrevista SET gratuita = 1 WHERE id = ?", (id_pergunta,))
    
    conn.commit()
    
    # 7. Verificar resultado final
    cursor.execute("SELECT COUNT(*) FROM perguntas_ds160 WHERE gratuita = 1")
    final_ds160 = cursor.fetchone()[0]
    
    cursor.execute("SELECT COUNT(*) FROM perguntas_entrevista WHERE gratuita = 1")
    final_entrevista = cursor.fetchone()[0]
    
    cursor.execute("SELECT COUNT(*) FROM perguntas_ds160 WHERE gratuita = 0")
    premium_ds160 = cursor.fetchone()[0]
    
    cursor.execute("SELECT COUNT(*) FROM perguntas_entrevista WHERE gratuita = 0")
    premium_entrevista = cursor.fetchone()[0]
    
    total_final_gratuitas = final_ds160 + final_entrevista
    total_premium = premium_ds160 + premium_entrevista
    
    print(f"\n" + "=" * 70)
    print("✅ REDUÇÃO CONCLUÍDA COM SUCESSO!")
    print("=" * 70)
    
    print(f"\n📈 RESULTADO FINAL:")
    print(f"\n   🆓 GRATUITAS: {total_final_gratuitas} perguntas")
    print(f"      - DS-160: {final_ds160} perguntas")
    print(f"      - Entrevista: {final_entrevista} perguntas")
    
    print(f"\n   💎 PREMIUM: {total_premium} perguntas")
    print(f"      - DS-160: {premium_ds160} perguntas")
    print(f"      - Entrevista: {premium_entrevista} perguntas")
    
    print(f"\n   📊 TOTAL: {total_final_gratuitas + total_premium} perguntas")
    
    # Mostrar exemplos das perguntas gratuitas
    print(f"\n" + "=" * 70)
    print("📝 EXEMPLOS DE PERGUNTAS QUE FICARAM GRATUITAS:")
    print("=" * 70)
    
    cursor.execute("""
        SELECT id, texto_pergunta 
        FROM perguntas_ds160 
        WHERE gratuita = 1 
        LIMIT 5
    """)
    print("\n   📋 DS-160 (primeiras 5):")
    for id_p, texto in cursor.fetchall():
        texto_curto = texto[:70] + "..." if len(texto) > 70 else texto
        print(f"      [{id_p}] {texto_curto}")
    
    cursor.execute("""
        SELECT id, texto_pergunta 
        FROM perguntas_entrevista 
        WHERE gratuita = 1 
        LIMIT 5
    """)
    print("\n   🎤 ENTREVISTA (primeiras 5):")
    for id_p, texto in cursor.fetchall():
        texto_curto = texto[:70] + "..." if len(texto) > 70 else texto
        print(f"      [{id_p}] {texto_curto}")
    
    print(f"\n" + "=" * 70)
    print("🎉 Agora os usuários GRATUITOS terão acesso a apenas 25 perguntas!")
    print("🎉 Os usuários PREMIUM continuam com acesso às 90 perguntas!")
    print("=" * 70)
    
    conn.close()

if __name__ == "__main__":
    try:
        reduzir_gratuitas()
    except Exception as e:
        print(f"\n❌ ERRO: {e}")
        import traceback
        traceback.print_exc()
