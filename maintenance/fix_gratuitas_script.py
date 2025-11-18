import psycopg2
import os
from dotenv import load_dotenv

load_dotenv()

# Conectar ao PostgreSQL do Railway
DATABASE_URL = os.getenv("DATABASE_URL")

if not DATABASE_URL:
    print("❌ DATABASE_URL não encontrada no .env")
    exit(1)

print("🔗 Conectando ao PostgreSQL...")
conn = psycopg2.connect(DATABASE_URL)
cursor = conn.cursor()
print("✅ Conectado!")

# Verificar status atual
print("\n📊 Status ANTES da correção:")
cursor.execute("SELECT COUNT(*), gratuito FROM perguntas_ds160 GROUP BY gratuito ORDER BY gratuito")
ds160_antes = cursor.fetchall()
print(f"DS-160: {ds160_antes}")

cursor.execute("SELECT COUNT(*), gratuito FROM perguntas_entrevista GROUP BY gratuito ORDER BY gratuito")
entrevista_antes = cursor.fetchall()
print(f"Entrevista: {entrevista_antes}")

# Marcar perguntas como gratuitas
print("\n🔧 Marcando perguntas como gratuitas...")

# DS-160: primeiras 25 gratuitas
cursor.execute("UPDATE perguntas_ds160 SET gratuito = true WHERE ordem <= 25")
ds160_updated = cursor.rowcount
print(f"✅ {ds160_updated} perguntas DS-160 marcadas como gratuitas")

# Entrevista: primeiras 15 gratuitas
cursor.execute("UPDATE perguntas_entrevista SET gratuito = true WHERE ordem <= 15")
entrevista_updated = cursor.rowcount
print(f"✅ {entrevista_updated} perguntas Entrevista marcadas como gratuitas")

conn.commit()

# Verificar status após correção
print("\n📊 Status DEPOIS da correção:")
cursor.execute("SELECT COUNT(*), gratuito FROM perguntas_ds160 GROUP BY gratuito ORDER BY gratuito")
ds160_depois = cursor.fetchall()
print(f"DS-160: {ds160_depois}")

cursor.execute("SELECT COUNT(*), gratuito FROM perguntas_entrevista GROUP BY gratuito ORDER BY gratuito")
entrevista_depois = cursor.fetchall()
print(f"Entrevista: {entrevista_depois}")

# Contar total de gratuitas
cursor.execute("SELECT COUNT(*) FROM perguntas_ds160 WHERE gratuito = true")
total_ds160_gratis = cursor.fetchone()[0]

cursor.execute("SELECT COUNT(*) FROM perguntas_entrevista WHERE gratuito = true")
total_entrevista_gratis = cursor.fetchone()[0]

cursor.close()
conn.close()

print("\n" + "="*60)
print("🎉 CORREÇÃO CONCLUÍDA!")
print("="*60)
print(f"📊 DS-160 gratuitas: {total_ds160_gratis}")
print(f"📊 Entrevista gratuitas: {total_entrevista_gratis}")
print(f"📊 TOTAL GRATUITO: {total_ds160_gratis + total_entrevista_gratis}")
print("="*60)
print("\n✅ Agora teste o simulador novamente!")