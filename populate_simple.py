import psycopg2
import json

# SUBSTITUA PELA SUA DATABASE_URL DO RAILWAY
DATABASE_URL = "postgresql://postgres:yLqSvgitoigRDPJCDdzuVfVnuqPMyfQz@ballast.proxy.rlwy.net:38147/railway"

# Conectar ao banco
print("Conectando ao PostgreSQL...")
conn = psycopg2.connect(DATABASE_URL)
cursor = conn.cursor()
print("✅ Conectado!")

# Criar tabelas (se não existirem)
print("\nCriando tabelas...")

cursor.execute("""
CREATE TABLE IF NOT EXISTS perguntas_ds160 (
    id SERIAL PRIMARY KEY,
    categoria VARCHAR NOT NULL,
    pergunta_texto VARCHAR NOT NULL,
    tipo_resposta VARCHAR DEFAULT 'texto',
    opcoes JSON,
    resposta_ideal VARCHAR,
    peso_avaliacao INTEGER DEFAULT 5,
    dica VARCHAR,
    gratuito BOOLEAN DEFAULT FALSE,
    ordem INTEGER DEFAULT 0
);
""")

cursor.execute("""
CREATE TABLE IF NOT EXISTS perguntas_entrevista (
    id SERIAL PRIMARY KEY,
    categoria VARCHAR NOT NULL,
    pergunta_texto VARCHAR NOT NULL,
    resposta_ideal VARCHAR,
    palavras_positivas JSON,
    palavras_negativas JSON,
    peso_avaliacao INTEGER DEFAULT 5,
    dica VARCHAR,
    gratuito BOOLEAN DEFAULT FALSE,
    ordem INTEGER DEFAULT 0
);
""")

conn.commit()
print("✅ Tabelas criadas!")

# Verificar se já existem perguntas
cursor.execute("SELECT COUNT(*) FROM perguntas_ds160")
count_ds160 = cursor.fetchone()[0]

cursor.execute("SELECT COUNT(*) FROM perguntas_entrevista")
count_entrevista = cursor.fetchone()[0]

if count_ds160 > 0 or count_entrevista > 0:
    print(f"\n⚠️ Banco já tem perguntas: {count_ds160} DS-160, {count_entrevista} Entrevista")
    resposta = input("Deseja apagar e recriar? (s/n): ")
    if resposta.lower() == 's':
        cursor.execute("DELETE FROM perguntas_ds160")
        cursor.execute("DELETE FROM perguntas_entrevista")
        conn.commit()
        print("✅ Perguntas antigas removidas!")
    else:
        print("❌ Cancelado.")
        exit()

# Inserir perguntas DS-160 (apenas as primeiras 25 como exemplo)
print("\n📝 Inserindo perguntas DS-160...")

perguntas_ds160 = [
    ("pessoal", "Qual é o seu nome completo conforme aparece no passaporte?", "texto", None, None, 3, "Use exatamente como está no passaporte", True, 1),
    ("pessoal", "Você já usou outros nomes?", "texto", None, None, 4, "Inclua nomes de solteira, apelidos oficiais", True, 2),
    ("pessoal", "Qual é o seu sexo?", "multipla_escolha", json.dumps(["Masculino", "Feminino"]), None, 2, None, True, 3),
    ("pessoal", "Qual é o seu estado civil?", "multipla_escolha", json.dumps(["Solteiro(a)", "Casado(a)", "Divorciado(a)", "Viúvo(a)", "União Estável"]), None, 5, "Estado civil correto é importante", True, 4),
    ("pessoal", "Qual é a sua data de nascimento?", "texto", None, None, 2, None, True, 5),
    ("pessoal", "Qual é o seu local de nascimento (cidade, estado, país)?", "texto", None, None, 3, None, True, 6),
    ("pessoal", "Qual é a sua nacionalidade atual?", "texto", None, None, 3, None, True, 7),
    ("pessoal", "Você possui outra nacionalidade além da atual?", "texto", None, None, 4, "Dupla cidadania deve ser mencionada", True, 8),
    ("pessoal", "Qual é o seu número de identificação nacional (CPF)?", "texto", None, None, 2, None, True, 9),
    ("pessoal", "Qual é o seu número de passaporte?", "texto", None, None, 3, None, True, 10),
    ("vinculos", "Qual é o seu endereço residencial completo no Brasil?", "texto", None, None, 5, "Endereço real e comprovável", True, 11),
    ("vinculos", "Há quanto tempo você mora neste endereço?", "texto", None, None, 6, "Estabilidade residencial é positiva", True, 12),
    ("vinculos", "Qual é o seu número de telefone residencial?", "texto", None, None, 3, None, True, 13),
    ("vinculos", "Qual é o seu número de telefone celular?", "texto", None, None, 3, None, True, 14),
    ("vinculos", "Qual é o seu endereço de e-mail?", "texto", None, None, 3, None, True, 15),
    ("vinculos", "Você está empregado atualmente?", "multipla_escolha", json.dumps(["Sim", "Não", "Autônomo", "Aposentado", "Estudante"]), None, 8, "Emprego formal é muito positivo", False, 16),
    ("vinculos", "Qual é o nome da sua empresa/empregador atual?", "texto", None, None, 7, "Nome oficial da empresa", False, 17),
    ("vinculos", "Qual é o seu cargo/função na empresa?", "texto", None, None, 6, None, False, 18),
    ("vinculos", "Há quanto tempo você trabalha nesta empresa?", "texto", None, None, 7, "Tempo de trabalho demonstra estabilidade", False, 19),
    ("vinculos", "Qual é o endereço da sua empresa?", "texto", None, None, 5, None, False, 20),
    ("vinculos", "Qual é o número de telefone da sua empresa?", "texto", None, None, 4, None, False, 21),
    ("vinculos", "Qual é a sua renda mensal aproximada?", "texto", None, None, 8, "Seja honesto, será verificado", False, 22),
    ("vinculos", "Você possui bens imóveis no Brasil? Quais?", "texto", None, None, 9, "Propriedades são vínculos fortes", False, 23),
    ("vinculos", "Você possui veículos registrados em seu nome?", "texto", None, None, 5, None, False, 24),
    ("vinculos", "Qual é o seu nível de escolaridade?", "multipla_escolha", json.dumps(["Fundamental", "Médio", "Superior Incompleto", "Superior Completo", "Pós-graduação"]), None, 4, None, False, 25),
]

for pergunta in perguntas_ds160:
    cursor.execute("""
        INSERT INTO perguntas_ds160 
        (categoria, pergunta_texto, tipo_resposta, opcoes, resposta_ideal, peso_avaliacao, dica, gratuito, ordem)
        VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s)
    """, pergunta)

conn.commit()
print(f"✅ {len(perguntas_ds160)} perguntas DS-160 inseridas!")

# Inserir perguntas de entrevista (primeiras 10 como exemplo)
print("\n📝 Inserindo perguntas de Entrevista...")

perguntas_entrevista = [
    ("vinculos", "Por que você quer ir para os Estados Unidos?", "Para turismo/negócios com retorno programado ao Brasil", json.dumps(["turismo", "férias", "conhecer", "visitar", "retornar", "voltar", "temporário"]), json.dumps(["morar", "ficar", "trabalhar ilegalmente", "não voltar"]), 10, "Seja claro sobre seu objetivo e intenção de retorno", True, 1),
    ("vinculos", "O que você faz no Brasil? Qual é sua profissão?", "Trabalho como [profissão] há [tempo] na empresa [nome]", json.dumps(["trabalho", "empregado", "empresa", "anos", "estável", "cargo"]), json.dumps(["desempregado", "procurando", "bicos"]), 9, "Demonstre estabilidade profissional", True, 2),
    ("vinculos", "Você tem família no Brasil? Quem?", "Sim, tenho [cônjuge/pais/filhos] que dependem de mim", json.dumps(["esposa", "marido", "filhos", "pais", "família", "moram comigo"]), json.dumps(["sozinho", "sem família", "todos nos EUA"]), 9, "Vínculos familiares são muito importantes", True, 3),
    ("vinculos", "Você possui imóveis ou propriedades no Brasil?", "Sim, possuo [casa/apartamento] onde moro", json.dumps(["casa própria", "apartamento", "propriedade", "escritura", "financiamento"]), json.dumps(["não tenho", "moro de aluguel"]), 8, "Propriedades demonstram vínculos fortes", True, 4),
    ("vinculos", "Quanto tempo você pretende ficar nos Estados Unidos?", "[X] dias/semanas, com data de retorno definida", json.dumps(["dias", "uma semana", "duas semanas", "retorno marcado", "volta"]), json.dumps(["não sei", "quanto der", "muito tempo", "meses"]), 10, "Seja específico e razoável", True, 5),
    ("vinculos", "O que garante que você voltará ao Brasil?", "Meu emprego, família e propriedades estão aqui", json.dumps(["emprego", "família", "casa", "compromissos", "responsabilidades", "empresa"]), json.dumps(["não sei", "talvez", "vou ver"]), 10, "Esta é uma das perguntas mais importantes", True, 6),
    ("vinculos", "Há quanto tempo você trabalha na sua empresa atual?", "[X] anos, com carteira assinada", json.dumps(["anos", "carteira assinada", "estável", "promovido", "carreira"]), json.dumps(["meses", "recente", "informal", "bico"]), 7, "Tempo de trabalho demonstra estabilidade", True, 7),
    ("vinculos", "Seu empregador sabe que você está viajando?", "Sim, tenho férias aprovadas/carta da empresa", json.dumps(["sim", "aprovado", "férias", "carta", "autorizado"]), json.dumps(["não", "não sabe", "pedi demissão"]), 6, None, True, 8),
    ("vinculos", "Você tem filhos? Eles vão viajar com você?", "Sim, tenho [número] filhos que [ficarão no Brasil/virão comigo]", json.dumps(["sim", "estudando", "escola", "ficarão aqui"]), json.dumps(["sozinho", "abandonar"]), 7, None, True, 9),
    ("vinculos", "Quem cuidará dos seus negócios/propriedades enquanto estiver fora?", "[Familiar/sócio/funcionário] ficará responsável", json.dumps(["esposa", "sócio", "família", "gerente", "funcionário"]), json.dumps(["ninguém", "não sei", "vou vender"]), 6, None, True, 10),
]

for pergunta in perguntas_entrevista:
    cursor.execute("""
        INSERT INTO perguntas_entrevista 
        (categoria, pergunta_texto, resposta_ideal, palavras_positivas, palavras_negativas, peso_avaliacao, dica, gratuito, ordem)
        VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s)
    """, pergunta)

conn.commit()
print(f"✅ {len(perguntas_entrevista)} perguntas de Entrevista inseridas!")

# Estatísticas finais
cursor.execute("SELECT COUNT(*) FROM perguntas_ds160")
total_ds160 = cursor.fetchone()[0]

cursor.execute("SELECT COUNT(*) FROM perguntas_entrevista")
total_entrevista = cursor.fetchone()[0]

cursor.execute("SELECT COUNT(*) FROM perguntas_ds160 WHERE gratuito = TRUE")
gratuitas_ds160 = cursor.fetchone()[0]

cursor.execute("SELECT COUNT(*) FROM perguntas_entrevista WHERE gratuito = TRUE")
gratuitas_entrevista = cursor.fetchone()[0]

print("\n" + "="*60)
print("🎉 BANCO POPULADO COM SUCESSO!")
print("="*60)
print(f"📊 Total de perguntas DS-160: {total_ds160}")
print(f"📊 Total de perguntas Entrevista: {total_entrevista}")
print(f"📊 Total geral: {total_ds160 + total_entrevista}")
print(f"🆓 Perguntas gratuitas DS-160: {gratuitas_ds160}")
print(f"🆓 Perguntas gratuitas Entrevista: {gratuitas_entrevista}")
print(f"🆓 Total de perguntas gratuitas: {gratuitas_ds160 + gratuitas_entrevista}")
print("="*60)

cursor.close()
conn.close()