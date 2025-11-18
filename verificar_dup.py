import psycopg2

DATABASE_URL = "postgresql://postgres:yLqSvgitoigRDPJCDdzuVfVnuqPMyfQz@ballast.proxy.rlwy.net:38147/railway"

print("Verificando duplicatas específicas...")
print("="*80)

conn = psycopg2.connect(DATABASE_URL)
cursor = conn.cursor()

# Pares reportados
pares = [(6,27), (11,26), (12,29), (13,30), (4,28), (32,19)]

duplicatas_reais = []

for id1, id2 in pares:
    cursor.execute("""
        SELECT id, pergunta_texto, categoria
        FROM perguntas_ds160
        WHERE id IN (%s, %s)
        ORDER BY id;
    """, (id1, id2))
    
    perguntas = cursor.fetchall()
    
    if len(perguntas) == 2:
        p1 = perguntas[0]
        p2 = perguntas[1]
        
        print(f"\nPar ({id1}, {id2}):")
        print(f"  ID {p1[0]}: {p1[1][:80]}")
        print(f"  ID {p2[0]}: {p2[1][:80]}")
        
        if p1[1].strip().lower() == p2[1].strip().lower():
            print("  -> DUPLICADAS (mesmo texto)")
            duplicatas_reais.append((id1, id2))
        else:
            print("  -> Textos diferentes")

print(f"\n{'='*80}")
print(f"\nDuplicatas confirmadas: {len(duplicatas_reais)}")

if duplicatas_reais:
    ids_remover = [max(par) for par in duplicatas_reais]
    print(f"IDs a remover: {ids_remover}")
    
    resp = input("\nRemover duplicatas? (SIM): ")
    if resp == "SIM":
        cursor.execute(f"DELETE FROM perguntas_ds160 WHERE id IN ({','.join(map(str, ids_remover))})")
        conn.commit()
        print(f"Removidos {cursor.rowcount} registros")

cursor.execute("SELECT COUNT(*) FROM perguntas_ds160")
print(f"\nTotal de perguntas DS-160: {cursor.fetchone()[0]}")

conn.close()
