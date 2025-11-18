from sqlalchemy.orm import Session
from datetime import datetime
from app import models
from app.schemas import TentativaCriar

def avaliar_respostas(db: Session, current_user, dados: TentativaCriar):
    respostas = dados.respostas
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

    for resposta in respostas:
        if resposta.tipo_pergunta == "ds160":
            pergunta = db.query(models.PerguntaDS160).filter(models.PerguntaDS160.id == resposta.pergunta_id).first()
        else:
            pergunta = db.query(models.PerguntaEntrevista).filter(models.PerguntaEntrevista.id == resposta.pergunta_id).first()
        if not pergunta:
            continue
        pontos = 0
        if len(resposta.resposta_usuario) > 10:
            pontos = pergunta.peso_avaliacao * 0.7
        if getattr(pergunta, "palavras_positivas", None):
            for palavra in pergunta.palavras_positivas:
                if palavra.lower() in resposta.resposta_usuario.lower():
                    pontos += 0.5
        pontuacao_total += pontos
        peso_total += pergunta.peso_avaliacao
        categoria_map = {
            "vinculos": "vinculos_brasil",
            "financeiro": "situacao_financeira",
            "viagem": "proposito_viagem",
            "pessoal": "perfil_pessoal",
            "historico": "historico_viagens"
        }
        categoria_key = categoria_map.get(pergunta.categoria.lower(), "perfil_pessoal")
        pontuacao_categorias[categoria_key] += pontos

    pontuacao_geral = (pontuacao_total / peso_total * 100) if peso_total > 0 else 0
    pontuacao_geral = min(100, pontuacao_geral)

    if pontuacao_geral >= 70:
        probabilidade = "Alta"
    elif pontuacao_geral >= 50:
        probabilidade = "Média"
    else:
        probabilidade = "Baixa"

    categorias_ordenadas = sorted(pontuacao_categorias.items(), key=lambda x: x[1], reverse=True)
    pontos_fortes = [cat[0].replace("_", " ").title() for cat in categorias_ordenadas[:2]]
    pontos_fracos = [cat[0].replace("_", " ").title() for cat in categorias_ordenadas[-2:]]

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

    nova_tentativa = models.Tentativa(
        usuario_id=current_user.id,
        tipo=dados.tipo,
        data_tentativa=datetime.utcnow(),
        pontuacao_final=pontuacao_geral,
        pontuacao_categorias=pontuacao_categorias,
        probabilidade=probabilidade,
        tempo_gasto=0,
        completo=True
    )
    db.add(nova_tentativa)
    db.commit()
    db.refresh(nova_tentativa)

    for resposta in respostas:
        nova_resposta = models.Resposta(
            tentativa_id=nova_tentativa.id,
            pergunta_id=resposta.pergunta_id,
            tipo_pergunta=resposta.tipo_pergunta,
            resposta_usuario=resposta.resposta_usuario
        )
        db.add(nova_resposta)
    db.commit()

    return {
        "tentativa_id": nova_tentativa.id,
        "pontuacao_geral": round(pontuacao_geral, 2),
        "probabilidade": probabilidade,
        "pontuacao_categorias": pontuacao_categorias,
        "pontos_fortes": pontos_fortes,
        "pontos_fracos": pontos_fracos,
        "recomendacoes": recomendacoes,
        "total_perguntas": total_perguntas,
        "perguntas_respondidas": total_perguntas
    }

def listar_historico(db: Session, current_user, limite: int = 50, tipo: str = None):
    usuario = db.query(models.Usuario).filter(models.Usuario.email == current_user.email).first()
    if not usuario:
        return {"total": 0, "tentativas": []}
    query = db.query(models.Tentativa).filter(models.Tentativa.usuario_id == usuario.id)
    if tipo:
        query = query.filter(models.Tentativa.tipo == tipo)
    tentativas = query.order_by(models.Tentativa.data_tentativa.desc()).limit(limite).all()
    resultado = []
    for t in tentativas:
        resultado.append({
            "id": t.id,
            "data": t.data_tentativa.strftime("%d/%m/%Y"),
            "hora": t.data_tentativa.strftime("%H:%M"),
            "data_completa": t.data_tentativa.strftime("%d/%m/%Y %H:%M"),
            "tipo": t.tipo,
            "pontuacao": round(t.pontuacao_final, 1) if t.pontuacao_final else 0,
            "probabilidade": t.probabilidade,
            "completo": t.completo,
            "tempo_gasto": t.tempo_gasto // 60 if t.tempo_gasto else 0,
            "pontuacao_categorias": t.pontuacao_categorias
        })
    return {"total": len(resultado), "tentativas": resultado}

def detalhe_tentativa(db: Session, current_user, tentativa_id: int):
    usuario = db.query(models.Usuario).filter(models.Usuario.email == current_user.email).first()
    if not usuario:
        return None
    tentativa = db.query(models.Tentativa).filter(models.Tentativa.id == tentativa_id, models.Tentativa.usuario_id == usuario.id).first()
    if not tentativa:
        return None
    respostas = db.query(models.Resposta).filter(models.Resposta.tentativa_id == tentativa_id).all()
    respostas_formatadas = []
    for r in respostas:
        if r.tipo_pergunta == "ds160":
            pergunta = db.query(models.PerguntaDS160).filter(models.PerguntaDS160.id == r.pergunta_id).first()
        else:
            pergunta = db.query(models.PerguntaEntrevista).filter(models.PerguntaEntrevista.id == r.pergunta_id).first()
        respostas_formatadas.append({
            "id": r.id,
            "pergunta_id": r.pergunta_id,
            "pergunta_texto": pergunta.pergunta_texto if pergunta else "Pergunta não encontrada",
            "resposta_usuario": r.resposta_usuario,
            "pontos_obtidos": r.pontos_obtidos,
            "feedback": r.feedback,
            "tipo_pergunta": r.tipo_pergunta
        })
    return {
        "id": tentativa.id,
        "data": tentativa.data_tentativa.strftime("%d/%m/%Y %H:%M"),
        "tipo": tentativa.tipo,
        "pontuacao_final": round(tentativa.pontuacao_final, 1) if tentativa.pontuacao_final else 0,
        "probabilidade": tentativa.probabilidade,
        "completo": tentativa.completo,
        "tempo_gasto": tentativa.tempo_gasto // 60 if tentativa.tempo_gasto else 0,
        "pontuacao_categorias": tentativa.pontuacao_categorias,
        "total_respostas": len(respostas_formatadas),
        "respostas": respostas_formatadas
    }

def deletar_tentativa(db: Session, current_user, tentativa_id: int):
    usuario = db.query(models.Usuario).filter(models.Usuario.email == current_user.email).first()
    if not usuario:
        return {"mensagem": "Usuário não encontrado"}
    tentativa = db.query(models.Tentativa).filter(models.Tentativa.id == tentativa_id, models.Tentativa.usuario_id == usuario.id).first()
    if not tentativa:
        return {"mensagem": "Tentativa não encontrada"}
    db.query(models.Resposta).filter(models.Resposta.tentativa_id == tentativa_id).delete()
    db.delete(tentativa)
    db.commit()
    return {"mensagem": "Tentativa deletada com sucesso", "tentativa_id": tentativa_id}

def comparar_tentativas(db: Session, current_user):
    usuario = db.query(models.Usuario).filter(models.Usuario.email == current_user.email).first()
    if not usuario:
        return {"total": 0, "evolucao": []}
    tentativas = db.query(models.Tentativa).filter(models.Tentativa.usuario_id == usuario.id).order_by(models.Tentativa.data_tentativa.asc()).all()
    evolucao = []
    for t in tentativas:
        evolucao.append({
            "data": t.data_tentativa.strftime("%d/%m/%Y"),
            "pontuacao": round(t.pontuacao_final, 1) if t.pontuacao_final else 0,
            "probabilidade": t.probabilidade,
            "tipo": t.tipo
        })
    pontuacoes = [t.pontuacao_final for t in tentativas if t.pontuacao_final]
    if pontuacoes:
        media = sum(pontuacoes) / len(pontuacoes)
        melhor = max(pontuacoes)
        pior = min(pontuacoes)
        if len(pontuacoes) > 1:
            diferenca = pontuacoes[-1] - pontuacoes[0]
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
