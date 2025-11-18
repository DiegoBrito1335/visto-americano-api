import psycopg2

conn = psycopg2.connect('postgresql://postgres:yLqSvgitoigRDPJCDdzuVfVnuqPMyfQz@ballast.proxy.rlwy.net:38147/railway')
cursor = conn.cursor()

print("="*80)
print("ANÁLISE COMPLETA DO BANCO DE PERGUNTAS")
print("="*80)

# Contar DS-160
cursor.execute('SELECT COUNT(*), COUNT(*) FILTER (WHERE gratuita=true) FROM perguntas_ds160')
ds160_total, ds160_gratis = cursor.fetchone()

# Contar Entrevista
cursor.execute('SELECT COUNT(*), COUNT(*) FILTER (WHERE gratuita=true) FROM perguntas_entrevista')
entrevista_total, entrevista_gratis = cursor.fetchone()

print(f"\n📊 PERGUNTAS DS-160:")
print(f"   Total: {ds160_total}")
print(f"   Gratuitas: {ds160_gratis}")
print(f"   Premium: {ds160_total - ds160_gratis}")

print(f"\n📊 PERGUNTAS ENTREVISTA:")
print(f"   Total: {entrevista_total}")
print(f"   Gratuitas: {entrevista_gratis}")
print(f"   Premium: {entrevista_total - entrevista_gratis}")

print(f"\n📊 TOTAL GERAL:")
print(f"   {ds160_total + entrevista_total} perguntas")
print(f"   {ds160_gratis + entrevista_gratis} gratuitas")
print(f"   {(ds160_total - ds160_gratis) + (entrevista_total - entrevista_gratis)} premium")

# Listar todas DS-160
print(f"\n{'='*80}")
print(f"📋 TODAS AS PERGUNTAS DS-160 ({ds160_total}):\n")
cursor.execute('SELECT id, pergunta_texto, gratuita FROM perguntas_ds160 ORDER BY id')
for id, texto, gratis in cursor.fetchall():
    tipo = "GRÁTIS" if gratis else "PREMIUM"
    print(f"ID {id:3d} [{tipo:7s}] {texto[:70]}...")

conn.close()
print(f"\n{'='*80}")
