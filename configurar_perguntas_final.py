"""
Script COMPLETO para configurar perguntas gratuitas vs premium
1. Adiciona coluna 'gratuita' se não existir
2. Marca 25 perguntas como gratuitas (15 DS-160 + 10 Entrevista)
3. Marca 65 perguntas como premium
"""
import sqlite3
import random

def configurar_perguntas_gratuitas():
    conn = sqlite3.connect('visto_americano.db')
    cursor = conn.cursor()
    
    print("=" * 70)
    print("CONFIGURAÇÃO DE PERGUNTAS GRATUITAS")
    print("=" * 70)
    
    # PASSO 1: Verificar se coluna 'gratuita' existe
    print("\n🔍 PASSO 1: Verificando estrutura das tabelas...")
    
    cursor.execute("PRAGMA table_info(perguntas_ds160)")
    colunas_ds160 = [col[1] for col in cursor.fetchall()]
    tem_gratuita_ds160 = 'gratuita' in colunas_ds160
    
    cursor.execute("PRAGMA table_info(perguntas_entrevista)")
    colunas_entrevista = [col[1] for col in cursor.fetchall()]
    tem_gratuita_entrevista = 'gratuita' in colunas_entrevista
    
    # PASSO 2: Adicionar coluna se não existir
    if not tem_gratuita_ds160:
        print("   ➕ Adicionando coluna 'gratuita' em perguntas_ds160...")
        cursor.execute("ALTER TABLE perguntas_ds160 ADD COLUMN gratuita BOOLEAN DEFAULT 0")
        print("   ✅ Coluna adicionada!")
    else:
        print("   ✅ Coluna 'gratuita' já existe em perguntas_ds160")
    
    if not tem_gratuita_entrevista:
        print("   ➕ Adicionando coluna 'gratuita' em perguntas_entrevista...")
        cursor.execute("ALTER TABLE perguntas_entrevista ADD COLUMN gratuita BOOLEAN DEFAULT 0")
        print("   ✅ Coluna adicionada!")
    else:
        print("   ✅ Coluna 'gratuita' já existe em perguntas_entrevista")
    
    conn.commit()
    
    # PASSO 3: Contar perguntas totais
    print("\n📊 PASSO 2: Contando perguntas...")
    
    cursor.execute("SELECT COUNT(*) FROM perguntas_ds160")
    total_ds160 = cursor.fetchone()[0]
    
    cursor.execute("SELECT COUNT(*) FROM perguntas_entrevista")
    total_entrevista = cursor.fetchone()[0]
    
    total_perguntas = total_ds160 + total_entrevista
    
    print(f"   DS-160: {total_ds160} perguntas")
    print(f"   Entrevista: {total_entrevista} perguntas")
    print(f"   Total: {total_perguntas} perguntas")
    
    # PASSO 4: Marcar TODAS como premium primeiro
    print("\n🔄 PASSO 3: Marcando todas as perguntas como PREMIUM...")
    cursor.execute("UPDATE perguntas_ds160 SET gratuita = 0")
    cursor.execute("UPDATE perguntas_entrevista SET gratuita = 0")
    conn.commit()
    print("   ✅ Todas marcadas como premium!")
    
    # PASSO 5: Selecionar 25 perguntas aleatórias para serem gratuitas
    print("\n🎲 PASSO 4: Selecionando 25 perguntas para serem GRATUITAS...")
    
    # Pegar todos os IDs
    cursor.execute("SELECT id FROM perguntas_ds160")
    ids_ds160 = [row[0] for row in cursor.fetchall()]
    
    cursor.execute("SELECT id FROM perguntas_entrevista")
    ids_entrevista = [row[0] for row in cursor.fetchall()]
    
    # Selecionar aleatoriamente
    # 15 do DS-160 (60% de 25)
    gratuitas_ds160 = random.sample(ids_ds160, min(15, len(ids_ds160)))
    
    # 10 da Entrevista (40% de 25)
    gratuitas_entrevista = random.sample(ids_entrevista, min(10, len(ids_entrevista)))
    
    print(f"   Selecionadas {len(gratuitas_ds160)} perguntas DS-160")
    print(f"   Selecionadas {len(gratuitas_entrevista)} perguntas Entrevista")
    
    # PASSO 6: Marcar as selecionadas como gratuitas
    print("\n✏️ PASSO 5: Marcando perguntas selecionadas como GRATUITAS...")
    
    for id_pergunta in gratuitas_ds160:
        cursor.execute("UPDATE perguntas_ds160 SET gratuita = 1 WHERE id = ?", (id_pergunta,))
    
    for id_pergunta in gratuitas_entrevista:
        cursor.execute("UPDATE perguntas_entrevista SET gratuita = 1 WHERE id = ?", (id_pergunta,))
    
    conn.commit()
    print("   ✅ Perguntas marcadas!")
    
    # PASSO 7: Verificar resultado final
    print("\n🔍 PASSO 6: Verificando resultado...")
    
    cursor.execute("SELECT COUNT(*) FROM perguntas_ds160 WHERE gratuita = 1")
    gratuitas_ds160_final = cursor.fetchone()[0]
    
    cursor.execute("SELECT COUNT(*) FROM perguntas_entrevista WHERE gratuita = 1")
    gratuitas_entrevista_final = cursor.fetchone()[0]
    
    cursor.execute("SELECT COUNT(*) FROM perguntas_ds160 WHERE gratuita = 0")
    premium_ds160 = cursor.fetchone()[0]
    
    cursor.execute("SELECT COUNT(*) FROM perguntas_entrevista WHERE gratuita = 0")
    premium_entrevista = cursor.fetchone()[0]
    
    total_gratuitas = gratuitas_ds160_final + gratuitas_entrevista_final
    total_premium = premium_ds160 + premium_entrevista
    
    # RESULTADO FINAL
    print("\n" + "=" * 70)
    print("✅ CONFIGURAÇÃO CONCLUÍDA COM SUCESSO!")
    print("=" * 70)
    
    print(f"\n📊 RESUMO FINAL:")
    print(f"\n   🆓 PERGUNTAS GRATUITAS: {total_gratuitas}")
    print(f"      ├─ DS-160: {gratuitas_ds160_final} perguntas")
    print(f"      └─ Entrevista: {gratuitas_entrevista_final} perguntas")
    
    print(f"\n   💎 PERGUNTAS PREMIUM: {total_premium}")
    print(f"      ├─ DS-160: {premium_ds160} perguntas")
    print(f"      └─ Entrevista: {premium_entrevista} perguntas")
    
    print(f"\n   📈 TOTAL: {total_gratuitas + total_premium} perguntas")
    
    # Mostrar exemplos
    print(f"\n" + "=" * 70)
    print("📝 EXEMPLOS DE PERGUNTAS GRATUITAS:")
    print("=" * 70)
    
    cursor.execute("""
        SELECT id, pergunta_texto 
        FROM perguntas_ds160 
        WHERE gratuita = 1 
        LIMIT 5
    """)
    print("\n   📋 DS-160:")
    for id_p, texto in cursor.fetchall():
        texto_curto = texto[:60] + "..." if len(texto) > 60 else texto
        print(f"      [{id_p}] {texto_curto}")
    
    cursor.execute("""
        SELECT id, pergunta_texto 
        FROM perguntas_entrevista 
        WHERE gratuita = 1 
        LIMIT 5
    """)
    print("\n   🎤 ENTREVISTA:")
    for id_p, texto in cursor.fetchall():
        texto_curto = texto[:60] + "..." if len(texto) > 60 else texto
        print(f"      [{id_p}] {texto_curto}")
    
    print(f"\n" + "=" * 70)
    print("🎉 AGORA O SISTEMA ESTÁ CONFIGURADO CORRETAMENTE!")
    print("=" * 70)
    print("\n   ✅ Usuários GRATUITOS: 25 perguntas")
    print("   ✅ Usuários PREMIUM: 90 perguntas (todas)")
    print("\n" + "=" * 70)
    
    conn.close()

if __name__ == "__main__":
    try:
        configurar_perguntas_gratuitas()
    except Exception as e:
        print(f"\n❌ ERRO: {e}")
        import traceback
        traceback.print_exc()
