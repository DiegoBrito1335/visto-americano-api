"""
Script para popular o banco de dados com perguntas de exemplo
Execute: python populate_db.py
"""

from sqlalchemy.orm import Session
from app.database import SessionLocal, engine, Base
from app.models import PerguntaDS160, PerguntaEntrevista

# Criar tabelas
Base.metadata.create_all(bind=engine)

def popular_perguntas_ds160(db: Session):
    """Adicionar perguntas DS-160 de exemplo"""
    
    perguntas = [
        # CATEGORIA: PESSOAL (gratuitas)
        {
            "categoria": "pessoal",
            "pergunta_texto": "Qual é o seu nome completo como consta no passaporte?",
            "tipo_resposta": "texto",
            "peso_avaliacao": 3,
            "dica": "Digite exatamente como aparece no seu passaporte",
            "gratuito": True,
            "ordem": 1
        },
        {
            "categoria": "pessoal",
            "pergunta_texto": "Você já teve outros nomes (nome de solteira, apelido legal)?",
            "tipo_resposta": "sim_nao",
            "peso_avaliacao": 2,
            "dica": "Seja honesto, isso não afeta negativamente",
            "gratuito": True,
            "ordem": 2
        },
        {
            "categoria": "pessoal",
            "pergunta_texto": "Qual é o seu estado civil?",
            "tipo_resposta": "multipla_escolha",
            "opcoes": ["Solteiro(a)", "Casado(a)", "Divorciado(a)", "Viúvo(a)", "União Estável"],
            "peso_avaliacao": 6,
            "dica": "Ser casado ou ter família pode demonstrar vínculos mais fortes",
            "gratuito": True,
            "ordem": 3
        },
        {
            "categoria": "pessoal",
            "pergunta_texto": "Você tem filhos?",
            "tipo_resposta": "sim_nao",
            "peso_avaliacao": 7,
            "dica": "Filhos no Brasil são considerados vínculos fortes",
            "gratuito": True,
            "ordem": 4
        },
        
        # CATEGORIA: TRABALHO
        {
            "categoria": "trabalho",
            "pergunta_texto": "Qual é a sua ocupação atual?",
            "tipo_resposta": "texto",
            "peso_avaliacao": 9,
            "resposta_ideal": "Ter emprego estável demonstra vínculos econômicos com o Brasil",
            "dica": "Seja específico: cargo, empresa, tempo no emprego",
            "gratuito": True,
            "ordem": 5
        },
        {
            "categoria": "trabalho",
            "pergunta_texto": "Há quanto tempo você trabalha nessa empresa/profissão?",
            "tipo_resposta": "texto",
            "peso_avaliacao": 8,
            "dica": "Maior tempo = mais estabilidade = melhor avaliação",
            "gratuito": False,
            "ordem": 6
        },
        {
            "categoria": "trabalho",
            "pergunta_texto": "Qual é a sua renda mensal aproximada?",
            "tipo_resposta": "multipla_escolha",
            "opcoes": ["Até R$ 2.000", "R$ 2.000-5.000", "R$ 5.000-10.000", "R$ 10.000-20.000", "Acima de R$ 20.000"],
            "peso_avaliacao": 10,
            "dica": "Renda compatível com a viagem é importante",
            "gratuito": False,
            "ordem": 7
        },
        
        # CATEGORIA: VIAGEM
        {
            "categoria": "viagem",
            "pergunta_texto": "Qual é o propósito principal da sua viagem aos EUA?",
            "tipo_resposta": "multipla_escolha",
            "opcoes": ["Turismo", "Negócios", "Visitar familiares", "Estudos", "Tratamento médico", "Outro"],
            "peso_avaliacao": 10,
            "dica": "Turismo é o mais comum e aceito",
            "gratuito": True,
            "ordem": 8
        },
        {
            "categoria": "viagem",
            "pergunta_texto": "Quanto tempo você pretende ficar nos EUA?",
            "tipo_resposta": "texto",
            "peso_avaliacao": 8,
            "dica": "Viagens curtas (1-3 semanas) são vistas com melhores olhos",
            "gratuito": True,
            "ordem": 9
        },
        {
            "categoria": "viagem",
            "pergunta_texto": "Você já tem passagens aéreas compradas?",
            "tipo_resposta": "sim_nao",
            "peso_avaliacao": 5,
            "dica": "Ter passagens demonstra planejamento, mas não compre antes da aprovação",
            "gratuito": False,
            "ordem": 10
        },
        
        # CATEGORIA: FAMÍLIA
        {
            "categoria": "familia",
            "pergunta_texto": "Seus pais estão vivos?",
            "tipo_resposta": "multipla_escolha",
            "opcoes": ["Ambos vivos", "Apenas mãe", "Apenas pai", "Ambos falecidos"],
            "peso_avaliacao": 4,
            "dica": "Família no Brasil é vínculo positivo",
            "gratuito": False,
            "ordem": 11
        },
        {
            "categoria": "familia",
            "pergunta_texto": "Você tem parentes morando nos Estados Unidos?",
            "tipo_resposta": "sim_nao",
            "peso_avaliacao": 7,
            "dica": "Seja honesto. Ter parentes não é negativo se você tiver vínculos fortes no Brasil",
            "gratuito": True,
            "ordem": 12
        },
        
        # CATEGORIA: SEGURANÇA
        {
            "categoria": "seguranca",
            "pergunta_texto": "Você já foi preso ou condenado por algum crime?",
            "tipo_resposta": "sim_nao",
            "peso_avaliacao": 10,
            "dica": "Seja completamente honesto. Mentir pode resultar em ban permanente",
            "gratuito": True,
            "ordem": 13
        },
        {
            "categoria": "seguranca",
            "pergunta_texto": "Você já teve visto americano negado anteriormente?",
            "tipo_resposta": "sim_nao",
            "peso_avaliacao": 9,
            "dica": "Se sim, entenda os motivos e demonstre mudanças desde então",
            "gratuito": True,
            "ordem": 14
        }
    ]
    
    for p in perguntas:
        pergunta = PerguntaDS160(**p)
        db.add(pergunta)
    
    db.commit()
    print(f"✅ {len(perguntas)} perguntas DS-160 adicionadas!")


def popular_perguntas_entrevista(db: Session):
    """Adicionar perguntas de entrevista de exemplo"""
    
    perguntas = [
        # VÍNCULOS
        {
            "categoria": "vinculos",
            "pergunta_texto": "Por que você quer ir aos Estados Unidos?",
            "resposta_ideal": "Mencione turismo, conhecer lugares específicos, retorno garantido ao Brasil",
            "palavras_positivas": ["turismo", "conhecer", "férias", "retornar", "voltar"],
            "palavras_negativas": ["morar", "ficar", "trabalhar ilegalmente"],
            "peso_avaliacao": 10,
            "dica": "Seja claro e específico sobre seus planos de turismo",
            "gratuito": True,
            "ordem": 1
        },
        {
            "categoria": "vinculos",
            "pergunta_texto": "O que você faz no Brasil? Me fale sobre seu trabalho.",
            "resposta_ideal": "Descreva seu cargo, responsabilidades, tempo de empresa, estabilidade",
            "palavras_positivas": ["empresa", "anos", "responsabilidade", "carreira", "equipe"],
            "palavras_negativas": ["temporário", "bico", "informal"],
            "peso_avaliacao": 9,
            "dica": "Demonstre estabilidade profissional e compromisso com seu emprego",
            "gratuito": True,
            "ordem": 2
        },
        {
            "categoria": "vinculos",
            "pergunta_texto": "Você tem família no Brasil?",
            "resposta_ideal": "Mencione cônjuge, filhos, pais - quanto mais vínculos familiares, melhor",
            "palavras_positivas": ["esposa", "marido", "filhos", "pais", "família"],
            "palavras_negativas": ["sozinho", "ninguém"],
            "peso_avaliacao": 8,
            "dica": "Família é um dos vínculos mais fortes",
            "gratuito": True,
            "ordem": 3
        },
        
        # FINANCEIRO
        {
            "categoria": "financeiro",
            "pergunta_texto": "Quem vai pagar pela sua viagem?",
            "resposta_ideal": "Você mesmo com seus recursos. Se alguém pagar, explique a relação e capacidade",
            "palavras_positivas": ["eu mesmo", "minha renda", "minhas economias", "trabalho"],
            "palavras_negativas": ["não sei", "talvez"],
            "peso_avaliacao": 10,
            "dica": "Demonstre capacidade financeira clara",
            "gratuito": True,
            "ordem": 4
        },
        {
            "categoria": "financeiro",
            "pergunta_texto": "Quanto você ganha por mês?",
            "resposta_ideal": "Seja honesto e tenha documentos que comprovem",
            "palavras_positivas": ["salário", "renda", "comprovante"],
            "palavras_negativas": ["aproximadamente", "mais ou menos"],
            "peso_avaliacao": 9,
            "dica": "Saiba o valor exato e tenha comprovação",
            "gratuito": False,
            "ordem": 5
        },
        
        # VIAGEM
        {
            "categoria": "viagem",
            "pergunta_texto": "Quais cidades você vai visitar?",
            "resposta_ideal": "Tenha um roteiro definido, conheça os lugares",
            "palavras_positivas": ["Disney", "Nova York", "Miami", "conhecer", "parques"],
            "palavras_negativas": ["não sei ainda", "vou decidir lá"],
            "peso_avaliacao": 7,
            "dica": "Demonstre planejamento da viagem",
            "gratuito": True,
            "ordem": 6
        },
        {
            "categoria": "viagem",
            "pergunta_texto": "Você já viajou para outros países?",
            "resposta_ideal": "Histórico de viagens internacionais com retorno é positivo",
            "palavras_positivas": ["Europa", "retornei", "várias vezes", "sempre voltei"],
            "palavras_negativas": ["primeira viagem internacional"],
            "peso_avaliacao": 6,
            "dica": "Histórico de viagens com retorno é muito positivo",
            "gratuito": False,
            "ordem": 7
        },
        
        # PESSOAL
        {
            "categoria": "pessoal",
            "pergunta_texto": "Você pretende voltar ao Brasil? Por quê?",
            "resposta_ideal": "Sim, com motivos claros: trabalho, família, casa, compromissos",
            "palavras_positivas": ["trabalho", "família", "casa", "responsabilidades", "compromissos"],
            "palavras_negativas": ["talvez", "não sei", "depende"],
            "peso_avaliacao": 10,
            "dica": "Esta é a pergunta mais importante. Seja convincente!",
            "gratuito": True,
            "ordem": 8
        },
        {
            "categoria": "pessoal",
            "pergunta_texto": "Você tem amigos ou parentes nos Estados Unidos?",
            "resposta_ideal": "Seja honesto. Se sim, deixe claro que vai visitar brevemente",
            "palavras_positivas": ["visitar", "breve", "turismo"],
            "palavras_negativas": ["morar com", "ficar na casa"],
            "peso_avaliacao": 6,
            "dica": "Ter parentes não é problema se você tem vínculos fortes no Brasil",
            "gratuito": True,
            "ordem": 9
        }
    ]
    
    for p in perguntas:
        pergunta = PerguntaEntrevista(**p)
        db.add(pergunta)
    
    db.commit()
    print(f"✅ {len(perguntas)} perguntas de entrevista adicionadas!")


def main():
    """Executar script de população"""
    print("🚀 Iniciando população do banco de dados...\n")
    
    db = SessionLocal()
    
    try:
        # Limpar dados antigos (opcional)
        db.query(PerguntaDS160).delete()
        db.query(PerguntaEntrevista).delete()
        db.commit()
        print("🗑️  Dados antigos removidos\n")
        
        # Popular novas perguntas
        popular_perguntas_ds160(db)
        popular_perguntas_entrevista(db)
        
        print("\n✅ Banco de dados populado com sucesso!")
        print("\n📊 Resumo:")
        print(f"   - Perguntas DS-160: {db.query(PerguntaDS160).count()}")
        print(f"   - Perguntas Entrevista: {db.query(PerguntaEntrevista).count()}")
        print(f"   - Perguntas Gratuitas DS-160: {db.query(PerguntaDS160).filter(PerguntaDS160.gratuito == True).count()}")
        print(f"   - Perguntas Gratuitas Entrevista: {db.query(PerguntaEntrevista).filter(PerguntaEntrevista.gratuito == True).count()}")
        
    except Exception as e:
        print(f"❌ Erro: {e}")
        db.rollback()
    finally:
        db.close()


if __name__ == "__main__":
    main()