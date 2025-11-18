import psycopg2

conn = psycopg2.connect('postgresql://postgres:yLqSvgitoigRDPJCDdzuVfVnuqPMyfQz@ballast.proxy.rlwy.net:38147/railway')
cur = conn.cursor()

# Atualizar para premium
cur.execute("UPDATE usuarios SET tipo_plano = 'premium' WHERE email = 'teste999@gmail.com'")
conn.commit()

print('✅ teste999@gmail.com agora é Premium!')

# Verificar
cur.execute("SELECT email, tipo_plano FROM usuarios WHERE email = 'teste999@gmail.com'")
resultado = cur.fetchone()
print(f'Email: {resultado[0]} | Plano: {resultado[1]}')

conn.close()