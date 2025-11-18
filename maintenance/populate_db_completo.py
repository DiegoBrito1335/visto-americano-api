"""
Script completo com 50 perguntas DS-160 + 40 perguntas de entrevista
Baseado em experiências reais de brasileiros na embaixada americana
"""

from sqlalchemy.orm import Session
from app.database import SessionLocal, engine, Base
from app.models import PerguntaDS160, PerguntaEntrevista

Base.metadata.create_all(bind=engine)

def popular_perguntas_ds160_completo(db: Session):
    """Perguntas DS-160 completas - baseadas no formulário oficial"""
    
    perguntas = [
        # ==================== CATEGORIA: PESSOAL (10) ====================
        {
            "categoria": "pessoal",
            "pergunta_texto": "Qual é o seu nome completo como aparece no passaporte?",
            "tipo_resposta": "texto",
            "peso_avaliacao": 3,
            "dica": "Digite exatamente como está escrito no passaporte, incluindo sobrenomes",
            "gratuito": True,
            "ordem": 1
        },
        {
            "categoria": "pessoal",
            "pergunta_texto": "Você já usou outros nomes (nome de solteira, apelido oficial)?",
            "tipo_resposta": "sim_nao",
            "peso_avaliacao": 2,
            "dica": "Seja honesto. Mudanças de nome legais devem ser informadas",
            "gratuito": True,
            "ordem": 2
        },
        {
            "categoria": "pessoal",
            "pergunta_texto": "Qual é o seu sexo?",
            "tipo_resposta": "multipla_escolha",
            "opcoes": ["Masculino", "Feminino"],
            "peso_avaliacao": 1,
            "dica": "Conforme documento oficial",
            "gratuito": True,
            "ordem": 3
        },
        {
            "categoria": "pessoal",
            "pergunta_texto": "Qual é o seu estado civil?",
            "tipo_resposta": "multipla_escolha",
            "opcoes": ["Solteiro(a)", "Casado(a)", "Divorciado(a)", "Viúvo(a)", "União Estável"],
            "peso_avaliacao": 7,
            "dica": "Casados e com família têm vínculos mais fortes com o Brasil",
            "gratuito": True,
            "ordem": 4
        },
        {
            "categoria": "pessoal",
            "pergunta_texto": "Qual é a sua data de nascimento?",
            "tipo_resposta": "texto",
            "peso_avaliacao": 2,
            "dica": "Formato: DD/MM/AAAA",
            "gratuito": True,
            "ordem": 5
        },
        {
            "categoria": "pessoal",
            "pergunta_texto": "Você tem filhos?",
            "tipo_resposta": "sim_nao",
            "peso_avaliacao": 8,
            "dica": "Filhos menores no Brasil são um dos vínculos mais fortes",
            "gratuito": False,
            "ordem": 6
        },
        {
            "categoria": "pessoal",
            "pergunta_texto": "Qual é o seu CPF?",
            "tipo_resposta": "texto",
            "peso_avaliacao": 3,
            "dica": "Necessário para comprovação de vínculos fiscais",
            "gratuito": False,
            "ordem": 7
        },
        {
            "categoria": "pessoal",
            "pergunta_texto": "Você possui alguma deficiência física ou mental?",
            "tipo_resposta": "sim_nao",
            "peso_avaliacao": 1,
            "dica": "Não afeta aprovação, mas pode necessitar documentação adicional",
            "gratuito": False,
            "ordem": 8
        },
        {
            "categoria": "pessoal",
            "pergunta_texto": "Qual é o seu nível de escolaridade?",
            "tipo_resposta": "multipla_escolha",
            "opcoes": ["Fundamental", "Médio", "Superior Incompleto", "Superior Completo", "Pós-graduação"],
            "peso_avaliacao": 4,
            "dica": "Maior escolaridade pode indicar melhores vínculos profissionais",
            "gratuito": False,
            "ordem": 9
        },
        {
            "categoria": "pessoal",
            "pergunta_texto": "Você fala inglês?",
            "tipo_resposta": "multipla_escolha",
            "opcoes": ["Não falo", "Básico", "Intermediário", "Avançado", "Fluente"],
            "peso_avaliacao": 3,
            "dica": "Não é obrigatório, mas facilita a entrevista",
            "gratuito": False,
            "ordem": 10
        },
        
        # ==================== CATEGORIA: VIAGEM (10) ====================
        {
            "categoria": "viagem",
            "pergunta_texto": "Qual é o propósito principal da sua viagem aos Estados Unidos?",
            "tipo_resposta": "multipla_escolha",
            "opcoes": ["Turismo", "Negócios", "Visitar familiares/amigos", "Estudos", "Tratamento médico", "Trânsito"],
            "peso_avaliacao": 10,
            "dica": "Turismo é o motivo mais comum e aceito para visto B1/B2",
            "gratuito": True,
            "ordem": 11
        },
        {
            "categoria": "viagem",
            "pergunta_texto": "Quanto tempo você pretende ficar nos Estados Unidos?",
            "tipo_resposta": "texto",
            "peso_avaliacao": 9,
            "dica": "Viagens de 1-3 semanas são ideais. Acima de 90 dias pode levantar suspeitas",
            "gratuito": True,
            "ordem": 12
        },
        {
            "categoria": "viagem",
            "pergunta_texto": "Você já comprou as passagens aéreas?",
            "tipo_resposta": "sim_nao",
            "peso_avaliacao": 4,
            "dica": "NÃO compre antes da aprovação! Mas ter roteiro planejado ajuda",
            "gratuito": True,
            "ordem": 13
        },
        {
            "categoria": "viagem",
            "pergunta_texto": "Quais cidades/estados você pretende visitar?",
            "tipo_resposta": "texto",
            "peso_avaliacao": 6,
            "dica": "Tenha um roteiro específico. Ex: Orlando (Disney), Miami (praias)",
            "gratuito": True,
            "ordem": 14
        },
        {
            "categoria": "viagem",
            "pergunta_texto": "Onde você vai se hospedar nos EUA?",
            "tipo_resposta": "multipla_escolha",
            "opcoes": ["Hotel", "Casa de amigos/família", "Airbnb", "Ainda não decidi"],
            "peso_avaliacao": 5,
            "dica": "Ter reservas ou endereço de hospedagem demonstra planejamento",
            "gratuito": False,
            "ordem": 15
        },
        {
            "categoria": "viagem",
            "pergunta_texto": "Esta é uma viagem de grupo ou individual?",
            "tipo_resposta": "multipla_escolha",
            "opcoes": ["Individual", "Com família", "Com amigos", "Grupo organizado"],
            "peso_avaliacao": 6,
            "dica": "Viagens em família têm mais chances de aprovação",
            "gratuito": False,
            "ordem": 16
        },
        {
            "categoria": "viagem",
            "pergunta_texto": "Você já visitou os Estados Unidos antes?",
            "tipo_resposta": "sim_nao",
            "peso_avaliacao": 7,
            "dica": "Ter visitado e retornado anteriormente é muito positivo",
            "gratuito": False,
            "ordem": 17
        },
        {
            "categoria": "viagem",
            "pergunta_texto": "Você já visitou outros países?",
            "tipo_resposta": "sim_nao",
            "peso_avaliacao": 8,
            "dica": "Histórico de viagens internacionais com retorno é excelente",
            "gratuito": False,
            "ordem": 18
        },
        {
            "categoria": "viagem",
            "pergunta_texto": "Quais países você já visitou?",
            "tipo_resposta": "texto",
            "peso_avaliacao": 7,
            "dica": "Europa, Canadá e outros países desenvolvidos são muito positivos",
            "gratuito": False,
            "ordem": 19
        },
        {
            "categoria": "viagem",
            "pergunta_texto": "Qual é a data prevista para a sua viagem?",
            "tipo_resposta": "texto",
            "peso_avaliacao": 5,
            "dica": "Não precisa ser exata, mas tenha uma estimativa (ex: Julho/2025)",
            "gratuito": False,
            "ordem": 20
        },
        
        # ==================== CATEGORIA: TRABALHO (10) ====================
        {
            "categoria": "trabalho",
            "pergunta_texto": "Qual é a sua ocupação atual?",
            "tipo_resposta": "texto",
            "peso_avaliacao": 10,
            "resposta_ideal": "Ter emprego fixo e estável é crucial",
            "dica": "Seja específico: cargo, nome da empresa, há quanto tempo trabalha",
            "gratuito": True,
            "ordem": 21
        },
        {
            "categoria": "trabalho",
            "pergunta_texto": "Qual é o nome da empresa onde você trabalha?",
            "tipo_resposta": "texto",
            "peso_avaliacao": 8,
            "dica": "Empresas conhecidas/grandes aumentam credibilidade",
            "gratuito": True,
            "ordem": 22
        },
        {
            "categoria": "trabalho",
            "pergunta_texto": "Há quanto tempo você trabalha nesta empresa/profissão?",
            "tipo_resposta": "multipla_escolha",
            "opcoes": ["Menos de 6 meses", "6 meses a 1 ano", "1 a 3 anos", "3 a 5 anos", "Mais de 5 anos"],
            "peso_avaliacao": 9,
            "dica": "Quanto mais tempo, melhor. Acima de 1 ano é ideal",
            "gratuito": True,
            "ordem": 23
        },
        {
            "categoria": "trabalho",
            "pergunta_texto": "Qual é a sua renda mensal aproximada?",
            "tipo_resposta": "multipla_escolha",
            "opcoes": ["Até R$ 2.000", "R$ 2.000-5.000", "R$ 5.000-10.000", "R$ 10.000-20.000", "Acima de R$ 20.000"],
            "peso_avaliacao": 10,
            "dica": "Renda deve ser compatível com os custos da viagem",
            "gratuito": True,
            "ordem": 24
        },
        {
            "categoria": "trabalho",
            "pergunta_texto": "Você tem carteira assinada (CLT)?",
            "tipo_resposta": "sim_nao",
            "peso_avaliacao": 7,
            "dica": "CLT demonstra vínculo empregatício formal",
            "gratuito": False,
            "ordem": 25
        },
        {
            "categoria": "trabalho",
            "pergunta_texto": "Se você for autônomo/empresário, há quanto tempo tem sua empresa?",
            "tipo_resposta": "multipla_escolha",
            "opcoes": ["Não se aplica", "Menos de 1 ano", "1-3 anos", "3-5 anos", "Mais de 5 anos"],
            "peso_avaliacao": 8,
            "dica": "Empresas consolidadas são vistas positivamente",
            "gratuito": False,
            "ordem": 26
        },
        {
            "categoria": "trabalho",
            "pergunta_texto": "Qual é o endereço da sua empresa?",
            "tipo_resposta": "texto",
            "peso_avaliacao": 3,
            "dica": "Pode ser solicitado para verificação",
            "gratuito": False,
            "ordem": 27
        },
        {
            "categoria": "trabalho",
            "pergunta_texto": "Você tem alguma propriedade comercial no Brasil?",
            "tipo_resposta": "sim_nao",
            "peso_avaliacao": 7,
            "dica": "Propriedades são vínculos econômicos fortes",
            "gratuito": False,
            "ordem": 28
        },
        {
            "categoria": "trabalho",
            "pergunta_texto": "Você está estudando atualmente?",
            "tipo_resposta": "sim_nao",
            "peso_avaliacao": 6,
            "dica": "Estudantes com matrícula ativa têm vínculo com retorno",
            "gratuito": False,
            "ordem": 29
        },
        {
            "categoria": "trabalho",
            "pergunta_texto": "Se estudante, qual curso e instituição?",
            "tipo_resposta": "texto",
            "peso_avaliacao": 5,
            "dica": "Universidades reconhecidas são positivas",
            "gratuito": False,
            "ordem": 30
        },
        
        # ==================== CATEGORIA: FAMÍLIA (10) ====================
        {
            "categoria": "familia",
            "pergunta_texto": "Seus pais estão vivos?",
            "tipo_resposta": "multipla_escolha",
            "opcoes": ["Ambos vivos", "Apenas mãe", "Apenas pai", "Ambos falecidos"],
            "peso_avaliacao": 5,
            "dica": "Pais no Brasil são vínculos familiares",
            "gratuito": True,
            "ordem": 31
        },
        {
            "categoria": "familia",
            "pergunta_texto": "Você tem irmãos? Quantos?",
            "tipo_resposta": "texto",
            "peso_avaliacao": 4,
            "dica": "Família no Brasil é sempre positivo",
            "gratuito": True,
            "ordem": 32
        },
        {
            "categoria": "familia",
            "pergunta_texto": "Você tem parentes diretos morando nos Estados Unidos?",
            "tipo_resposta": "sim_nao",
            "peso_avaliacao": 8,
            "dica": "SEJA HONESTO! Mentir é motivo de ban permanente",
            "gratuito": True,
            "ordem": 33
        },
        {
            "categoria": "familia",
            "pergunta_texto": "Se sim, qual o grau de parentesco e status legal deles nos EUA?",
            "tipo_resposta": "texto",
            "peso_avaliacao": 9,
            "dica": "Ter parentes NÃO é negativo se você tem vínculos fortes no Brasil",
            "gratuito": True,
            "ordem": 34
        },
        {
            "categoria": "familia",
            "pergunta_texto": "Seu cônjuge vai viajar com você?",
            "tipo_resposta": "multipla_escolha",
            "opcoes": ["Não sou casado(a)", "Sim, faremos pedido juntos", "Não, cônjuge fica no Brasil"],
            "peso_avaliacao": 7,
            "dica": "Cônjuge no Brasil é vínculo forte de retorno",
            "gratuito": False,
            "ordem": 35
        },
        {
            "categoria": "familia",
            "pergunta_texto": "Se seus filhos ficarem no Brasil, qual a idade deles?",
            "tipo_resposta": "texto",
            "peso_avaliacao": 9,
            "dica": "Filhos menores são um dos maiores vínculos de retorno",
            "gratuito": False,
            "ordem": 36
        },
        {
            "categoria": "familia",
            "pergunta_texto": "Você tem imóvel próprio no Brasil?",
            "tipo_resposta": "sim_nao",
            "peso_avaliacao": 8,
            "dica": "Casa própria é vínculo patrimonial forte",
            "gratuito": False,
            "ordem": 37
        },
        {
            "categoria": "familia",
            "pergunta_texto": "Você mora com seus pais ou possui residência própria?",
            "tipo_resposta": "multipla_escolha",
            "opcoes": ["Com os pais", "Casa/apartamento próprio", "Casa/apartamento alugado", "Outro"],
            "peso_avaliacao": 6,
            "dica": "Imóvel próprio é mais forte como vínculo",
            "gratuito": False,
            "ordem": 38
        },
        {
            "categoria": "familia",
            "pergunta_texto": "Algum membro da sua família já teve visto negado para os EUA?",
            "tipo_resposta": "sim_nao",
            "peso_avaliacao": 7,
            "dica": "Seja honesto. O oficial pode ter acesso a esse histórico",
            "gratuito": False,
            "ordem": 39
        },
        {
            "categoria": "familia",
            "pergunta_texto": "Você é responsável financeiro por algum familiar?",
            "tipo_resposta": "sim_nao",
            "peso_avaliacao": 6,
            "dica": "Dependentes no Brasil são vínculos de retorno",
            "gratuito": False,
            "ordem": 40
        },
        
        # ==================== CATEGORIA: SEGURANÇA (10) ====================
        {
            "categoria": "seguranca",
            "pergunta_texto": "Você já foi preso ou condenado por algum crime?",
            "tipo_resposta": "sim_nao",
            "peso_avaliacao": 10,
            "dica": "SEJA COMPLETAMENTE HONESTO. Mentir resulta em ban permanente",
            "gratuito": True,
            "ordem": 41
        },
        {
            "categoria": "seguranca",
            "pergunta_texto": "Você já teve visto americano negado anteriormente?",
            "tipo_resposta": "sim_nao",
            "peso_avaliacao": 9,
            "dica": "Se sim, entenda os motivos e demonstre mudanças na sua situação",
            "gratuito": True,
            "ordem": 42
        },
        {
            "categoria": "seguranca",
            "pergunta_texto": "Você já violou os termos de qualquer visto no passado?",
            "tipo_resposta": "sim_nao",
            "peso_avaliacao": 10,
            "dica": "Overstay (ficar além do permitido) é muito grave",
            "gratuito": True,
            "ordem": 43
        },
        {
            "categoria": "seguranca",
            "pergunta_texto": "Você já foi deportado de algum país?",
            "tipo_resposta": "sim_nao",
            "peso_avaliacao": 10,
            "dica": "Deportação é fator extremamente negativo",
            "gratuito": True,
            "ordem": 44
        },
        {
            "categoria": "seguranca",
            "pergunta_texto": "Você tem alguma doença transmissível?",
            "tipo_resposta": "sim_nao",
            "peso_avaliacao": 5,
            "dica": "Algumas doenças podem exigir documentação médica adicional",
            "gratuito": False,
            "ordem": 45
        },
        {
            "categoria": "seguranca",
            "pergunta_texto": "Você já esteve envolvido em atividades terroristas?",
            "tipo_resposta": "sim_nao",
            "peso_avaliacao": 10,
            "dica": "Pergunta obrigatória do formulário",
            "gratuito": False,
            "ordem": 46
        },
        {
            "categoria": "seguranca",
            "pergunta_texto": "Você já foi membro de algum partido político totalitário?",
            "tipo_resposta": "sim_nao",
            "peso_avaliacao": 8,
            "dica": "Pergunta obrigatória do DS-160",
            "gratuito": False,
            "ordem": 47
        },
        {
            "categoria": "seguranca",
            "pergunta_texto": "Você pretende trabalhar ilegalmente nos EUA?",
            "tipo_resposta": "sim_nao",
            "peso_avaliacao": 10,
            "dica": "Resposta deve ser NÃO. Trabalho ilegal é inadmissível",
            "gratuito": False,
            "ordem": 48
        },
        {
            "categoria": "seguranca",
            "pergunta_texto": "Você tem histórico de abuso de substâncias?",
            "tipo_resposta": "sim_nao",
            "peso_avaliacao": 7,
            "dica": "Pode requerer documentação médica adicional",
            "gratuito": False,
            "ordem": 49
        },
        {
            "categoria": "seguranca",
            "pergunta_texto": "Você declarou Imposto de Renda nos últimos anos?",
            "tipo_resposta": "sim_nao",
            "peso_avaliacao": 6,
            "dica": "Declaração de IR comprova situação fiscal regular",
            "gratuito": False,
            "ordem": 50
        }
    ]
    
    for p in perguntas:
        pergunta = PerguntaDS160(**p)
        db.add(pergunta)
    
    db.commit()
    print(f"✅ {len(perguntas)} perguntas DS-160 adicionadas!")


def popular_perguntas_entrevista_completo(db: Session):
    """Perguntas de entrevista - BASEADAS EM EXPERIÊNCIAS REAIS"""
    
    perguntas = [
        # ==================== VÍNCULOS COM BRASIL (12) ====================
        {
            "categoria": "vinculos",
            "pergunta_texto": "Por que você quer ir aos Estados Unidos?",
            "resposta_ideal": "Mencione turismo específico (Disney, praias), conhecer lugares famosos, curtir férias. SEMPRE enfatize que vai RETORNAR ao Brasil",
            "palavras_positivas": ["turismo", "conhecer", "férias", "Disney", "retornar", "voltar", "visitar"],
            "palavras_negativas": ["morar", "ficar", "trabalhar", "imigrar", "tentar a sorte"],
            "peso_avaliacao": 10,
            "dica": "PERGUNTA MAIS IMPORTANTE! Seja específico sobre lugares turísticos. Nunca diga que quer 'ver como é'",
            "gratuito": True,
            "ordem": 1
        },
        {
            "categoria": "vinculos",
            "pergunta_texto": "O que você faz no Brasil? Me fale sobre seu trabalho.",
            "resposta_ideal": "Descreva seu cargo, responsabilidades, tempo na empresa, projetos importantes. Demonstre que tem uma carreira estabelecida",
            "palavras_positivas": ["trabalho há", "anos", "empresa", "responsabilidade", "equipe", "carreira", "projetos"],
            "palavras_negativas": ["temporário", "bico", "informal", "desempregado", "sem carteira"],
            "peso_avaliacao": 10,
            "dica": "Demonstre ESTABILIDADE. Mencione tempo de casa, colegas, projetos em andamento",
            "gratuito": True,
            "ordem": 2
        },
        {
            "categoria": "vinculos",
            "pergunta_texto": "Você tem família no Brasil? Me fale sobre eles.",
            "resposta_ideal": "Mencione cônjuge, filhos (principalmente menores), pais, irmãos. Quanto mais vínculos familiares, melhor",
            "palavras_positivas": ["esposa", "marido", "filhos", "pais", "família", "dependentes", "casado"],
            "palavras_negativas": ["sozinho", "sem família", "pais falecidos"],
            "peso_avaliacao": 9,
            "dica": "Família é um dos vínculos MAIS FORTES. Enfatize dependentes e cônjuge",
            "gratuito": True,
            "ordem": 3
        },
        {
            "categoria": "vinculos",
            "pergunta_texto": "Você vai voltar ao Brasil? Por quê?",
            "resposta_ideal": "SIM, com motivos CLAROS: trabalho, família, casa, compromissos profissionais, projetos em andamento",
            "palavras_positivas": ["sim", "trabalho", "família", "casa", "responsabilidades", "compromissos", "carreira"],
            "palavras_negativas": ["talvez", "não sei", "depende", "vou ver", "quero ficar"],
            "peso_avaliacao": 10,
            "dica": "CRUCIAL! Liste 3-4 motivos CONCRETOS de retorno. Seja CONVINCENTE!",
            "gratuito": True,
            "ordem": 4
        },
        {
            "categoria": "vinculos",
            "pergunta_texto": "Você tem casa própria no Brasil?",
            "resposta_ideal": "Sim, descreva se é casa/apartamento, localização, se está quitado",
            "palavras_positivas": ["própria", "quitada", "financiando", "meu nome"],
            "palavras_negativas": ["alugada", "dos pais", "não tenho"],
            "peso_avaliacao": 8,
            "dica": "Imóvel próprio é VÍNCULO PATRIMONIAL forte",
            "gratuito": True,
            "ordem": 5
        },
        {
            "categoria": "vinculos",
            "pergunta_texto": "Quanto tempo você trabalha na sua empresa atual?",
            "resposta_ideal": "Quanto mais tempo, melhor. Mínimo recomendado: 1 ano",
            "palavras_positivas": ["anos", "desde", "estável", "consolidado"],
            "palavras_negativas": ["recém-contratado", "semanas", "meses", "novo emprego"],
            "peso_avaliacao": 9,
            "dica": "Se trabalha há pouco tempo, explique seu histórico profissional anterior",
            "gratuito": True,
            "ordem": 6
        },
        {
            "categoria": "vinculos",
            "pergunta_texto": "Seus filhos vão com você ou ficam no Brasil?",
            "resposta_ideal": "Se ficarem no Brasil (especialmente menores), é ÓTIMO para vínculo de retorno",
            "palavras_positivas": ["ficam", "escola", "estudando", "menores"],
            "palavras_negativas": ["vão comigo", "não tenho filhos"],
            "peso_avaliacao": 9,
            "dica": "Filhos no Brasil = razão FORTE para retornar",
            "gratuito": False,
            "ordem": 7
        },
        {
            "categoria": "vinculos",
            "pergunta_texto": "O que você vai fazer quando voltar dos Estados Unidos?",
            "resposta_ideal": "Retomar trabalho, ver família, continuar projetos, compromissos agendados",
            "palavras_positivas": ["trabalho", "projetos", "reuniões", "compromissos", "família"],
            "palavras_negativas": ["não sei", "vou ver", "nada específico"],
            "peso_avaliacao": 8,
            "dica": "Demonstre que tem planos CONCRETOS no Brasil após a viagem",
            "gratuito": False,
            "ordem": 8
        },
        {
            "categoria": "vinculos",
            "pergunta_texto": "Você tem carro próprio no Brasil?",
            "resposta_ideal": "Sim, carro próprio é bem patrimonial",
            "palavras_positivas": ["próprio", "quitado", "meu nome"],
            "peso_avaliacao": 5,
            "dica": "Patrimônio demonstra vínculos econômicos",
            "gratuito": False,
            "ordem": 9
        },
        {
            "categoria": "vinculos",
            "pergunta_texto": "Você tem algum negócio próprio no Brasil?",
            "resposta_ideal": "Empresa própria consolidada é vínculo forte",
            "palavras_positivas": ["empresa", "anos", "funcionários", "estabelecida"],
            "peso_avaliacao": 8,
            "dica": "Se tem empresa, mencione tempo de funcionamento e funcionários",
            "gratuito": False,
            "ordem": 10
        },
        {
            "categoria": "vinculos",
            "pergunta_texto": "Quanto tempo faz que você mora no seu endereço atual?",
            "resposta_ideal": "Quanto mais tempo, melhor. Demonstra estabilidade",
            "palavras_positivas": ["anos", "sempre morei", "desde"],
            "peso_avaliacao": 5,
            "dica": "Estabilidade residencial é positiva",
            "gratuito": False,
            "ordem": 11
        },
        {
            "categoria": "vinculos",
            "pergunta_texto": "Você está matriculado em algum curso ou faculdade?",
            "resposta_ideal": "Estudante matriculado tem compromisso de retorno",
            "palavras_positivas": ["matriculado", "cursando", "semestre", "faculdade"],
            "peso_avaliacao": 7,
            "dica": "Se for estudante, leve comprovante de matrícula",
            "gratuito": False,
            "ordem": 12
        },
        
        # ==================== SITUAÇÃO FINANCEIRA (10) ====================
        {
            "categoria": "financeiro",
            "pergunta_texto": "Quem vai pagar pela sua viagem?",
            "resposta_ideal": "Você mesmo com seus recursos. Se alguém pagar, explique claramente a relação e capacidade financeira",
            "palavras_positivas": ["eu mesmo", "minha renda", "minhas economias", "meu salário"],
            "palavras_negativas": ["não sei", "talvez", "vou ver", "emprestado"],
            "peso_avaliacao": 10,
            "dica": "CRUCIAL! Demonstre capacidade financeira CLARA e documentada",
            "gratuito": True,
            "ordem": 13
        },
        {
            "categoria": "financeiro",
            "pergunta_texto": "Quanto você ganha por mês?",
            "resposta_ideal": "Seja honesto e tenha documentos que comprovem (holerite, declaração IR)",
            "palavras_positivas": ["salário", "renda", "comprovante", "holerite"],
            "palavras_negativas": ["aproximadamente", "mais ou menos", "varia muito"],
            "peso_avaliacao": 10,
            "dica": "Saiba o valor EXATO. Renda deve ser compatível com custos da viagem",
            "gratuito": True,
            "ordem": 14
        },
        {
            "categoria": "financeiro",
            "pergunta_texto": "Quanto você estima gastar na viagem?",
            "resposta_ideal": "Tenha um valor realista. Viagem de 2 semanas: US$ 3.000-5.000 por pessoa",
            "palavras_positivas": ["planejei", "estimativa", "dólares"],
            "peso_avaliacao": 8,
            "dica": "Valores muito baixos podem gerar suspeitas",
            "gratuito": True,
            "ordem": 15
        },
        {
            "categoria": "financeiro",
            "pergunta_texto": "Você tem poupança ou investimentos?",
            "resposta_ideal": "Sim, demonstre capacidade de poupar",
            "palavras_positivas": ["poupança", "investimentos", "reserva", "aplicação"],
            "peso_avaliacao": 8,
            "dica": "Leve extratos bancários mostrando movimentação regular",
            "gratuito": True,
            "ordem": 16
        },
        {
            "categoria": "financeiro",
            "pergunta_texto": "Você declara Imposto de Renda?",
            "resposta_ideal": "Sim, declaração de IR comprova situação fiscal regular",
            "palavras_positivas": ["declaro", "anualmente", "última declaração"],
            "peso_avaliacao": 7,
            "dica": "Leve cópia da última declaração",
            "gratuito": False,
            "ordem": 17
        },
        {
            "categoria": "financeiro",
            "pergunta_texto": "Se outra pessoa vai pagar, qual a relação com você?",
            "resposta_ideal": "Pai/mãe, cônjuge, patrocinador com carta formal",
            "palavras_positivas": ["pai", "mãe", "cônjuge", "patrocinador", "carta"],
            "peso_avaliacao": 8,
            "dica": "Patrocinador precisa de carta assinada + comprovante de renda",
            "gratuito": False,
            "ordem": 18
        },
        {
            "categoria": "financeiro",
            "pergunta_texto": "Você tem dívidas? Seu nome está limpo?",
            "resposta_ideal": "Nome limpo e sem dívidas significativas",
            "palavras_positivas": ["não tenho dívidas", "nome limpo", "sem restrições"],
            "peso_avaliacao": 6,
            "dica": "Dívidas muito altas podem indicar risco de imigração ilegal",
            "gratuito": False,
            "ordem": 19
        },
        {
            "categoria": "financeiro",
            "pergunta_texto": "Quanto você tem em conta corrente/poupança atualmente?",
            "resposta_ideal": "Saldo compatível com custos da viagem",
            "palavras_positivas": ["saldo", "economia", "reserva"],
            "peso_avaliacao": 8,
            "dica": "Não precisa ser rico, mas precisa demonstrar que pode custear a viagem",
            "gratuito": False,
            "ordem": 20
        },
        {
            "categoria": "financeiro",
            "pergunta_texto": "Você tem cartão de crédito? Qual o limite?",
            "resposta_ideal": "Cartão com limite razoável demonstra crédito",
            "palavras_positivas": ["tenho", "limite", "internacional"],
            "peso_avaliacao": 5,
            "dica": "Cartão internacional facilita demonstrar capacidade de pagamento",
            "gratuito": False,
            "ordem": 21
        },
        {
            "categoria": "financeiro",
            "pergunta_texto": "Você já comprou dólar para a viagem?",
            "resposta_ideal": "Não precisa ter comprado antes da aprovação",
            "palavras_positivas": ["vou comprar após aprovação", "pretendo levar"],
            "peso_avaliacao": 4,
            "dica": "Ter câmbio já comprado pode demonstrar planejamento",
            "gratuito": False,
            "ordem": 22
        },
        
        # ==================== PROPÓSITO DA VIAGEM (8) ====================
        {
            "categoria": "viagem",
            "pergunta_texto": "Quais cidades você vai visitar nos Estados Unidos?",
            "resposta_ideal": "Tenha um roteiro ESPECÍFICO. Ex: Orlando (Disney, Universal), Miami (praias), Nova York (Estátua da Liberdade)",
            "palavras_positivas": ["Disney", "Orlando", "Miami", "Nova York", "parques", "pontos turísticos"],
            "palavras_negativas": ["não sei ainda", "vou decidir lá", "vou ver"],
            "peso_avaliacao": 9,
            "dica": "Demonstre PLANEJAMENTO. Mencione atrações turísticas específicas",
            "gratuito": True,
            "ordem": 23
        },
        {
            "categoria": "viagem",
            "pergunta_texto": "Você já viajou para outros países? Quais?",
            "resposta_ideal": "Histórico de viagens internacionais com RETORNO é excelente",
            "palavras_positivas": ["Europa", "Canadá", "retornei", "várias vezes", "sempre voltei"],
            "palavras_negativas": ["primeira viagem internacional", "nunca saí do Brasil"],
            "peso_avaliacao": 8,
            "dica": "Se já viajou e retornou, é MUITO positivo. Leve carimbos do passaporte",
            "gratuito": True,
            "ordem": 24
        },
        {
            "categoria": "viagem",
            "pergunta_texto": "Com quem você vai viajar?",
            "resposta_ideal": "Viagens em família são mais confiáveis",
            "palavras_positivas": ["família", "esposa", "marido", "filhos", "pais"],
            "palavras_negativas": ["sozinho", "amigos que mal conheço"],
            "peso_avaliacao": 7,
            "dica": "Família viajando junta tem mais chance de aprovação",
            "gratuito": True,
            "ordem": 25
        },
        {
            "categoria": "viagem",
            "pergunta_texto": "Onde você vai ficar hospedado?",
            "resposta_ideal": "Hotel reservado ou endereço específico de amigos/família",
            "palavras_positivas": ["hotel", "reserva", "Airbnb", "endereço específico"],
            "palavras_negativas": ["não sei", "vou procurar lá", "ainda não decidi"],
            "peso_avaliacao": 7,
            "dica": "Ter reserva ou endereço demonstra planejamento",
            "gratuito": False,
            "ordem": 26
        },
        {
            "categoria": "viagem",
            "pergunta_texto": "Quando você pretende viajar? Já tem datas?",
            "resposta_ideal": "Tenha período estimado, mesmo que não exato",
            "palavras_positivas": ["próximo mês", "julho", "férias", "período estimado"],
            "peso_avaliacao": 6,
            "dica": "Não precisa data exata, mas tenha ideia do período",
            "gratuito": False,
            "ordem": 27
        },
        {
            "categoria": "viagem",
            "pergunta_texto": "Por que você escolheu os Estados Unidos e não outro país?",
            "resposta_ideal": "Mencione atrações específicas americanas (parques, compras, lugares icônicos)",
            "palavras_positivas": ["Disney", "parques", "lugares famosos", "sempre quis conhecer"],
            "peso_avaliacao": 6,
            "dica": "Demonstre interesse genuíno em turismo específico",
            "gratuito": False,
            "ordem": 28
        },
        {
            "categoria": "viagem",
            "pergunta_texto": "Você já comprou passagens aéreas?",
            "resposta_ideal": "NÃO compre antes da aprovação!",
            "palavras_positivas": ["vou comprar após aprovação", "aguardando visto"],
            "palavras_negativas": ["já comprei"],
            "peso_avaliacao": 4,
            "dica": "Comprar antes é ERRO. Pode parecer presunção de aprovação",
            "gratuito": False,
            "ordem": 29
        },
        {
            "categoria": "viagem",
            "pergunta_texto": "Você tem seguro viagem?",
            "resposta_ideal": "Pretende contratar (não obrigatório, mas é positivo)",
            "palavras_positivas": ["vou contratar", "pretendo fazer"],
            "peso_avaliacao": 3,
            "dica": "Seguro viagem demonstra responsabilidade",
            "gratuito": False,
            "ordem": 30
        },
        
        # ==================== HISTÓRICO E INTENÇÕES (10) ====================
        {
            "categoria": "pessoal",
            "pergunta_texto": "Você tem amigos ou parentes nos Estados Unidos?",
            "resposta_ideal": "Seja HONESTO. Se sim, deixe claro que vai visitar brevemente",
            "palavras_positivas": ["visitar", "brevemente", "turismo", "poucos dias"],
            "palavras_negativas": ["morar com", "ficar na casa", "ajudar financeiramente"],
            "peso_avaliacao": 8,
            "dica": "Ter parentes NÃO é problema se você tem vínculos fortes no Brasil",
            "gratuito": True,
            "ordem": 31
        },
        {
            "categoria": "pessoal",
            "pergunta_texto": "Alguém da sua família já morou ou mora ilegalmente nos EUA?",
            "resposta_ideal": "SEJA HONESTO. O oficial pode ter acesso a esse histórico",
            "palavras_positivas": ["não", "ninguém"],
            "peso_avaliacao": 9,
            "dica": "Mentir sobre isso pode resultar em ban permanente",
            "gratuito": True,
            "ordem": 32
        },
        {
            "categoria": "pessoal",
            "pergunta_texto": "Você já teve visto negado para algum país?",
            "resposta_ideal": "Se sim, explique os motivos e como sua situação mudou",
            "palavras_positivas": ["não", "situação mudou", "vínculos fortaleceram"],
            "peso_avaliacao": 8,
            "dica": "Negação anterior não impede nova tentativa se situação melhorou",
            "gratuito": True,
            "ordem": 33
        },
        {
            "categoria": "pessoal",
            "pergunta_texto": "O que você acha dos Estados Unidos?",
            "resposta_ideal": "Seja positivo, mas não exagerado. Mencione admiração por atrações turísticas",
            "palavras_positivas": ["bonito", "interessante", "quero conhecer", "cultura"],
            "palavras_negativas": ["melhor que Brasil", "perfeito", "queria morar lá"],
            "peso_avaliacao": 5,
            "dica": "Demonstre interesse turístico, não interesse em emigrar",
            "gratuito": True,
            "ordem": 34
        },
        {
            "categoria": "pessoal",
            "pergunta_texto": "Você fala inglês?",
            "resposta_ideal": "Seja honesto sobre seu nível. Não é obrigatório falar inglês",
            "palavras_positivas": ["básico", "estou aprendendo", "intermediário"],
            "peso_avaliacao": 4,
            "dica": "Se falar bem inglês, pode conduzir entrevista em inglês",
            "gratuito": False,
            "ordem": 35
        },
        {
            "categoria": "pessoal",
            "pergunta_texto": "Por que você está solicitando o visto agora?",
            "resposta_ideal": "Momento adequado: férias marcadas, economia junta, oportunidade surgiu",
            "palavras_positivas": ["férias", "oportunidade", "planejamento", "sempre quis"],
            "peso_avaliacao": 5,
            "dica": "Demonstre que é o momento certo na sua vida",
            "gratuito": False,
            "ordem": 36
        },
        {
            "categoria": "pessoal",
            "pergunta_texto": "Você pretende estudar ou trabalhar nos EUA?",
            "resposta_ideal": "NÃO para visto de turismo. Se sim, precisa visto específico",
            "palavras_positivas": ["não", "apenas turismo"],
            "palavras_negativas": ["sim", "talvez", "gostaria"],
            "peso_avaliacao": 10,
            "dica": "Para turismo B1/B2, resposta deve ser NÃO",
            "gratuito": False,
            "ordem": 37
        },
        {
            "categoria": "pessoal",
            "pergunta_texto": "Se você gostar muito dos EUA, você voltaria ao Brasil?",
            "resposta_ideal": "SIM! Enfatize vínculos e que é apenas turismo",
            "palavras_positivas": ["sim", "com certeza", "tenho vida no Brasil", "responsabilidades"],
            "palavras_negativas": ["não sei", "talvez não", "depende"],
            "peso_avaliacao": 10,
            "dica": "PERGUNTA PEGADINHA! Sempre responda SIM com convicção",
            "gratuito": False,
            "ordem": 38
        },
        {
            "categoria": "pessoal",
            "pergunta_texto": "O que mais te atrai nos Estados Unidos?",
            "resposta_ideal": "Atrações TURÍSTICAS específicas, não estilo de vida",
            "palavras_positivas": ["parques", "praias", "pontos turísticos", "cultura"],
            "palavras_negativas": ["qualidade de vida", "oportunidades", "dólares"],
            "peso_avaliacao": 6,
            "dica": "Foque em TURISMO, não em vantagens de morar lá",
            "gratuito": False,
            "ordem": 39
        },
        {
            "categoria": "pessoal",
            "pergunta_texto": "Você está satisfeito com sua vida no Brasil?",
            "resposta_ideal": "SIM! Demonstre satisfação com trabalho, família, vida",
            "palavras_positivas": ["sim", "satisfeito", "feliz", "realizado", "bom emprego"],
            "palavras_negativas": ["não muito", "poderia ser melhor", "insatisfeito"],
            "peso_avaliacao": 8,
            "dica": "Pessoa insatisfeita é risco de imigração. Demonstre contentamento!",
            "gratuito": False,
            "ordem": 40
        }
    ]
    
    for p in perguntas:
        pergunta = PerguntaEntrevista(**p)
        db.add(pergunta)
    
    db.commit()
    print(f"✅ {len(perguntas)} perguntas de entrevista adicionadas!")


def main():
    """Executar população completa do banco"""
    print("🚀 POPULANDO BANCO DE DADOS COMPLETO")
    print("📋 50 perguntas DS-160 + 40 perguntas de entrevista")
    print("🎯 Baseado em experiências REAIS de brasileiros\n")
    
    db = SessionLocal()
    
    try:
        # Limpar dados antigos
        print("🗑️  Limpando dados antigos...")
        db.query(PerguntaDS160).delete()
        db.query(PerguntaEntrevista).delete()
        db.commit()
        print("✅ Dados antigos removidos\n")
        
        # Popular novas perguntas
        print("📝 Adicionando perguntas DS-160...")
        popular_perguntas_ds160_completo(db)
        
        print("\n💬 Adicionando perguntas de entrevista...")
        popular_perguntas_entrevista_completo(db)
        
        # Estatísticas
        print("\n" + "="*60)
        print("✅ BANCO DE DADOS POPULADO COM SUCESSO!")
        print("="*60)
        
        total_ds160 = db.query(PerguntaDS160).count()
        gratuitas_ds160 = db.query(PerguntaDS160).filter(PerguntaDS160.gratuito == True).count()
        premium_ds160 = total_ds160 - gratuitas_ds160
        
        total_entrevista = db.query(PerguntaEntrevista).count()
        gratuitas_entrevista = db.query(PerguntaEntrevista).filter(PerguntaEntrevista.gratuito == True).count()
        premium_entrevista = total_entrevista - gratuitas_entrevista
        
        print(f"\n📊 ESTATÍSTICAS:")
        print(f"\n🗂️  PERGUNTAS DS-160:")
        print(f"   Total: {total_ds160}")
        print(f"   ├─ Gratuitas: {gratuitas_ds160}")
        print(f"   └─ Premium: {premium_ds160}")
        
        print(f"\n💬 PERGUNTAS ENTREVISTA:")
        print(f"   Total: {total_entrevista}")
        print(f"   ├─ Gratuitas: {gratuitas_entrevista}")
        print(f"   └─ Premium: {premium_entrevista}")
        
        print(f"\n🎯 TOTAL GERAL: {total_ds160 + total_entrevista} perguntas")
        print(f"   ├─ Modo Gratuito: {gratuitas_ds160 + gratuitas_entrevista} perguntas")
        print(f"   └─ Modo Premium: {premium_ds160 + premium_entrevista} perguntas")
        
        print("\n📂 CATEGORIAS DS-160:")
        for cat in ["pessoal", "viagem", "trabalho", "familia", "seguranca"]:
            count = db.query(PerguntaDS160).filter(PerguntaDS160.categoria == cat).count()
            print(f"   └─ {cat.capitalize()}: {count} perguntas")
        
        print("\n📂 CATEGORIAS ENTREVISTA:")
        for cat in ["vinculos", "financeiro", "viagem", "pessoal"]:
            count = db.query(PerguntaEntrevista).filter(PerguntaEntrevista.categoria == cat).count()
            print(f"   └─ {cat.capitalize()}: {count} perguntas")
        
        print("\n" + "="*60)
        print("🎉 Pronto para usar! Execute: python -m uvicorn app.main:app --reload")
        print("="*60 + "\n")
        
    except Exception as e:
        print(f"\n❌ ERRO: {e}")
        db.rollback()
    finally:
        db.close()


if __name__ == "__main__":
    main()