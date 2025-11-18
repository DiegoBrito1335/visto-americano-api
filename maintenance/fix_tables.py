import psycopg2

# Sua DATABASE_URL
DATABASE_URL = "postgresql://postgres:yLqSvgitoigRDPJCDdzuVfVnuqPMyfQz@ballast.proxy.rlwy.net:38147/railway"

print("Conectando ao PostgreSQL...")
conn = psycopg2.connect(DATABASE_URL)
cursor = conn.cursor()
print("✅ Conectado!")

print("\nAdicionando coluna 'gratuito' às tabelas...")

try:
    cursor.execute("ALTER TABLE perguntas_ds160 ADD COLUMN IF NOT EXISTS gratuito BOOLEAN DEFAULT FALSE;")
    cursor.execute("ALTER TABLE perguntas_ds160 ADD COLUMN IF NOT EXISTS ordem INTEGER DEFAULT 0;")
    print("✅ Colunas adicionadas em perguntas_ds160!")
except Exception as e:
    print(f"⚠️ Erro em perguntas_ds160: {e}")

try:
    cursor.execute("ALTER TABLE perguntas_entrevista ADD COLUMN IF NOT EXISTS gratuito BOOLEAN DEFAULT FALSE;")
    cursor.execute("ALTER TABLE perguntas_entrevista ADD COLUMN IF NOT EXISTS ordem INTEGER DEFAULT 0;")
    print("✅ Colunas adicionadas em perguntas_entrevista!")
except Exception as e:
    print(f"⚠️ Erro em perguntas_entrevista: {e}")

conn.commit()
print("\n✅ Tabelas corrigidas com sucesso!")

cursor.close()
conn.close()