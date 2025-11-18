import psycopg2

DATABASE_URL = "postgresql://postgres:yLqSvgitoigRDPJCDdzuVfVnuqPMyfQz@ballast.proxy.rlwy.net:38147/railway"

print("REDUZINDO PARA 30 PERGUNTAS")
print("="*80)

conn = psycopg2.connect(DATABASE_URL)
cursor = conn.cursor()

cursor.execute("SELECT COUNT(*) FROM perguntas_ds160")
print(f"\nTotal atual: {cursor.fetchone()[0]} perguntas")

# IDs duplicados que você identificou
ids_remover = [28, 27, 26, 29, 33, 32]

print(f"\nIDs a remover: {ids_remover}")
print("\nPerguntas que serão removidas:\n")

for id in ids_remover:
    cursor.execute("SELECT pergunta_texto FROM perguntas_ds160 WHERE id = %s", (id,))
    resultado = cursor.fetchone()
    if resultado:
        print(f"ID {id}: {resultado[0][:70]}...")

resp = input("\nRemover? (SIM): ")

if resp == "SIM":
    cursor.execute(f"DELETE FROM perguntas_ds160 WHERE id IN ({','.join(map(str, ids_remover))})")
    conn.commit()
    print(f"\n✅ Removidas {cursor.rowcount} perguntas")
    
    cursor.execute("SELECT COUNT(*) FROM perguntas_ds160")
    total = cursor.fetchone()[0]
    print(f"Total agora: {total} perguntas")
    
    if total > 30:
        print(f"\n⚠️ Ainda tem {total-30} a mais. Vou listar para você escolher quais remover.")
        cursor.execute("SELECT id, pergunta_texto FROM perguntas_ds160 ORDER BY id")
        print("\n📋 PERGUNTAS RESTANTES:")
        for id, texto in cursor.fetchall():
            print(f"{id:3d}. {texto[:70]}...")

conn.close()
