"""
Script para verificar a estrutura das tabelas do banco de dados
"""
import sqlite3

def verificar_estrutura():
    conn = sqlite3.connect('visto_americano.db')
    cursor = conn.cursor()
    
    print("=" * 70)
    print("VERIFICANDO ESTRUTURA DO BANCO DE DADOS")
    print("=" * 70)
    
    # Listar todas as tabelas
    cursor.execute("SELECT name FROM sqlite_master WHERE type='table'")
    tabelas = cursor.fetchall()
    
    print(f"\n📊 TABELAS ENCONTRADAS: {len(tabelas)}")
    for tabela in tabelas:
        print(f"   - {tabela[0]}")
    
    # Verificar estrutura da tabela perguntas_ds160
    print(f"\n" + "=" * 70)
    print("📋 ESTRUTURA: perguntas_ds160")
    print("=" * 70)
    cursor.execute("PRAGMA table_info(perguntas_ds160)")
    colunas_ds160 = cursor.fetchall()
    
    if colunas_ds160:
        print("\nColunas:")
        for col in colunas_ds160:
            print(f"   {col[1]} ({col[2]})")
    else:
        print("   ❌ Tabela não encontrada!")
    
    # Verificar estrutura da tabela perguntas_entrevista
    print(f"\n" + "=" * 70)
    print("📋 ESTRUTURA: perguntas_entrevista")
    print("=" * 70)
    cursor.execute("PRAGMA table_info(perguntas_entrevista)")
    colunas_entrevista = cursor.fetchall()
    
    if colunas_entrevista:
        print("\nColunas:")
        for col in colunas_entrevista:
            print(f"   {col[1]} ({col[2]})")
    else:
        print("   ❌ Tabela não encontrada!")
    
    # Contar perguntas
    print(f"\n" + "=" * 70)
    print("📈 QUANTIDADE DE PERGUNTAS")
    print("=" * 70)
    
    try:
        cursor.execute("SELECT COUNT(*) FROM perguntas_ds160")
        total_ds160 = cursor.fetchone()[0]
        print(f"   DS-160: {total_ds160} perguntas")
    except:
        print(f"   DS-160: ❌ Erro ao contar")
    
    try:
        cursor.execute("SELECT COUNT(*) FROM perguntas_entrevista")
        total_entrevista = cursor.fetchone()[0]
        print(f"   Entrevista: {total_entrevista} perguntas")
    except:
        print(f"   Entrevista: ❌ Erro ao contar")
    
    # Verificar se existe coluna 'gratuita'
    print(f"\n" + "=" * 70)
    print("🔍 VERIFICANDO COLUNA 'gratuita'")
    print("=" * 70)
    
    tem_gratuita_ds160 = any(col[1] == 'gratuita' for col in colunas_ds160)
    tem_gratuita_entrevista = any(col[1] == 'gratuita' for col in colunas_entrevista)
    
    print(f"\n   perguntas_ds160: {'✅ TEM' if tem_gratuita_ds160 else '❌ NÃO TEM'}")
    print(f"   perguntas_entrevista: {'✅ TEM' if tem_gratuita_entrevista else '❌ NÃO TEM'}")
    
    if not tem_gratuita_ds160 or not tem_gratuita_entrevista:
        print(f"\n" + "=" * 70)
        print("⚠️  ATENÇÃO: COLUNA 'gratuita' NÃO EXISTE!")
        print("=" * 70)
        print("\n   É necessário adicionar a coluna 'gratuita' nas tabelas.")
        print("   Vou criar um script para fazer isso automaticamente.")
    else:
        print(f"\n✅ Coluna 'gratuita' encontrada em ambas as tabelas!")
    
    # Mostrar exemplo de 3 perguntas
    print(f"\n" + "=" * 70)
    print("📝 EXEMPLO DE PERGUNTAS (primeiras 3)")
    print("=" * 70)
    
    cursor.execute("SELECT * FROM perguntas_ds160 LIMIT 3")
    print("\n   DS-160:")
    for row in cursor.fetchall():
        print(f"      {row}")
    
    cursor.execute("SELECT * FROM perguntas_entrevista LIMIT 3")
    print("\n   ENTREVISTA:")
    for row in cursor.fetchall():
        print(f"      {row}")
    
    conn.close()

if __name__ == "__main__":
    try:
        verificar_estrutura()
    except Exception as e:
        print(f"\n❌ ERRO: {e}")
        import traceback
        traceback.print_exc()
