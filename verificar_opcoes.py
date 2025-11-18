import psycopg2

conn = psycopg2.connect('postgresql://postgres:yLqSvgitoigRDPJCDdzuVfVnuqPMyfQz@ballast.proxy.rlwy.net:38147/railway')
cur = conn.cursor()

cur.execute("SELECT id, pergunta_texto, tipo_resposta, opcoes FROM perguntas_ds160 WHERE pergunta_texto LIKE '%estado civil%'")
resultado = cur.fetchone()

print('ID:', resultado[0])
print('Pergunta:', resultado[1])
print('Tipo:', resultado[2])
print('Opções:', resultado[3])
print('Tipo das opções:', type(resultado[3]))

conn.close()