import psycopg2
import os
import json
from dotenv import load_dotenv

load_dotenv()

# Conectar ao PostgreSQL do Railway
DATABASE_URL = os.getenv("DATABASE_URL")

if not DATABASE_URL:
    print("❌ DATABASE_URL não encontrada no .env")
    exit(1)

conn = psycopg2.connect(DATABASE_URL)
cursor = conn.cursor()

print("🔗 Conectado ao PostgreSQL do Railway")

# ==================== PERGUNTAS DS-160 (50 TOTAL) ====================
perguntas_ds160 = [
    # === GRATUITAS (25) ===
    # Pessoal (10 gratuitas)
    {
        "categoria": "pessoal",
        "pergunta_texto": "Qual é o seu nome completo conforme aparece no passaporte?",
        "tipo_resposta": "texto",
        "peso_avaliacao": 5,
        "dica": "Use exatamente como está no passaporte",
        "gratuito": True,
        "ordem": 1
    },
    {
        "categoria": "pessoal",
        "pergunta_texto": "Qual é a sua nacionalidade?",
        "tipo_resposta": "texto",
        "peso_avaliacao": 5,
        "dica": "Brasileiro(a)",
        "gratuito": True,
        "ordem": 2
    },
    {
        "categoria": "pessoal",
        "pergunta_texto": "Qual é a sua data de nascimento?",
        "tipo_resposta": "texto",
        "peso_avaliacao": 5,
        "dica": "Formato: DD/MM/AAAA",
        "gratuito": True,
        "ordem": 3
    },
    {
        "categoria": "pessoal",
        "pergunta_texto": "Qual é o seu estado civil?",
        "tipo_resposta": "multipla",
        "opcoes": ["Solteiro(a)", "Casado(a)", "Divorciado(a)", "Viúvo(a)", "União Estável"],
        "peso_avaliacao": 7,
        "dica": "Estado civil afeta análise de vínculos",
        "gratuito": True,
        "ordem": 4
    },
    {
        "categoria": "pessoal",
        "pergunta_texto": "Qual é o seu nível de escolaridade?",
        "tipo_resposta": "multipla",
        "opcoes": ["Ensino Fundamental", "Ensino Médio", "Superior Incompleto", "Superior Completo", "Pós-Graduação", "Mestrado", "Doutorado"],
        "peso_avaliacao": 6,
        "dica": "Maior escolaridade aumenta pontuação",
        "gratuito": True,
        "ordem": 5
    },
    {
        "categoria": "pessoal",
        "pergunta_texto": "Qual é a sua profissão/ocupação atual?",
        "tipo_resposta": "texto",
        "peso_avaliacao": 8,
        "dica": "Emprego formal aumenta chances",
        "gratuito": True,
        "ordem": 6
    },
    {
        "categoria": "pessoal",
        "pergunta_texto": "Há quanto tempo você trabalha nessa função?",
        "tipo_resposta": "texto",
        "peso_avaliacao": 7,
        "dica": "Estabilidade profissional é importante",
        "gratuito": True,
        "ordem": 7
    },
    {
        "categoria": "pessoal",
        "pergunta_texto": "Você possui dependentes (filhos, cônjuge, pais)?",
        "tipo_resposta": "multipla",
        "opcoes": ["Não", "Sim, 1 dependente", "Sim, 2 dependentes", "Sim, 3 ou mais"],
        "peso_avaliacao": 8,
        "dica": "Dependentes demonstram vínculo com Brasil",
        "gratuito": True,
        "ordem": 8
    },
    {
        "categoria": "pessoal",
        "pergunta_texto": "Você possui imóveis no Brasil?",
        "tipo_resposta": "multipla",
        "opcoes": ["Não", "Sim, 1 imóvel", "Sim, 2 ou mais imóveis"],
        "peso_avaliacao": 9,
        "dica": "Propriedades demonstram raízes no Brasil",
        "gratuito": True,
        "ordem": 9
    },
    {
        "categoria": "pessoal",
        "pergunta_texto": "Você possui veículo próprio?",
        "tipo_resposta": "multipla",
        "opcoes": ["Não", "Sim, 1 veículo", "Sim, 2 ou mais veículos"],
        "peso_avaliacao": 6,
        "dica": "Patrimônio reforça vínculo",
        "gratuito": True,
        "ordem": 10
    },
    
    # Viagem (8 gratuitas)
    {
        "categoria": "viagem",
        "pergunta_texto": "Qual é o principal motivo da sua viagem aos EUA?",
        "tipo_resposta": "multipla",
        "opcoes": ["Turismo", "Negócios", "Estudo", "Visita Familiar", "Tratamento Médico", "Evento/Conferência"],
        "peso_avaliacao": 9,
        "dica": "Seja específico e honesto",
        "gratuito": True,
        "ordem": 11
    },
    {
        "categoria": "viagem",
        "pergunta_texto": "Por quanto tempo você pretende ficar nos EUA?",
        "tipo_resposta": "texto",
        "peso_avaliacao": 7,
        "dica": "Viagens curtas (1-3 semanas) são mais aprovadas",
        "gratuito": True,
        "ordem": 12
    },
    {
        "categoria": "viagem",
        "pergunta_texto": "Quais cidades você pretende visitar?",
        "tipo_resposta": "texto",
        "peso_avaliacao": 6,
        "dica": "Liste cidades específicas e motivos",
        "gratuito": True,
        "ordem": 13
    },
    {
        "categoria": "viagem",
        "pergunta_texto": "Você já tem passagens aéreas compradas?",
        "tipo_resposta": "multipla",
        "opcoes": ["Não", "Sim, ida", "Sim, ida e volta"],
        "peso_avaliacao": 7,
        "dica": "Passagem de volta demonstra intenção de retorno",
        "gratuito": True,
        "ordem": 14
    },
    {
        "categoria": "viagem",
        "pergunta_texto": "Você já reservou hospedagem nos EUA?",
        "tipo_resposta": "multipla",
        "opcoes": ["Não", "Sim, parcialmente", "Sim, toda a estadia"],
        "peso_avaliacao": 6,
        "dica": "Reservas demonstram planejamento",
        "gratuito": True,
        "ordem": 15
    },
    {
        "categoria": "viagem",
        "pergunta_texto": "Você conhece alguém que mora nos EUA?",
        "tipo_resposta": "multipla",
        "opcoes": ["Não", "Sim, familiar", "Sim, amigo", "Sim, familiar e amigos"],
        "peso_avaliacao": 5,
        "dica": "Ser honesto é essencial",
        "gratuito": True,
        "ordem": 16
    },
    {
        "categoria": "viagem",
        "pergunta_texto": "Você planeja trabalhar nos EUA durante sua visita?",
        "tipo_resposta": "multipla",
        "opcoes": ["Não", "Sim"],
        "peso_avaliacao": 10,
        "dica": "SEMPRE responda NÃO para visto de turismo",
        "gratuito": True,
        "ordem": 17
    },
    {
        "categoria": "viagem",
        "pergunta_texto": "Você tem parentes próximos que migraram ilegalmente para os EUA?",
        "tipo_resposta": "multipla",
        "opcoes": ["Não", "Sim"],
        "peso_avaliacao": 9,
        "dica": "Seja honesto - mentir pode causar banimento permanente",
        "gratuito": True,
        "ordem": 18
    },
    
    # Financeiro (7 gratuitas)
    {
        "categoria": "financeiro",
        "pergunta_texto": "Qual é a sua renda mensal aproximada?",
        "tipo_resposta": "multipla",
        "opcoes": ["Até R$ 3.000", "R$ 3.000 - R$ 6.000", "R$ 6.000 - R$ 10.000", "R$ 10.000 - R$ 20.000", "Acima de R$ 20.000"],
        "peso_avaliacao": 8,
        "dica": "Renda compatível com custo da viagem",
        "gratuito": True,
        "ordem": 19
    },
    {
        "categoria": "financeiro",
        "pergunta_texto": "Quem financiará sua viagem?",
        "tipo_resposta": "multipla",
        "opcoes": ["Eu mesmo", "Cônjuge", "Pais", "Empresa", "Outro"],
        "peso_avaliacao": 7,
        "dica": "Recursos próprios são mais valorizados",
        "gratuito": True,
        "ordem": 20
    },
    {
        "categoria": "financeiro",
        "pergunta_texto": "Quanto você estima gastar durante a viagem?",
        "tipo_resposta": "texto",
        "peso_avaliacao": 6,
        "dica": "Seja realista com custos (passagem, hotel, alimentação)",
        "gratuito": True,
        "ordem": 21
    },
    {
        "categoria": "financeiro",
        "pergunta_texto": "Você possui poupança ou investimentos?",
        "tipo_resposta": "multipla",
        "opcoes": ["Não", "Sim, até R$ 10 mil", "Sim, R$ 10-50 mil", "Sim, acima de R$ 50 mil"],
        "peso_avaliacao": 8,
        "dica": "Reserva financeira demonstra estabilidade",
        "gratuito": True,
        "ordem": 22
    },
    {
        "categoria": "financeiro",
        "pergunta_texto": "Você possui cartão de crédito internacional?",
        "tipo_resposta": "multipla",
        "opcoes": ["Não", "Sim"],
        "peso_avaliacao": 5,
        "dica": "Facilita pagamentos nos EUA",
        "gratuito": True,
        "ordem": 23
    },
    {
        "categoria": "financeiro",
        "pergunta_texto": "Você declara Imposto de Renda?",
        "tipo_resposta": "multipla",
        "opcoes": ["Não", "Sim"],
        "peso_avaliacao": 7,
        "dica": "Declaração de IR comprova renda",
        "gratuito": True,
        "ordem": 24
    },
    {
        "categoria": "financeiro",
        "pergunta_texto": "Você possui dívidas ou empréstimos ativos?",
        "tipo_resposta": "multipla",
        "opcoes": ["Não", "Sim, pequenas dívidas", "Sim, dívidas significativas"],
        "peso_avaliacao": 6,
        "dica": "Muitas dívidas podem ser vistas como risco",
        "gratuito": True,
        "ordem": 25
    },
    
    # === PREMIUM (25) ===
    # Histórico de Viagens (10 premium)
    {
        "categoria": "historico_viagens",
        "pergunta_texto": "Quantos países você já visitou?",
        "tipo_resposta": "multipla",
        "opcoes": ["Nenhum", "1-3 países", "4-7 países", "8 ou mais países"],
        "peso_avaliacao": 8,
        "dica": "Histórico de viagens internacionais aumenta credibilidade",
        "gratuito": False,
        "ordem": 26
    },
    {
        "categoria": "historico_viagens",
        "pergunta_texto": "Você já visitou países da Europa?",
        "tipo_resposta": "multipla",
        "opcoes": ["Não", "Sim, 1 vez", "Sim, 2-3 vezes", "Sim, mais de 3 vezes"],
        "peso_avaliacao": 7,
        "dica": "Vistos europeus demonstram confiabilidade",
        "gratuito": False,
        "ordem": 27
    },
    {
        "categoria": "historico_viagens",
        "pergunta_texto": "Você já visitou Canadá ou México?",
        "tipo_resposta": "multipla",
        "opcoes": ["Não", "Sim, Canadá", "Sim, México", "Sim, ambos"],
        "peso_avaliacao": 7,
        "dica": "Países vizinhos aos EUA contam positivamente",
        "gratuito": False,
        "ordem": 28
    },
    {
        "categoria": "historico_viagens",
        "pergunta_texto": "Você já teve algum visto negado?",
        "tipo_resposta": "multipla",
        "opcoes": ["Não", "Sim, EUA", "Sim, outro país", "Sim, múltiplos países"],
        "peso_avaliacao": 10,
        "dica": "Negação anterior requer explicação detalhada",
        "gratuito": False,
        "ordem": 29
    },
    {
        "categoria": "historico_viagens",
        "pergunta_texto": "Se teve visto negado, há quanto tempo foi?",
        "tipo_resposta": "texto",
        "peso_avaliacao": 8,
        "dica": "Tempo ajuda - situação pode ter mudado",
        "gratuito": False,
        "ordem": 30
    },
    {
        "categoria": "historico_viagens",
        "pergunta_texto": "Você já overstayed (ficou além do permitido) em algum país?",
        "tipo_resposta": "multipla",
        "opcoes": ["Não", "Sim"],
        "peso_avaliacao": 10,
        "dica": "Overstay é muito negativo - seja honesto",
        "gratuito": False,
        "ordem": 31
    },
    {
        "categoria": "historico_viagens",
        "pergunta_texto": "Você possui vistos válidos para outros países atualmente?",
        "tipo_resposta": "texto",
        "peso_avaliacao": 6,
        "dica": "Vistos válidos demonstram credibilidade",
        "gratuito": False,
        "ordem": 32
    },
    {
        "categoria": "historico_viagens",
        "pergunta_texto": "Qual foi o último país internacional que você visitou?",
        "tipo_resposta": "texto",
        "peso_avaliacao": 5,
        "dica": "Viagens recentes demonstram capacidade financeira",
        "gratuito": False,
        "ordem": 33
    },
    {
        "categoria": "historico_viagens",
        "pergunta_texto": "Você viaja a trabalho ou turismo normalmente?",
        "tipo_resposta": "multipla",
        "opcoes": ["Não viajo", "Turismo", "Trabalho", "Ambos"],
        "peso_avaliacao": 6,
        "dica": "Viagens a trabalho são vistas positivamente",
        "gratuito": False,
        "ordem": 34
    },
    {
        "categoria": "historico_viagens",
        "pergunta_texto": "Você já participou de programas de intercâmbio?",
        "tipo_resposta": "multipla",
        "opcoes": ["Não", "Sim, intercâmbio escolar", "Sim, intercâmbio universitário", "Sim, trabalho"],
        "peso_avaliacao": 7,
        "dica": "Intercâmbios demonstram experiência internacional",
        "gratuito": False,
        "ordem": 35
    },
    
    # Vínculos Brasil (8 premium)
    {
        "categoria": "vinculos",
        "pergunta_texto": "Seus pais moram no Brasil?",
        "tipo_resposta": "multipla",
        "opcoes": ["Sim, ambos", "Sim, um deles", "Não, nenhum"],
        "peso_avaliacao": 8,
        "dica": "Família no Brasil é forte vínculo",
        "gratuito": False,
        "ordem": 36
    },
    {
        "categoria": "vinculos",
        "pergunta_texto": "Você possui irmãos que moram no Brasil?",
        "tipo_resposta": "multipla",
        "opcoes": ["Sim", "Não", "Não tenho irmãos"],
        "peso_avaliacao": 6,
        "dica": "Laços familiares importam",
        "gratuito": False,
        "ordem": 37
    },
    {
        "categoria": "vinculos",
        "pergunta_texto": "Há quanto tempo você mora no seu endereço atual?",
        "tipo_resposta": "multipla",
        "opcoes": ["Menos de 1 ano", "1-3 anos", "3-5 anos", "Mais de 5 anos"],
        "peso_avaliacao": 7,
        "dica": "Estabilidade residencial é importante",
        "gratuito": False,
        "ordem": 38
    },
    {
        "categoria": "vinculos",
        "pergunta_texto": "Você possui negócio próprio no Brasil?",
        "tipo_resposta": "multipla",
        "opcoes": ["Não", "Sim, microempresa", "Sim, pequena empresa", "Sim, média/grande empresa"],
        "peso_avaliacao": 9,
        "dica": "Negócio próprio é forte vínculo",
        "gratuito": False,
        "ordem": 39
    },
    {
        "categoria": "vinculos",
        "pergunta_texto": "Você participa de organizações sociais, clubes ou associações?",
        "tipo_resposta": "multipla",
        "opcoes": ["Não", "Sim, 1 organização", "Sim, 2 ou mais"],
        "peso_avaliacao": 5,
        "dica": "Envolvimento comunitário demonstra raízes",
        "gratuito": False,
        "ordem": 40
    },
    {
        "categoria": "vinculos",
        "pergunta_texto": "Você possui pets no Brasil?",
        "tipo_resposta": "multipla",
        "opcoes": ["Não", "Sim"],
        "peso_avaliacao": 3,
        "dica": "Pequeno detalhe mas pode contar",
        "gratuito": False,
        "ordem": 41
    },
    {
        "categoria": "vinculos",
        "pergunta_texto": "Você está matriculado em algum curso no Brasil?",
        "tipo_resposta": "multipla",
        "opcoes": ["Não", "Sim, curso técnico", "Sim, graduação", "Sim, pós-graduação"],
        "peso_avaliacao": 7,
        "dica": "Estudos em andamento são vínculo forte",
        "gratuito": False,
        "ordem": 42
    },
    {
        "categoria": "vinculos",
        "pergunta_texto": "Você planeja retornar ao mesmo emprego após a viagem?",
        "tipo_resposta": "multipla",
        "opcoes": ["Sim", "Não", "Não estou empregado"],
        "peso_avaliacao": 8,
        "dica": "Retorno ao emprego é essencial",
        "gratuito": False,
        "ordem": 43
    },
    
    # Perfil Adicional (7 premium)
    {
        "categoria": "pessoal",
        "pergunta_texto": "Você possui seguro viagem internacional?",
        "tipo_resposta": "multipla",
        "opcoes": ["Não", "Sim, básico", "Sim, completo"],
        "peso_avaliacao": 5,
        "dica": "Seguro demonstra responsabilidade",
        "gratuito": False,
        "ordem": 44
    },
    {
        "categoria": "pessoal",
        "pergunta_texto": "Você fala inglês?",
        "tipo_resposta": "multipla",
        "opcoes": ["Não", "Básico", "Intermediário", "Avançado", "Fluente"],
        "peso_avaliacao": 6,
        "dica": "Inglês facilita mas não é obrigatório",
        "gratuito": False,
        "ordem": 45
    },
    {
        "categoria": "pessoal",
        "pergunta_texto": "Você já foi preso ou condenado por algum crime?",
        "tipo_resposta": "multipla",
        "opcoes": ["Não", "Sim"],
        "peso_avaliacao": 10,
        "dica": "Antecedentes criminais são verificados",
        "gratuito": False,
        "ordem": 46
    },
    {
        "categoria": "pessoal",
        "pergunta_texto": "Você possui alguma condição médica que requer tratamento contínuo?",
        "tipo_resposta": "multipla",
        "opcoes": ["Não", "Sim"],
        "peso_avaliacao": 4,
        "dica": "Pode requerer documentação adicional",
        "gratuito": False,
        "ordem": 47
    },
    {
        "categoria": "pessoal",
        "pergunta_texto": "Você já serviu nas forças armadas?",
        "tipo_resposta": "multipla",
        "opcoes": ["Não", "Sim"],
        "peso_avaliacao": 3,
        "dica": "Informação necessária no DS-160",
        "gratuito": False,
        "ordem": 48
    },
    {
        "categoria": "pessoal",
        "pergunta_texto": "Você possui tatuagens visíveis?",
        "tipo_resposta": "multipla",
        "opcoes": ["Não", "Sim"],
        "peso_avaliacao": 2,
        "dica": "Pode ser perguntado na entrevista",
        "gratuito": False,
        "ordem": 49
    },
    {
        "categoria": "pessoal",
        "pergunta_texto": "Você se sente preparado para a entrevista do visto?",
        "tipo_resposta": "multipla",
        "opcoes": ["Não", "Um pouco", "Sim", "Muito preparado"],
        "peso_avaliacao": 5,
        "dica": "Confiança é importante mas sem arrogância",
        "gratuito": False,
        "ordem": 50
    }
]

# ==================== PERGUNTAS ENTREVISTA (40 TOTAL) ====================
perguntas_entrevista = [
    # === GRATUITAS (15) ===
    {
        "categoria": "pessoal",
        "pergunta_texto": "Por que você quer ir para os Estados Unidos?",
        "palavras_positivas": ["turismo", "conhecer", "férias", "visitar", "passeio", "cultura"],
        "palavras_negativas": ["trabalhar", "morar", "ficar", "imigrar", "permanente"],
        "peso_avaliacao": 10,
        "dica": "Seja direto e específico sobre turismo",
        "gratuito": True,
        "ordem": 1
    },
    {
        "categoria": "pessoal",
        "pergunta_texto": "O que você faz profissionalmente?",
        "palavras_positivas": ["trabalho", "empresa", "cargo", "anos", "estável"],
        "palavras_negativas": ["desempregado", "bico", "autônomo sem registro"],
        "peso_avaliacao": 9,
        "dica": "Destaque estabilidade e vínculo empregatício",
        "gratuito": True,
        "ordem": 2
    },
    {
        "categoria": "pessoal",
        "pergunta_texto": "Você é casado(a)? Tem filhos?",
        "palavras_positivas": ["casado", "esposa", "marido", "filhos", "família"],
        "palavras_negativas": ["separado", "sozinho"],
        "peso_avaliacao": 8,
        "dica": "Família é forte vínculo com Brasil",
        "gratuito": True,
        "ordem": 3
    },
    {
        "categoria": "viagem",
        "pergunta_texto": "Quanto tempo pretende ficar nos EUA?",
        "palavras_positivas": ["semanas", "dias", "curto", "15 dias", "10 dias"],
        "palavras_negativas": ["meses", "indefinido", "depende", "bastante tempo"],
        "peso_avaliacao": 9,
        "dica": "Viagens curtas (1-3 semanas) são ideais",
        "gratuito": True,
        "ordem": 4
    },
    {
        "categoria": "viagem",
        "pergunta_texto": "Quais cidades você vai visitar?",
        "palavras_positivas": ["Nova York", "Miami", "Orlando", "Los Angeles", "roteiro"],
        "palavras_negativas": ["não sei", "depende", "vou decidir lá"],
        "peso_avaliacao": 7,
        "dica": "Tenha um roteiro específico preparado",
        "gratuito": True,
        "ordem": 5
    },
    {
        "categoria": "viagem",
        "pergunta_texto": "Onde você vai ficar hospedado?",
        "palavras_positivas": ["hotel", "airbnb", "reserva", "endereço"],
        "palavras_negativas": ["casa de parente", "amigo", "não sei ainda"],
        "peso_avaliacao": 7,
        "dica": "Hospedagem em hotel/Airbnb é melhor que casa de parentes",
        "gratuito": True,
        "ordem": 6
    },
    {
        "categoria": "financeiro",
        "pergunta_texto": "Quem vai pagar pela sua viagem?",
        "palavras_positivas": ["eu", "próprio", "salário", "poupança", "economia"],
        "palavras_negativas": ["empréstimo", "não sei", "alguém vai pagar"],
        "peso_avaliacao": 9,
        "dica": "Recursos próprios são fundamentais",
        "gratuito": True,
        "ordem": 7
    },
    {
        "categoria": "financeiro",
        "pergunta_texto": "Quanto você ganha por mês?",
        "palavras_positivas": ["R$", "salário", "renda", "compatível"],
        "palavras_negativas": ["pouco", "não tenho renda fixa", "varia muito"],
        "peso_avaliacao": 8,
        "dica": "Seja honesto e tenha como comprovar",
        "gratuito": True,
        "ordem": 8
    },
    {
        "categoria": "vinculos",
        "pergunta_texto": "Por que você vai voltar para o Brasil?",
        "palavras_positivas": ["trabalho", "família", "casa", "negócio", "estudos", "vida"],
        "palavras_negativas": ["não sei", "se der certo volto", "depende"],
        "peso_avaliacao": 10,
        "dica": "CRUCIAL - liste múltiplos motivos fortes",
        "gratuito": True,
        "ordem": 9
    },
    {
        "categoria": "vinculos",
        "pergunta_texto": "Você tem parentes ou amigos nos Estados Unidos?",
        "palavras_positivas": ["não", "sim mas vou ficar em hotel"],
        "palavras_negativas": ["sim e vou ficar com eles", "vários parentes"],
        "peso_avaliacao": 7,
        "dica": "Muitos parentes nos EUA pode ser visto como risco",
        "gratuito": True,
        "ordem": 10
    },
    {
        "categoria": "historico_viagens",
        "pergunta_texto": "Você já viajou para fora do Brasil?",
        "palavras_positivas": ["sim", "Europa", "América do Sul", "vários países"],
        "palavras_negativas": ["não", "nunca", "primeira viagem"],
        "peso_avaliacao": 8,
        "dica": "Histórico de viagens aumenta credibilidade",
        "gratuito": True,
        "ordem": 11
    },
    {
        "categoria": "historico_viagens",
        "pergunta_texto": "Você já teve visto americano antes?",
        "palavras_positivas": ["sim", "visitei", "respeitei prazo", "voltei"],
        "palavras_negativas": ["não", "foi negado"],
        "peso_avaliacao": 9,
        "dica": "Visto anterior aprovado ajuda muito",
        "gratuito": True,
        "ordem": 12
    },
    {
        "categoria": "viagem",
        "pergunta_texto": "Você conhece alguém que pode te hospedar nos EUA?",
        "palavras_positivas": ["não", "vou ficar em hotel"],
        "palavras_negativas": ["sim", "familiar", "amigo", "vou ficar na casa"],
        "peso_avaliacao": 6,
        "dica": "Hotel é sempre melhor que casa de conhecidos",
        "gratuito": True,
        "ordem": 13
    },
    {
        "categoria": "pessoal",
        "pergunta_texto": "Você estuda? Onde?",
        "palavras_positivas": ["sim", "universidade", "faculdade", "curso"],
        "palavras_negativas": ["parei", "tranquei", "não estudo"],
        "peso_avaliacao": 7,
        "dica": "Estudos em andamento são vínculo forte",
        "gratuito": True,
        "ordem": 14
    },
    {
        "categoria": "viagem",
        "pergunta_texto": "Você tem seguro viagem?",
        "palavras_positivas": ["sim", "contratei", "vou contratar"],
        "palavras_negativas": ["não", "não precisa", "não vou fazer"],
        "peso_avaliacao": 5,
        "dica": "Seguro demonstra responsabilidade",
        "gratuito": True,
        "ordem": 15
    },
    
    # === PREMIUM (25) ===
    {
        "categoria": "pessoal",
        "pergunta_texto": "Há quanto tempo você trabalha na empresa atual?",
        "palavras_positivas": ["anos", "estável", "desde", "tempo"],
        "palavras_negativas": ["recente", "comecei agora", "poucos meses"],
        "peso_avaliacao": 8,
        "dica": "Estabilidade profissional é importante",
        "gratuito": False,
        "ordem": 16
    },
    {
        "categoria": "financeiro",
        "pergunta_texto": "Você possui investimentos ou poupança?",
        "palavras_positivas": ["sim", "poupança", "investimentos", "reserva"],
        "palavras_negativas": ["não", "nada guardado"],
        "peso_avaliacao": 7,
        "dica": "Reserva financeira é positiva",
        "gratuito": False,
        "ordem": 17
    },
    {
        "categoria": "vinculos",
        "pergunta_texto": "Você possui imóveis no Brasil?",
        "palavras_positivas": ["sim", "casa própria", "apartamento", "propriedade"],
        "palavras_negativas": ["não", "aluguel", "moro com pais"],
        "peso_avaliacao": 9,
        "dica": "Propriedades são forte vínculo",
        "gratuito": False,
        "ordem": 18
    },
    {
        "categoria": "vinculos",
        "pergunta_texto": "Seus pais moram no Brasil?",
        "palavras_positivas": ["sim", "ambos", "família toda"],
        "palavras_negativas": ["não", "moram fora", "moram nos EUA"],
        "peso_avaliacao": 8,
        "dica": "Família no Brasil é vínculo forte",
        "gratuito": False,
        "ordem": 19
    },
    {
        "categoria": "viagem",
        "pergunta_texto": "Quem vai viajar com você?",
        "palavras_positivas": ["família", "cônjuge", "grupo", "amigos"],
        "palavras_negativas": ["sozinho", "ninguém"],
        "peso_avaliacao": 6,
        "dica": "Viajar em grupo pode ser positivo",
        "gratuito": False,
        "ordem": 20
    },
    {
        "categoria": "viagem",
        "pergunta_texto": "Já comprou as passagens aéreas?",
        "palavras_positivas": ["sim", "ida e volta", "confirmadas"],
        "palavras_negativas": ["não", "só ida", "vou comprar depois"],
        "peso_avaliacao": 7,
        "dica": "Passagem de volta demonstra intenção de retorno",
        "gratuito": False,
        "ordem": 21
    },
    {
        "categoria": "financeiro",
        "pergunta_texto": "Quanto você planeja gastar na viagem?",
        "palavras_positivas": ["orçamento", "planejado", "calculei", "US$"],
        "palavras_negativas": ["não sei", "vou gastando", "depende"],
        "peso_avaliacao": 6,
        "dica": "Tenha orçamento detalhado preparado",
        "gratuito": False,
        "ordem": 22
    },
    {
        "categoria": "historico_viagens",
        "pergunta_texto": "Quais países você já visitou?",
        "palavras_positivas": ["Europa", "Ásia", "vários", "países desenvolvidos"],
        "palavras_negativas": ["nenhum", "só América do Sul"],
        "peso_avaliacao": 7,
        "dica": "Liste todos os países visitados",
        "gratuito": False,
        "ordem": 23
    },
    {
        "categoria": "historico_viagens",
        "pergunta_texto": "Você sempre voltou no prazo das suas viagens internacionais?",
        "palavras_positivas": ["sim", "sempre", "respeitei prazos"],
        "palavras_negativas": ["não", "fiquei mais tempo", "overstay"],
        "peso_avaliacao": 10,
        "dica": "CRÍTICO - overstay é muito negativo",
        "gratuito": False,
        "ordem": 24
    },
    {
        "categoria": "pessoal",
        "pergunta_texto": "Você fala inglês?",
        "palavras_positivas": ["sim", "fluente", "intermediário", "consigo comunicar"],
        "palavras_negativas": ["não", "nada", "muito pouco"],
        "peso_avaliacao": 5,
        "dica": "Inglês ajuda mas não é obrigatório",
        "gratuito": False,
        "ordem": 25
    },
    {
        "categoria": "viagem",
        "pergunta_texto": "Por que escolheu esses destinos específicos nos EUA?",
        "palavras_positivas": ["pontos turísticos", "cultura", "história", "sempre quis conhecer"],
        "palavras_negativas": ["não sei", "qualquer lugar", "onde tiver trabalho"],
        "peso_avaliacao": 6,
        "dica": "Demonstre interesse genuíno em turismo",
        "gratuito": False,
        "ordem": 26
    },
    {
        "categoria": "viagem",
        "pergunta_texto": "Você tem planos de trabalhar nos EUA?",
        "palavras_positivas": ["não", "jamais", "apenas turismo", "férias"],
        "palavras_negativas": ["sim", "se surgir oportunidade", "talvez"],
        "peso_avaliacao": 10,
        "dica": "SEMPRE diga NÃO para visto de turismo",
        "gratuito": False,
        "ordem": 27
    },
    {
        "categoria": "vinculos",
        "pergunta_texto": "O que você mais gosta no seu trabalho atual?",
        "palavras_positivas": ["carreira", "desafios", "equipe", "crescimento", "satisfeito"],
        "palavras_negativas": ["nada", "só pelo salário", "quero sair"],
        "peso_avaliacao": 7,
        "dica": "Demonstre satisfação profissional",
        "gratuito": False,
        "ordem": 28
    },
    {
        "categoria": "financeiro",
        "pergunta_texto": "Você possui dívidas?",
        "palavras_positivas": ["não", "quitei", "em dia", "controladas"],
        "palavras_negativas": ["sim", "muitas", "atrasadas", "negativado"],
        "peso_avaliacao": 6,
        "dica": "Dívidas podem ser vistas como risco",
        "gratuito": False,
        "ordem": 29
    },
    {
        "categoria": "pessoal",
        "pergunta_texto": "Você já foi preso ou teve problemas com a lei?",
        "palavras_positivas": ["não", "nunca", "ficha limpa"],
        "palavras_negativas": ["sim", "processo", "condenação"],
        "peso_avaliacao": 10,
        "dica": "Antecedentes criminais são verificados",
        "gratuito": False,
        "ordem": 30
    },
    {
        "categoria": "vinculos",
        "pergunta_texto": "Você pretende voltar ao mesmo emprego após a viagem?",
        "palavras_positivas": ["sim", "com certeza", "tirei férias", "já combinei"],
        "palavras_negativas": ["não", "vou pedir demissão", "não sei"],
        "peso_avaliacao": 9,
        "dica": "Retorno ao emprego é essencial",
        "gratuito": False,
        "ordem": 31
    },
    {
        "categoria": "viagem",
        "pergunta_texto": "Você já pesquisou sobre os lugares que vai visitar?",
        "palavras_positivas": ["sim", "bastante", "li sobre", "assisti vídeos", "planejei"],
        "palavras_negativas": ["não", "vou ver lá", "não pesquisei"],
        "peso_avaliacao": 5,
        "dica": "Planejamento demonstra seriedade",
        "gratuito": False,
        "ordem": 32
    },
    {
        "categoria": "historico_viagens",
        "pergunta_texto": "Se já teve visto negado, o que mudou desde então?",
        "palavras_positivas": ["emprego melhor", "situação financeira", "vínculos mais fortes", "comprovantes"],
        "palavras_negativas": ["nada", "mesma situação"],
        "peso_avaliacao": 9,
        "dica": "Mostre mudanças significativas",
        "gratuito": False,
        "ordem": 33
    },
    {
        "categoria": "pessoal",
        "pergunta_texto": "Você possui outras fontes de renda além do salário?",
        "palavras_positivas": ["sim", "aluguel", "investimentos", "renda extra"],
        "palavras_negativas": ["não", "só salário"],
        "peso_avaliacao": 6,
        "dica": "Múltiplas fontes demonstram estabilidade",
        "gratuito": False,
        "ordem": 34
    },
    {
        "categoria": "vinculos",
        "pergunta_texto": "Você possui negócio próprio no Brasil?",
        "palavras_positivas": ["sim", "empresa", "sócio", "CNPJ"],
        "palavras_negativas": ["não", "informal"],
        "peso_avaliacao": 8,
        "dica": "Negócio próprio é vínculo muito forte",
        "gratuito": False,
        "ordem": 35
    },
    {
        "categoria": "viagem",
        "pergunta_texto": "Você está levando quanto dinheiro?",
        "palavras_positivas": ["suficiente", "planejado", "cartão", "dólares"],
        "palavras_negativas": ["pouco", "não sei", "vou ver lá"],
        "peso_avaliacao": 6,
        "dica": "Demonstre planejamento financeiro",
        "gratuito": False,
        "ordem": 36
    },
    {
        "categoria": "pessoal",
        "pergunta_texto": "Qual é o seu nível de escolaridade?",
        "palavras_positivas": ["superior", "pós-graduação", "mestrado", "formado"],
        "palavras_negativas": ["fundamental", "incompleto"],
        "peso_avaliacao": 6,
        "dica": "Maior escolaridade é vista positivamente",
        "gratuito": False,
        "ordem": 37
    },
    {
        "categoria": "vinculos",
        "pergunta_texto": "Você está matriculado em algum curso?",
        "palavras_positivas": ["sim", "faculdade", "curso técnico", "semestre"],
        "palavras_negativas": ["não", "tranquei", "larguei"],
        "peso_avaliacao": 7,
        "dica": "Estudos em andamento são vínculo",
        "gratuito": False,
        "ordem": 38
    },
    {
        "categoria": "viagem",
        "pergunta_texto": "Como você ficou sabendo sobre os EUA?",
        "palavras_positivas": ["sempre quis conhecer", "sonho", "pesquisei", "cultura"],
        "palavras_negativas": ["amigos falaram", "para ganhar dinheiro"],
        "peso_avaliacao": 4,
        "dica": "Demonstre interesse genuíno em turismo",
        "gratuito": False,
        "ordem": 39
    },
    {
        "categoria": "pessoal",
        "pergunta_texto": "Você se sente preparado para essa entrevista?",
        "palavras_positivas": ["sim", "estudei", "preparado", "confiante"],
        "palavras_negativas": ["não", "nervoso", "inseguro"],
        "peso_avaliacao": 5,
        "dica": "Confiança é importante, mas sem arrogância",
        "gratuito": False,
        "ordem": 40
    }
]

# ==================== INSERIR NO BANCO ====================
# Limpar perguntas antigas antes de inserir novas
print("🧹 Limpando perguntas antigas...")
cursor.execute("DELETE FROM perguntas_ds160")
cursor.execute("DELETE FROM perguntas_entrevista")
conn.commit()
print("✅ Perguntas antigas removidas!")

print("\n📝 Inserindo perguntas DS-160...")
for p in perguntas_ds160:
    cursor.execute("""
        INSERT INTO perguntas_ds160 (
            categoria, pergunta_texto, tipo_resposta, opcoes,
            peso_avaliacao, dica, gratuito, ordem
        ) VALUES (%s, %s, %s, %s, %s, %s, %s, %s)
    """, (
        p["categoria"],
        p["pergunta_texto"],
        p.get("tipo_resposta", "texto"),
        json.dumps(p.get("opcoes")) if p.get("opcoes") else None,
        p["peso_avaliacao"],
        p.get("dica"),
        p["gratuito"],
        p["ordem"]
    ))

conn.commit()
print(f"✅ {len(perguntas_ds160)} perguntas DS-160 inseridas!")

print("\n📝 Inserindo perguntas de Entrevista...")
for p in perguntas_entrevista:
    cursor.execute("""
        INSERT INTO perguntas_entrevista (
            categoria, pergunta_texto, palavras_positivas, palavras_negativas,
            peso_avaliacao, dica, gratuito, ordem
        ) VALUES (%s, %s, %s, %s, %s, %s, %s, %s)
    """, (
        p["categoria"],
        p["pergunta_texto"],
        json.dumps(p.get("palavras_positivas")) if p.get("palavras_positivas") else None,
        json.dumps(p.get("palavras_negativas")) if p.get("palavras_negativas") else None,
        p["peso_avaliacao"],
        p.get("dica"),
        p["gratuito"],
        p["ordem"]
    ))

conn.commit()
print(f"✅ {len(perguntas_entrevista)} perguntas de Entrevista inseridas!")

# Verificar total
cursor.execute("SELECT COUNT(*) FROM perguntas_ds160")
total_ds160 = cursor.fetchone()[0]

cursor.execute("SELECT COUNT(*) FROM perguntas_entrevista")
total_entrevista = cursor.fetchone()[0]

cursor.close()
conn.close()

print("\n" + "="*60)
print("🎉 BANCO POPULADO COM SUCESSO!")
print("="*60)
print(f"📊 DS-160: {total_ds160} perguntas")
print(f"📊 Entrevista: {total_entrevista} perguntas")
print(f"📊 TOTAL: {total_ds160 + total_entrevista} perguntas")
print("="*60)