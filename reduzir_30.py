import psycopg2

DATABASE_URL = "postgresql://postgres:yLqSvgitoigRDPJCDdzuVfVnuqPMyfQz@ballast.proxy.rlwy.net:38147/railway"

print("="*80)
print("REDUZINDO DS-160 PARA 30 PERGUNTAS")
print("="*80)

conn = psycopg2.connect(DATABASE_URL)
cursor = conn.cursor()

# IDs para REMOVER (20 perguntas menos essenciais)
# Mantendo as mais importantes para avaliação de visto
ids_remover = [
    135,  # Tempo na função - redundante
    138,  # Veículo próprio - pouco relevante  
    142,  # Passagens compradas - não essencial
    143,  # Hospedagem - não essencial
    145,  # Trabalhar nos EUA - óbvio
    151,  # Cartão crédito - menos importante
    153,  # Dívidas - muito detalhado
    154,  # Quantos países - número exato irrelevante
    156,  # Canadá/México - menos relevante
    158,  # Tempo visto negado - condicional
    159,  # Overstayed - muito específico
    160,  # Vistos outros países - menos relevante
    162,  # Tipo de viagem - redundante
    163,  # Intercâmbio - menos importante
    166,  # Tempo endereço - pouco relevante
    168,  # Organizações - menos importante
    169,  # Pets - irrelevante
    172,  # Seguro viagem - não decisivo
    175,  # Condição médica - muito específico
    177,  # Tatuagens - irrelevante
]

print(f"\n🗑️ Removendo {len(ids_remover)} perguntas:\n")

for id in ids_remover:
    cursor.execute("SELECT pergunta_texto, gratuita FROM perguntas_ds160 WHERE id = %s", (id,))
    resultado = cursor.fetchone()
    if resultado:
        texto, gratis = resultado
        tipo = "GRÁTIS" if gratis else "PREMIUM"
        print(f"❌ ID {id:3d} [{tipo}] {texto[:60]}...")

cursor.execute("SELECT COUNT(*) FROM perguntas_ds160")
atual = cursor.fetchone()[0]

print(f"\n{'='*80}")
print(f"Perguntas atuais: {atual}")
print(f"Após remoção: {atual - len(ids_remover)}")

resp = input("\nConfirmar? (SIM): ").upper()

if resp == "SIM":
    cursor.execute(f"DELETE FROM perguntas_ds160 WHERE id IN ({','.join(map(str, ids_remover))})")
    conn.commit()
    print(f"\n✅ Removidas {cursor.rowcount} perguntas!")
    
    cursor.execute("SELECT COUNT(*) FROM perguntas_ds160")
    total = cursor.fetchone()[0]
    
    cursor.execute("SELECT COUNT(*) FILTER (WHERE gratuita=true) FROM perguntas_ds160")
    gratis = cursor.fetchone()[0]
    
    print(f"\n📊 RESULTADO FINAL:")
    print(f"   Total: {total} perguntas")
    print(f"   Gratuitas: {gratis}")
    print(f"   Premium: {total - gratis}")
else:
    print("\n❌ Cancelado")

conn.close()
