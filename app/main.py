from fastapi import FastAPI, HTTPException, Depends, status, Request
from fastapi.middleware.cors import CORSMiddleware
from fastapi.security import OAuth2PasswordRequestForm
from sqlalchemy.orm import Session
from typing import List, Union
from datetime import timedelta
import uvicorn
import os

from app.database import engine, get_db, Base
from app import models, schemas
from app.auth import (
    gerar_hash_senha,
    autenticar_usuario,
    criar_token,
    get_current_user,
)
from app.pagamentos import router as pagamentos_router

# Criar tabelas
Base.metadata.create_all(bind=engine)

# ================================
#   FASTAPI CONFIG
# ================================
app = FastAPI(
    title="API Visto Americano",
    description="API para simulação de preparação para visto americano",
    version="1.0.0",
)

# Rotas de pagamento
app.include_router(pagamentos_router)

# ================================
#   CORS SEGURO (ATUALIZADO)
# ================================
FRONTEND_URL = os.getenv("URL_FRONTEND", "https://visto-americano-api.vercel.app")

app.add_middleware(
    CORSMiddleware,
    allow_origins=[
        FRONTEND_URL,
        "https://visto-americano-api.vercel.app",
        "http://localhost:8080",
        "http://localhost:3000",
        "http://127.0.0.1:8080",
        "http://127.0.0.1:3000",
        "*"  # Aceita todas as origens (mantenha temporariamente)
    ],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# ================================
#   ROTAS
# ================================

@app.get("/")
def home():
    return {
        "mensagem": "API Visto Americano funcionando!",
        "versao": "1.0.0",
        "documentacao": "/docs",
        "frontend_autorizado": FRONTEND_URL
    }


# ============================================================
# REGISTRO DE USUÁRIO
# ============================================================
@app.post("/api/registrar", response_model=schemas.UsuarioResposta, status_code=status.HTTP_201_CREATED)
def registrar_usuario(usuario: schemas.UsuarioCriar, db: Session = Depends(get_db)):
    """Registrar novo usuário"""
    usuario_existente = db.query(models.Usuario).filter(
        models.Usuario.email == usuario.email
    ).first()
    
    if usuario_existente:
        raise HTTPException(status_code=400, detail="E-mail já registrado.")
    
    senha_hash = gerar_hash_senha(usuario.senha)
    novo_usuario = models.Usuario(
        email=usuario.email,
        senha_hash=senha_hash,
        nome_completo=usuario.nome_completo,
        tipo_plano="gratuito",
        ativo=True,
    )
    
    db.add(novo_usuario)
    db.commit()
    db.refresh(novo_usuario)
    return novo_usuario


# ============================================================
# LOGIN
# ============================================================
@app.post("/api/login", response_model=schemas.Token)
def login(form_data: OAuth2PasswordRequestForm = Depends(), db: Session = Depends(get_db)):
    """Login de usuário"""
    usuario = autenticar_usuario(db, form_data.username, form_data.password)
    if not usuario:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="E-mail ou senha incorretos.",
            headers={"WWW-Authenticate": "Bearer"},
        )
    
    access_token = criar_token(
        data={"sub": usuario.email},
        expires_delta=timedelta(minutes=30)
    )
    return {"access_token": access_token, "token_type": "bearer"}


# ============================================================
# PERGUNTAS DS160 / ENTREVISTA (PÚBLICAS)
# ============================================================
@app.get("/api/perguntas-ds160", response_model=List[schemas.PerguntaDS160Resposta])
def listar_perguntas_ds160(gratuito: bool = None, categoria: str = None, db: Session = Depends(get_db)):
    query = db.query(models.PerguntaDS160)
    
    if gratuito is True:
        query = query.filter(models.PerguntaDS160.gratuita == True)  # CORRETO
    
    if categoria:
        query = query.filter(models.PerguntaDS160.categoria == categoria)
    
    return query.order_by(models.PerguntaDS160.ordem).all()


@app.get("/api/perguntas-entrevista", response_model=List[schemas.PerguntaEntrevistaResposta])
def listar_perguntas_entrevista(gratuito: bool = None, categoria: str = None, db: Session = Depends(get_db)):
    query = db.query(models.PerguntaEntrevista)
    
    if gratuito is True:
        query = query.filter(models.PerguntaEntrevista.gratuita == True)  # CORRETO
    
    if categoria:
        query = query.filter(models.PerguntaEntrevista.categoria == categoria)
    
    return query.order_by(models.PerguntaEntrevista.ordem).all()


@app.get("/api/perguntas/stats")
def estatisticas_perguntas(db: Session = Depends(get_db)):
    total_ds160 = db.query(models.PerguntaDS160).count()
    gratuitas_ds160 = db.query(models.PerguntaDS160).filter(models.PerguntaDS160.gratuita == True).count()
    
    total_entrevista = db.query(models.PerguntaEntrevista).count()
    gratuitas_entrevista = db.query(models.PerguntaEntrevista).filter(models.PerguntaEntrevista.gratuita == True).count()
    
    return {
        "ds160": {
            "total": total_ds160,
            "gratuitas": gratuitas_ds160,
            "premium": total_ds160 - gratuitas_ds160
        },
        "entrevista": {
            "total": total_entrevista,
            "gratuitas": gratuitas_entrevista,
            "premium": total_entrevista - gratuitas_entrevista
        },
        "total_geral": total_ds160 + total_entrevista
    }


# ============================================================
# AVALIAR RESPOSTAS
# ============================================================
@app.post("/api/avaliar")
def avaliar_respostas(
    dados: schemas.TentativaCriar,
    db: Session = Depends(get_db),
    current_user: models.Usuario = Depends(get_current_user)
):
    """
    Avalia as respostas do usuário e SALVA no banco de dados.
    CORRIGIDO: Agora salva tentativa e retorna tentativa_id!
    """
    respostas = dados.respostas
    
    # Inicializar pontuações por categoria
    pontuacao_categorias = {
        "vinculos_brasil": 0,
        "situacao_financeira": 0,
        "proposito_viagem": 0,
        "historico_viagens": 0,
        "perfil_pessoal": 0
    }
    
    total_perguntas = len(respostas)
    pontuacao_total = 0
    peso_total = 0
    
    # Avaliar cada resposta
    for resposta in respostas:
        if resposta.tipo_pergunta == "ds160":
            pergunta = db.query(models.PerguntaDS160).filter(
                models.PerguntaDS160.id == resposta.pergunta_id
            ).first()
        else:
            pergunta = db.query(models.PerguntaEntrevista).filter(
                models.PerguntaEntrevista.id == resposta.pergunta_id
            ).first()
        
        if not pergunta:
            continue
        
        # Calcular pontuação da resposta
        pontos = 0
        
        # Pontuação pela resposta (70% se respondeu substancialmente)
        if len(resposta.resposta_usuario) > 10:
            pontos = pergunta.peso_avaliacao * 0.7
        
        # Pontos de palavras positivas (se existir)
        if hasattr(pergunta, 'palavras_positivas') and pergunta.palavras_positivas:
            for palavra in pergunta.palavras_positivas:
                if palavra.lower() in resposta.resposta_usuario.lower():
                    pontos += 0.5
        
        pontuacao_total += pontos
        peso_total += pergunta.peso_avaliacao
        
        # Mapear categoria
        categoria_map = {
            "vinculos": "vinculos_brasil",
            "financeiro": "situacao_financeira",
            "viagem": "proposito_viagem",
            "pessoal": "perfil_pessoal",
            "historico": "historico_viagens"
        }
        
        categoria_key = categoria_map.get(pergunta.categoria.lower(), "perfil_pessoal")
        pontuacao_categorias[categoria_key] += pontos
    
    # Calcular pontuação geral (0-100)
    pontuacao_geral = (pontuacao_total / peso_total * 100) if peso_total > 0 else 0
    pontuacao_geral = min(100, pontuacao_geral)  # Limitar a 100
    
    # Determinar probabilidade
    if pontuacao_geral >= 70:
        probabilidade = "Alta"
    elif pontuacao_geral >= 50:
        probabilidade = "Média"
    else:
        probabilidade = "Baixa"
    
    # Identificar pontos fortes e fracos
    categorias_ordenadas = sorted(
        pontuacao_categorias.items(), 
        key=lambda x: x[1], 
        reverse=True
    )
    pontos_fortes = [cat[0].replace("_", " ").title() for cat in categorias_ordenadas[:2]]
    pontos_fracos = [cat[0].replace("_", " ").title() for cat in categorias_ordenadas[-2:]]
    
    # Gerar recomendações
    recomendacoes = []
    if pontuacao_geral < 70:
        recomendacoes.append("Fortaleça seus vínculos com o Brasil (emprego, família, propriedades)")
    if pontuacao_categorias["situacao_financeira"] < 50:
        recomendacoes.append("Organize documentos financeiros (extratos, IR, comprovantes)")
    if pontuacao_categorias["proposito_viagem"] < 50:
        recomendacoes.append("Deixe claro o propósito da viagem e planeje o roteiro detalhadamente")
    if pontuacao_categorias["historico_viagens"] < 50:
        recomendacoes.append("Se possível, viaje para outros países antes de solicitar o visto americano")
    
    if not recomendacoes:
        recomendacoes.append("Continue se preparando e revise suas respostas antes da entrevista")
    
    # ====== SALVAR NO BANCO DE DADOS ======
    from datetime import datetime
    
    # Criar registro da tentativa
    nova_tentativa = models.Tentativa(
        usuario_id=current_user.id,
        tipo=dados.tipo,
        data_tentativa=datetime.utcnow(),
        pontuacao_final=pontuacao_geral,
        pontuacao_categorias=pontuacao_categorias,
        probabilidade=probabilidade,
        tempo_gasto=0,  # Pode ser enviado do frontend
        completo=True
    )
    
    db.add(nova_tentativa)
    db.commit()
    db.refresh(nova_tentativa)
    
    # Salvar cada resposta individual
    for resposta in respostas:
        nova_resposta = models.Resposta(
            tentativa_id=nova_tentativa.id,
            pergunta_id=resposta.pergunta_id,
            tipo_pergunta=resposta.tipo_pergunta,
            resposta_usuario=resposta.resposta_usuario
        )
        db.add(nova_resposta)
    
    db.commit()
    # ====== FIM DA CORREÇÃO ======
    
    # Retornar resultado COM tentativa_id
    return {
        "tentativa_id": nova_tentativa.id,  # ← CAMPO CRÍTICO ADICIONADO!
        "pontuacao_geral": round(pontuacao_geral, 2),
        "probabilidade": probabilidade,
        "pontuacao_categorias": pontuacao_categorias,
        "pontos_fortes": pontos_fortes,
        "pontos_fracos": pontos_fracos,
        "recomendacoes": recomendacoes,
        "total_perguntas": total_perguntas,
        "perguntas_respondidas": total_perguntas
    }

@app.get("/api/usuarios/listar")
def listar_todos_usuarios(db: Session = Depends(get_db)):
    """Listar todos os usuários (apenas para debug/admin)"""
    usuarios = db.query(models.Usuario).all()
    
    resultado = []
    for user in usuarios:
        resultado.append({
            "id": user.id,
            "email": user.email,
            "nome": user.nome_completo,
            "plano": user.tipo_plano,
            "cadastro": user.data_cadastro.strftime("%d/%m/%Y %H:%M"),
            "premium_ate": user.data_expiracao_premium.strftime("%d/%m/%Y") if user.data_expiracao_premium else "Vitalício" if user.tipo_plano == "premium" else "N/A",
            "ativo": user.ativo
        })
    
    return {
        "total": len(usuarios),
        "usuarios": resultado
    }

@app.post("/api/usuarios/{usuario_id}/tornar-premium")
def tornar_premium(usuario_id: int, db: Session = Depends(get_db)):
    """Tornar usuário Premium (para testes manuais)"""
    usuario = db.query(models.Usuario).filter(models.Usuario.id == usuario_id).first()
    
    if not usuario:
        raise HTTPException(status_code=404, detail="Usuário não encontrado")
    
    usuario.tipo_plano = "premium"
    usuario.data_expiracao_premium = None  # Vitalício
    db.commit()
    
    return {
        "mensagem": "Usuário atualizado para Premium com sucesso!",
        "usuario": {
            "id": usuario.id,
            "email": usuario.email,
            "plano": usuario.tipo_plano
        }
    }

# ============================================================================
# SISTEMA DE RECUPERAÇÃO DE SENHA
# ============================================================================

from datetime import datetime, timedelta
import secrets
import hashlib

# Dicionário temporário para tokens (em produção, use Redis ou banco de dados)
tokens_recuperacao = {}

@app.post("/api/recuperar-senha/solicitar")
def solicitar_recuperacao_senha(email: str, db: Session = Depends(get_db)):
    """
    Solicitar recuperação de senha
    Envia email com link para resetar senha
    """
    # Buscar usuário
    usuario = db.query(models.Usuario).filter(models.Usuario.email == email).first()
    
    if not usuario:
        # Por segurança, não informar se o email existe ou não
        return {
            "mensagem": "Se o email existir, você receberá um link de recuperação.",
            "sucesso": True
        }
    
    # Gerar token único
    token = secrets.token_urlsafe(32)
    expiracao = datetime.utcnow() + timedelta(hours=1)  # Token válido por 1 hora
    
    # Armazenar token temporariamente
    tokens_recuperacao[token] = {
        "email": email,
        "expiracao": expiracao,
        "usado": False
    }
    
    # Em produção, envie email aqui
    # Para desenvolvimento, apenas retornar o link
    link_recuperacao = f"http://localhost:8080/recuperar-senha.html?token={token}"
    
    print("\n" + "="*70)
    print("📧 EMAIL DE RECUPERAÇÃO DE SENHA")
    print("="*70)
    print(f"Para: {email}")
    print(f"Link de recuperação (válido por 1 hora):")
    print(f"{link_recuperacao}")
    print("="*70 + "\n")
    
    return {
        "mensagem": "Se o email existir, você receberá um link de recuperação.",
        "sucesso": True,
        # Remover em produção (apenas para desenvolvimento)
        "debug_link": link_recuperacao
    }


@app.post("/api/recuperar-senha/validar-token")
def validar_token_recuperacao(token: str):
    """
    Validar se o token de recuperação é válido
    """
    if token not in tokens_recuperacao:
        raise HTTPException(status_code=400, detail="Token inválido ou expirado")
    
    token_info = tokens_recuperacao[token]
    
    # Verificar se já foi usado
    if token_info["usado"]:
        raise HTTPException(status_code=400, detail="Token já foi utilizado")
    
    # Verificar se expirou
    if datetime.utcnow() > token_info["expiracao"]:
        raise HTTPException(status_code=400, detail="Token expirado")
    
    return {
        "valido": True,
        "email": token_info["email"]
    }


@app.post("/api/recuperar-senha/resetar")
def resetar_senha(token: str, nova_senha: str, db: Session = Depends(get_db)):
    """
    Resetar senha usando token válido
    """
    # Validar token
    if token not in tokens_recuperacao:
        raise HTTPException(status_code=400, detail="Token inválido ou expirado")
    
    token_info = tokens_recuperacao[token]
    
    # Verificar se já foi usado
    if token_info["usado"]:
        raise HTTPException(status_code=400, detail="Token já foi utilizado")
    
    # Verificar se expirou
    if datetime.utcnow() > token_info["expiracao"]:
        raise HTTPException(status_code=400, detail="Token expirado")
    
    # Buscar usuário
    usuario = db.query(models.Usuario).filter(
        models.Usuario.email == token_info["email"]
    ).first()
    
    if not usuario:
        raise HTTPException(status_code=404, detail="Usuário não encontrado")
    
    # Validar nova senha
    if len(nova_senha) < 6:
        raise HTTPException(status_code=400, detail="Senha deve ter no mínimo 6 caracteres")
    
    # Atualizar senha
    usuario.senha_hash = gerar_hash_senha(nova_senha)
    db.commit()
    
    # Marcar token como usado
    tokens_recuperacao[token]["usado"] = True
    
    return {
        "mensagem": "Senha alterada com sucesso!",
        "sucesso": True
    }


# ============================================================================
# DASHBOARD DO USUÁRIO
# ============================================================================

@app.get("/api/dashboard")
def obter_dashboard(
    current_user: dict = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """
    Retorna dados do dashboard do usuário
    - Informações pessoais
    - Estatísticas
    - Histórico resumido
    - Status do plano
    """
    
    # Buscar usuário
    usuario = db.query(models.Usuario).filter(
        models.Usuario.email == current_user.email
    ).first()
    
    if not usuario:
        raise HTTPException(status_code=404, detail="Usuário não encontrado")
    
    # Buscar tentativas do usuário
    tentativas = db.query(models.Tentativa).filter(
        models.Tentativa.usuario_id == usuario.id
    ).order_by(models.Tentativa.data_tentativa.desc()).all()
    
    # Calcular estatísticas
    total_tentativas = len(tentativas)
    
    # Última tentativa
    ultima_tentativa = None
    if tentativas:
        ultima = tentativas[0]
        ultima_tentativa = {
            "data": ultima.data_tentativa.strftime("%d/%m/%Y %H:%M"),
            "tipo": ultima.tipo,
            "pontuacao": ultima.pontuacao_final,
            "probabilidade": ultima.probabilidade,
            "completo": ultima.completo
        }
    
    # Média de pontuação
    media_pontuacao = 0
    if tentativas:
        pontuacoes = [t.pontuacao_final for t in tentativas if t.pontuacao_final]
        if pontuacoes:
            media_pontuacao = sum(pontuacoes) / len(pontuacoes)
    
    # Melhor pontuação
    melhor_pontuacao = 0
    if tentativas:
        pontuacoes = [t.pontuacao_final for t in tentativas if t.pontuacao_final]
        if pontuacoes:
            melhor_pontuacao = max(pontuacoes)
    
    # Tempo total gasto (em minutos)
    tempo_total = sum([t.tempo_gasto for t in tentativas if t.tempo_gasto]) // 60
    
    # Evolução (últimas 5 tentativas)
    evolucao = []
    for t in tentativas[:5][::-1]:  # Inverter para ordem cronológica
        if t.pontuacao_final:
            evolucao.append({
                "data": t.data_tentativa.strftime("%d/%m"),
                "pontuacao": round(t.pontuacao_final, 1)
            })
    
    # Status do plano
    plano_info = {
        "tipo": usuario.tipo_plano,
        "ativo": usuario.ativo,
        "premium": usuario.tipo_plano == "premium",
        "data_cadastro": usuario.data_cadastro.strftime("%d/%m/%Y"),
        "expiracao": None
    }
    
    if usuario.data_expiracao_premium:
        plano_info["expiracao"] = usuario.data_expiracao_premium.strftime("%d/%m/%Y")
    
    # Contar perguntas disponíveis
    if usuario.tipo_plano == "premium":
        perguntas_disponiveis = 90
    else:
        perguntas_disponiveis = 25
    
    return {
        "usuario": {
            "id": usuario.id,
            "nome": usuario.nome_completo,
            "email": usuario.email,
            "ativo": usuario.ativo
        },
        "plano": plano_info,
        "estatisticas": {
            "total_tentativas": total_tentativas,
            "media_pontuacao": round(media_pontuacao, 1),
            "melhor_pontuacao": round(melhor_pontuacao, 1),
            "tempo_total_minutos": tempo_total,
            "perguntas_disponiveis": perguntas_disponiveis
        },
        "ultima_tentativa": ultima_tentativa,
        "evolucao": evolucao
    }


# ============================================================================
# HISTÓRICO DE TENTATIVAS
# ============================================================================

@app.get("/api/historico")
def listar_historico(
    current_user: dict = Depends(get_current_user),
    db: Session = Depends(get_db),
    limite: int = 50,
    tipo: str = None
):
    """
    Listar histórico completo de tentativas do usuário
    - Parâmetros opcionais: limite, tipo (ds160/entrevista)
    """
    
    # Buscar usuário
    usuario = db.query(models.Usuario).filter(
        models.Usuario.email == current_user.email
    ).first()
    
    if not usuario:
        raise HTTPException(status_code=404, detail="Usuário não encontrado")
    
    # Query base
    query = db.query(models.Tentativa).filter(
        models.Tentativa.usuario_id == usuario.id
    )
    
    # Filtrar por tipo se especificado
    if tipo:
        query = query.filter(models.Tentativa.tipo == tipo)
    
    # Ordenar por data (mais recente primeiro) e aplicar limite
    tentativas = query.order_by(
        models.Tentativa.data_tentativa.desc()
    ).limit(limite).all()
    
    # Formatar resultado
    historico = []
    for t in tentativas:
        historico.append({
            "id": t.id,
            "data": t.data_tentativa.strftime("%d/%m/%Y"),
            "hora": t.data_tentativa.strftime("%H:%M"),
            "data_completa": t.data_tentativa.strftime("%d/%m/%Y %H:%M"),
            "tipo": t.tipo,
            "tipo_formatado": "DS-160" if t.tipo == "ds160" else "Entrevista Consular",
            "pontuacao": round(t.pontuacao_final, 1) if t.pontuacao_final else 0,
            "probabilidade": t.probabilidade,
            "completo": t.completo,
            "tempo_gasto": t.tempo_gasto // 60 if t.tempo_gasto else 0,  # em minutos
            "pontuacao_categorias": t.pontuacao_categorias
        })
    
    return {
        "total": len(historico),
        "tentativas": historico,
        "usuario": {
            "nome": usuario.nome_completo,
            "plano": usuario.tipo_plano
        }
    }


@app.get("/api/historico/{tentativa_id}")
def detalhe_tentativa(
    tentativa_id: int,
    current_user: dict = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """
    Obter detalhes completos de uma tentativa específica
    Inclui todas as respostas dadas pelo usuário
    """
    
    # Buscar usuário
    usuario = db.query(models.Usuario).filter(
        models.Usuario.email == current_user.email
    ).first()
    
    if not usuario:
        raise HTTPException(status_code=404, detail="Usuário não encontrado")
    
    # Buscar tentativa
    tentativa = db.query(models.Tentativa).filter(
        models.Tentativa.id == tentativa_id,
        models.Tentativa.usuario_id == usuario.id
    ).first()
    
    if not tentativa:
        raise HTTPException(status_code=404, detail="Tentativa não encontrada")
    
    # Buscar respostas da tentativa
    respostas = db.query(models.Resposta).filter(
        models.Resposta.tentativa_id == tentativa_id
    ).all()
    
    # Formatar respostas
    respostas_formatadas = []
    for r in respostas:
        # Buscar pergunta correspondente
        if r.tipo_pergunta == "ds160":
            pergunta = db.query(models.PerguntaDS160).filter(
                models.PerguntaDS160.id == r.pergunta_id
            ).first()
        else:
            pergunta = db.query(models.PerguntaEntrevista).filter(
                models.PerguntaEntrevista.id == r.pergunta_id
            ).first()
        
        respostas_formatadas.append({
            "id": r.id,
            "pergunta_id": r.pergunta_id,
            "pergunta_texto": pergunta.pergunta_texto if pergunta else "Pergunta não encontrada",
            "resposta_usuario": r.resposta_usuario,
            "pontos_obtidos": r.pontos_obtidos,
            "feedback": r.feedback,
            "tipo_pergunta": r.tipo_pergunta
        })
    
    # Formatar tentativa completa
    return {
        "id": tentativa.id,
        "data": tentativa.data_tentativa.strftime("%d/%m/%Y %H:%M"),
        "tipo": tentativa.tipo,
        "tipo_formatado": "DS-160" if tentativa.tipo == "ds160" else "Entrevista Consular",
        "pontuacao_final": round(tentativa.pontuacao_final, 1) if tentativa.pontuacao_final else 0,
        "probabilidade": tentativa.probabilidade,
        "completo": tentativa.completo,
        "tempo_gasto": tentativa.tempo_gasto // 60 if tentativa.tempo_gasto else 0,
        "pontuacao_categorias": tentativa.pontuacao_categorias,
        "total_respostas": len(respostas_formatadas),
        "respostas": respostas_formatadas
    }


@app.delete("/api/historico/{tentativa_id}")
def deletar_tentativa(
    tentativa_id: int,
    current_user: dict = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """
    Deletar uma tentativa específica do histórico
    """
    
    # Buscar usuário
    usuario = db.query(models.Usuario).filter(
        models.Usuario.email == current_user.email
    ).first()
    
    if not usuario:
        raise HTTPException(status_code=404, detail="Usuário não encontrado")
    
    # Buscar tentativa
    tentativa = db.query(models.Tentativa).filter(
        models.Tentativa.id == tentativa_id,
        models.Tentativa.usuario_id == usuario.id
    ).first()
    
    if not tentativa:
        raise HTTPException(status_code=404, detail="Tentativa não encontrada")
    
    # Deletar respostas associadas
    db.query(models.Resposta).filter(
        models.Resposta.tentativa_id == tentativa_id
    ).delete()
    
    # Deletar tentativa
    db.delete(tentativa)
    db.commit()
    
    return {
        "mensagem": "Tentativa deletada com sucesso",
        "tentativa_id": tentativa_id
    }


@app.get("/api/historico/estatisticas/comparacao")
def comparar_tentativas(
    current_user: dict = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """
    Comparar estatísticas entre todas as tentativas
    Útil para visualizar evolução ao longo do tempo
    """
    
    # Buscar usuário
    usuario = db.query(models.Usuario).filter(
        models.Usuario.email == current_user.email
    ).first()
    
    if not usuario:
        raise HTTPException(status_code=404, detail="Usuário não encontrado")
    
    # Buscar todas as tentativas
    tentativas = db.query(models.Tentativa).filter(
        models.Tentativa.usuario_id == usuario.id
    ).order_by(models.Tentativa.data_tentativa.asc()).all()
    
    if not tentativas:
        return {
            "mensagem": "Nenhuma tentativa encontrada",
            "total": 0,
            "evolucao": []
        }
    
    # Análise de evolução
    evolucao = []
    for t in tentativas:
        evolucao.append({
            "data": t.data_tentativa.strftime("%d/%m/%Y"),
            "pontuacao": round(t.pontuacao_final, 1) if t.pontuacao_final else 0,
            "probabilidade": t.probabilidade,
            "tipo": t.tipo
        })
    
    # Calcular estatísticas gerais
    pontuacoes = [t.pontuacao_final for t in tentativas if t.pontuacao_final]
    
    if pontuacoes:
        media = sum(pontuacoes) / len(pontuacoes)
        melhor = max(pontuacoes)
        pior = min(pontuacoes)
        
        # Calcular tendência (primeira vs última)
        if len(pontuacoes) > 1:
            primeira_pontuacao = pontuacoes[0]
            ultima_pontuacao = pontuacoes[-1]
            diferenca = ultima_pontuacao - primeira_pontuacao
            
            if diferenca > 0:
                tendencia = "melhorando"
            elif diferenca < 0:
                tendencia = "piorando"
            else:
                tendencia = "estável"
        else:
            tendencia = "insuficiente"
            diferenca = 0
    else:
        media = 0
        melhor = 0
        pior = 0
        tendencia = "sem dados"
        diferenca = 0
    
    return {
        "total": len(tentativas),
        "evolucao": evolucao,
        "estatisticas": {
            "media": round(media, 1),
            "melhor_pontuacao": round(melhor, 1),
            "pior_pontuacao": round(pior, 1),
            "tendencia": tendencia,
            "diferenca": round(diferenca, 1)
        }
    }


# ============================================================================
# EXPORTAR PDF
# ============================================================================

from fastapi.responses import StreamingResponse
from io import BytesIO
from reportlab.lib.pagesizes import letter
from reportlab.lib import colors
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.lib.units import inch
from reportlab.platypus import SimpleDocTemplate, Table, TableStyle, Paragraph, Spacer
from reportlab.lib.enums import TA_CENTER, TA_LEFT

@app.get("/api/resultado/{tentativa_id}/pdf")
async def exportar_pdf(
    tentativa_id: int,
    current_user: models.Usuario = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """
    Exportar resultado de uma tentativa em PDF
    """
    
    # Buscar tentativa
    tentativa = db.query(models.Tentativa).filter(
        models.Tentativa.id == tentativa_id,
        models.Tentativa.usuario_id == current_user.id
    ).first()
    
    if not tentativa:
        raise HTTPException(status_code=404, detail="Tentativa não encontrada")
    
    # Criar PDF em memória
    buffer = BytesIO()
    doc = SimpleDocTemplate(buffer, pagesize=letter, topMargin=0.5*inch, bottomMargin=0.5*inch)
    
    # Elementos do PDF
    elements = []
    styles = getSampleStyleSheet()
    
    # Estilo customizado para título
    title_style = ParagraphStyle(
        'CustomTitle',
        parent=styles['Heading1'],
        fontSize=24,
        textColor=colors.HexColor('#1e40af'),
        spaceAfter=30,
        alignment=TA_CENTER,
        fontName='Helvetica-Bold'
    )
    
    # Estilo para subtítulo
    subtitle_style = ParagraphStyle(
        'Subtitle',
        parent=styles['Heading2'],
        fontSize=16,
        textColor=colors.HexColor('#3b82f6'),
        spaceAfter=12,
        fontName='Helvetica-Bold'
    )
    
    # Estilo para texto normal
    normal_style = ParagraphStyle(
        'CustomNormal',
        parent=styles['Normal'],
        fontSize=11,
        spaceAfter=6
    )
    
    # ===== HEADER =====
    elements.append(Paragraph("RELATÓRIO DE ANÁLISE - VISTO AMERICANO", title_style))
    elements.append(Paragraph("Preparação para Visto Americano", subtitle_style))
    elements.append(Spacer(1, 0.3*inch))
    
    # ===== INFORMAÇÕES GERAIS =====
    info_data = [
        ['Data da Simulação:', tentativa.data_tentativa.strftime("%d/%m/%Y %H:%M")],
        ['Tipo:', 'DS-160' if tentativa.tipo == 'ds160' else 'Entrevista Consular'],
        ['Usuário:', current_user.nome_completo],
        ['Plano:', current_user.tipo_plano.upper()]
    ]
    
    info_table = Table(info_data, colWidths=[2*inch, 4*inch])
    info_table.setStyle(TableStyle([
        ('BACKGROUND', (0, 0), (0, -1), colors.HexColor('#e5e7eb')),
        ('TEXTCOLOR', (0, 0), (-1, -1), colors.black),
        ('ALIGN', (0, 0), (-1, -1), 'LEFT'),
        ('FONTNAME', (0, 0), (0, -1), 'Helvetica-Bold'),
        ('FONTSIZE', (0, 0), (-1, -1), 10),
        ('BOTTOMPADDING', (0, 0), (-1, -1), 8),
        ('TOPPADDING', (0, 0), (-1, -1), 8),
        ('GRID', (0, 0), (-1, -1), 1, colors.HexColor('#d1d5db'))
    ]))
    
    elements.append(info_table)
    elements.append(Spacer(1, 0.3*inch))
    
    # ===== RESULTADO PRINCIPAL =====
    elements.append(Paragraph("RESULTADO DA ANÁLISE", subtitle_style))
    
    # Determinar cor baseado na probabilidade
    if tentativa.probabilidade == 'Alta':
        prob_color = colors.HexColor('#10b981')
        prob_emoji = 'ALTA'
    elif tentativa.probabilidade == 'Média':
        prob_color = colors.HexColor('#f59e0b')
        prob_emoji = 'MÉDIA'
    else:
        prob_color = colors.HexColor('#ef4444')
        prob_emoji = 'BAIXA'
    
    resultado_data = [
        ['Pontuação Final:', f"{round(tentativa.pontuacao_final, 1)}%"],
        ['Probabilidade de Aprovação:', f"{prob_emoji}"],
        ['Tempo Gasto:', f"{tentativa.tempo_gasto // 60} minutos"]
    ]
    
    resultado_table = Table(resultado_data, colWidths=[3*inch, 3*inch])
    resultado_table.setStyle(TableStyle([
        ('BACKGROUND', (0, 0), (-1, -1), colors.HexColor('#f3f4f6')),
        ('TEXTCOLOR', (0, 0), (0, -1), colors.black),
        ('TEXTCOLOR', (1, 0), (1, 0), colors.HexColor('#1e40af')),
        ('TEXTCOLOR', (1, 1), (1, 1), prob_color),
        ('ALIGN', (0, 0), (-1, -1), 'LEFT'),
        ('FONTNAME', (0, 0), (0, -1), 'Helvetica-Bold'),
        ('FONTNAME', (1, 0), (1, 0), 'Helvetica-Bold'),
        ('FONTSIZE', (0, 0), (-1, -1), 12),
        ('BOTTOMPADDING', (0, 0), (-1, -1), 10),
        ('TOPPADDING', (0, 0), (-1, -1), 10),
        ('GRID', (0, 0), (-1, -1), 1.5, colors.HexColor('#d1d5db'))
    ]))
    
    elements.append(resultado_table)
    elements.append(Spacer(1, 0.3*inch))
    
    # ===== PONTUAÇÃO POR CATEGORIA =====
    if tentativa.pontuacao_categorias:
        elements.append(Paragraph("PONTUAÇÃO POR CATEGORIA", subtitle_style))
        
        categorias_data = [['Categoria', 'Pontuação']]
        for categoria, pontos in tentativa.pontuacao_categorias.items():
            cat_nome = categoria.replace('_', ' ').title()
            categorias_data.append([cat_nome, f"{round(pontos, 1)} pts"])
        
        cat_table = Table(categorias_data, colWidths=[4*inch, 2*inch])
        cat_table.setStyle(TableStyle([
            ('BACKGROUND', (0, 0), (-1, 0), colors.HexColor('#3b82f6')),
            ('TEXTCOLOR', (0, 0), (-1, 0), colors.whitesmoke),
            ('ALIGN', (0, 0), (-1, -1), 'LEFT'),
            ('ALIGN', (1, 0), (1, -1), 'CENTER'),
            ('FONTNAME', (0, 0), (-1, 0), 'Helvetica-Bold'),
            ('FONTSIZE', (0, 0), (-1, 0), 11),
            ('BOTTOMPADDING', (0, 0), (-1, -1), 8),
            ('TOPPADDING', (0, 0), (-1, -1), 8),
            ('BACKGROUND', (0, 1), (-1, -1), colors.white),
            ('GRID', (0, 0), (-1, -1), 1, colors.HexColor('#d1d5db')),
            ('ROWBACKGROUNDS', (0, 1), (-1, -1), [colors.white, colors.HexColor('#f9fafb')])
        ]))
        
        elements.append(cat_table)
        elements.append(Spacer(1, 0.3*inch))
    
    # ===== ANÁLISE QUALITATIVA =====
    elements.append(Paragraph("ANÁLISE QUALITATIVA", subtitle_style))
    
    # Pontos Fortes
    if tentativa.pontuacao_categorias:
        categorias_ordenadas = sorted(
            tentativa.pontuacao_categorias.items(), 
            key=lambda x: x[1], 
            reverse=True
        )
        pontos_fortes = [cat[0].replace('_', ' ').title() for cat in categorias_ordenadas[:2]]
        pontos_fracos = [cat[0].replace('_', ' ').title() for cat in categorias_ordenadas[-2:]]
        
        elements.append(Paragraph("<b>Pontos Fortes:</b>", normal_style))
        for pf in pontos_fortes:
            elements.append(Paragraph(f"  • {pf}", normal_style))
        
        elements.append(Spacer(1, 0.1*inch))
        
        elements.append(Paragraph("<b>Áreas de Melhoria:</b>", normal_style))
        for pf in pontos_fracos:
            elements.append(Paragraph(f"  • {pf}", normal_style))
        
        elements.append(Spacer(1, 0.2*inch))
    
    # ===== RECOMENDAÇÕES =====
    elements.append(Paragraph("RECOMENDAÇÕES", subtitle_style))
    
    recomendacoes = []
    pontuacao = tentativa.pontuacao_final
    
    if pontuacao < 70:
        recomendacoes.append("Fortaleça seus vínculos com o Brasil (emprego estável, família, propriedades)")
    if pontuacao < 50:
        recomendacoes.append("Organize e prepare toda documentação financeira com antecedência")
        recomendacoes.append("Considere melhorar seu histórico de viagens internacionais")
    if tentativa.pontuacao_categorias:
        if tentativa.pontuacao_categorias.get('situacao_financeira', 0) < 50:
            recomendacoes.append("Prepare extratos bancários, declaração de IR e comprovantes de renda")
    
    recomendacoes.append("Pratique suas respostas mantendo clareza e objetividade")
    recomendacoes.append("Leve todos os documentos originais para a entrevista")
    recomendacoes.append("Seja honesto e confiante durante a entrevista")
    
    for rec in recomendacoes:
        elements.append(Paragraph(f"  • {rec}", normal_style))
    
    elements.append(Spacer(1, 0.3*inch))
    
    # ===== FOOTER =====
    elements.append(Spacer(1, 0.5*inch))
    footer_style = ParagraphStyle(
        'Footer',
        parent=styles['Normal'],
        fontSize=8,
        textColor=colors.grey,
        alignment=TA_CENTER
    )
    
    elements.append(Paragraph(
        "Este relatório é uma ferramenta de preparação e não garante a aprovação do visto.<br/>"
        "A decisão final é exclusiva do oficial consular.<br/><br/>"
        "© 2025 Sistema de Preparação para Visto Americano",
        footer_style
    ))
    
    # Construir PDF
    doc.build(elements)
    
    # Preparar resposta
    buffer.seek(0)
    filename = f"resultado_visto_{tentativa_id}_{tentativa.data_tentativa.strftime('%Y%m%d')}.pdf"
    
    return StreamingResponse(
        buffer,
        media_type="application/pdf",
        headers={
            "Content-Disposition": f"attachment; filename={filename}"
        }
    )

# ============================================================================
# STRIPE WEBHOOK
# ============================================================================

@app.post("/api/webhook/stripe")
async def stripe_webhook(request: Request, db: Session = Depends(get_db)):
    """Webhook do Stripe para atualizar plano após pagamento"""
    payload = await request.body()
    sig_header = request.headers.get('stripe-signature')
    
    try:
        import stripe
        stripe.api_key = os.getenv('STRIPE_SECRET_KEY')
        webhook_secret = os.getenv('STRIPE_WEBHOOK_SECRET')
        
        event = stripe.Webhook.construct_event(
            payload, sig_header, webhook_secret
        )
        
        # Processar evento de pagamento
        if event['type'] == 'checkout.session.completed':
            session = event['data']['object']
            customer_email = session.get('customer_details', {}).get('email')
            
            if customer_email:
                # Atualizar usuário para premium
                usuario = db.query(models.Usuario).filter(
                    models.Usuario.email == customer_email
                ).first()
                
                if usuario:
                    usuario.tipo_plano = 'premium'
                    db.commit()
                    print(f"✅ Usuário {customer_email} atualizado para Premium via webhook!")
        
        return {"status": "success"}
        
    except Exception as e:
        print(f"❌ Erro no webhook: {str(e)}")
        raise HTTPException(status_code=400, detail=str(e))
# ============================================================================
# FIM DO CÓDIGO
# ============================================================================

if __name__ == "__main__":
    uvicorn.run("app.main:app", host="0.0.0.0", port=8000, reload=True)