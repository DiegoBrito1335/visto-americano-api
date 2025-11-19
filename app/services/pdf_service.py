from io import BytesIO
from datetime import datetime
from fastapi.responses import StreamingResponse
from sqlalchemy.orm import Session

from reportlab.lib.pagesizes import letter
from reportlab.lib import colors
from reportlab.lib.enums import TA_CENTER
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.platypus import (
    SimpleDocTemplate, Table, TableStyle, Paragraph, Spacer
)

from app import models


class PDFService:

    @staticmethod
    def gerar_pdf_tentativa(db: Session, tentativa_id: int, usuario: models.Usuario):
        """
        Gera o PDF completo da tentativa, com pontuação, categorias,
        recomendações e respostas detalhadas.
        """

        tentativa = db.query(models.Tentativa).filter(
            models.Tentativa.id == tentativa_id,
            models.Tentativa.usuario_id == usuario.id
        ).first()

        if not tentativa:
            return None

        # Buscar respostas
        respostas = db.query(models.Resposta).filter(
            models.Resposta.tentativa_id == tentativa_id
        ).all()

        # Tipo formatado
        tipos_map = {
            "ds160": "DS-160 (Formulário)",
            "entrevista": "Entrevista Consular",
            "completo": "Simulação Completa"
        }
        tipo_formatado = tipos_map.get(tentativa.tipo, tentativa.tipo)

        buffer = BytesIO()
        doc = SimpleDocTemplate(buffer, pagesize=letter, topMargin=40, bottomMargin=40)

        styles = getSampleStyleSheet()
        elements = []

        # --- Estilos ----
        title_style = ParagraphStyle(
            "Title",
            parent=styles["Heading1"],
            alignment=TA_CENTER,
            fontSize=22,
            textColor=colors.HexColor("#1e40af"),
            spaceAfter=20,
        )

        subtitle_style = ParagraphStyle(
            "Subtitle",
            parent=styles["Heading2"],
            fontSize=14,
            textColor=colors.HexColor("#3b82f6"),
            spaceAfter=10,
        )

        normal = styles["Normal"]

        # Header
        elements.append(Paragraph("RELATÓRIO DE ANÁLISE - VISTO AMERICANO", title_style))
        elements.append(Spacer(1, 15))

        # ------------------------------------------------------------
        # INFO DO USUÁRIO
        # ------------------------------------------------------------
        elements.append(Paragraph("INFORMAÇÕES DO USUÁRIO", subtitle_style))

        info = [
            ["Nome:", usuario.nome_completo],
            ["Email:", usuario.email],
            ["Plano:", usuario.tipo_plano.upper()],
            ["Data da Tentativa:", tentativa.data_tentativa.strftime("%d/%m/%Y %H:%M")],
            ["Tipo da Simulação:", tipo_formatado],
        ]

        info_table = Table(info, colWidths=[150, 340])
        info_table.setStyle(TableStyle([
            ("BACKGROUND", (0, 0), (0, -1), colors.lightgrey),
            ("FONTNAME", (0, 0), (-1, -1), "Helvetica"),
            ("GRID", (0, 0), (-1, -1), 0.4, colors.grey),
        ]))

        elements.append(info_table)
        elements.append(Spacer(1, 20))

        # ------------------------------------------------------------
        # RESULTADO
        # ------------------------------------------------------------
        elements.append(Paragraph("RESULTADO GERAL", subtitle_style))

        cor_prob = (
            colors.green if tentativa.probabilidade == "Alta" else
            colors.orange if tentativa.probabilidade == "Média" else
            colors.red
        )

        resultado = [
            ["Pontuação:", f"{tentativa.pontuacao_final:.1f}%"],
            ["Probabilidade:", tentativa.probabilidade],
            ["Tempo Total:", f"{tentativa.tempo_gasto // 60} min"],
        ]

        res_table = Table(resultado, colWidths=[150, 340])
        res_table.setStyle(TableStyle([
            ("BACKGROUND", (0, 0), (-1, -1), colors.HexColor("#f3f4f6")),
            ("TEXTCOLOR", (1, 1), (1, 1), cor_prob),
            ("GRID", (0, 0), (-1, -1), 0.4, colors.grey),
        ]))
        elements.append(res_table)
        elements.append(Spacer(1, 20))

        # ------------------------------------------------------------
        # PONTUAÇÃO POR CATEGORIA
        # ------------------------------------------------------------
        if tentativa.pontuacao_categorias:
            elements.append(Paragraph("PONTUAÇÃO POR CATEGORIA", subtitle_style))

            header = ["Categoria", "Pontuação"]
            rows = [header]

            for cat, pts in tentativa.pontuacao_categorias.items():
                rows.append([cat.replace("_", " ").title(), f"{pts:.1f}"])

            table = Table(rows, colWidths=[260, 230])
            table.setStyle(TableStyle([
                ("BACKGROUND", (0, 0), (-1, 0), colors.HexColor("#3b82f6")),
                ("TEXTCOLOR", (0, 0), (-1, 0), colors.white),
                ("GRID", (0, 0), (-1, -1), 0.4, colors.grey),
                ("ROWBACKGROUNDS", (0, 1), (-1, -1), [colors.white, colors.HexColor("#f9fafb")]),
            ]))

            elements.append(table)
            elements.append(Spacer(1, 20))

        # ------------------------------------------------------------
        # RECOMENDAÇÕES REAIS
        # ------------------------------------------------------------
        if tentativa.pontuacao_categorias:
            elements.append(Paragraph("RECOMENDAÇÕES", subtitle_style))

            # Recomendações geradas pelo TentativasService
            recs = PDFService._gerar_recomendacoes(tentativa)

            for r in recs:
                elements.append(Paragraph(f"• {r}", normal))

            elements.append(Spacer(1, 20))

        # ------------------------------------------------------------
        # RESPOSTAS DETALHADAS
        # ------------------------------------------------------------
        if respostas:
            elements.append(Paragraph("RESPOSTAS DETALHADAS", subtitle_style))

            for r in respostas:
                pergunta = None

                if r.tipo_pergunta == "ds160":
                    pergunta = db.query(models.PerguntaDS160).filter(
                        models.PerguntaDS160.id == r.pergunta_id
                    ).first()
                else:
                    pergunta = db.query(models.PerguntaEntrevista).filter(
                        models.PerguntaEntrevista.id == r.pergunta_id
                    ).first()

                texto = pergunta.pergunta_texto if pergunta else "Pergunta não encontrada"

                elements.append(Paragraph(f"<b>{texto}</b>", normal))
                elements.append(Paragraph(r.resposta_usuario, normal))
                elements.append(Spacer(1, 12))

        # ------------------------------------------------------------
        # FOOTER
        # ------------------------------------------------------------
        footer = Paragraph(
            "Este relatório é um auxílio e NÃO garante aprovação do visto.",
            ParagraphStyle("Footer", alignment=TA_CENTER, fontSize=8, textColor=colors.grey),
        )
        elements.append(footer)

        doc.build(elements)
        buffer.seek(0)

        filename = f"analise_tentativa_{tentativa.tipo}_{tentativa.id}.pdf"

        return StreamingResponse(
            buffer,
            media_type="application/pdf",
            headers={"Content-Disposition": f"attachment; filename={filename}"}
        )

    @staticmethod
    def _gerar_recomendacoes(tentativa: models.Tentativa):
        """
        Gera recomendações a partir das pontuações da tentativa.
        """
        recs = []

        cats = tentativa.pontuacao_categorias

        if cats.get("vinculos_brasil", 0) < 50:
            recs.append("Fortaleça seus vínculos no Brasil (emprego, estudo, família).")

        if cats.get("situacao_financeira", 0) < 50:
            recs.append("Melhore a apresentação da sua organização financeira.")

        if cats.get("proposito_viagem", 0) < 50:
            recs.append("Apresente melhor seu propósito de viagem e planejamento.")

        if cats.get("historico_viagens", 0) < 50:
            recs.append("Obtenha histórico de viagens para fortalecer sua elegibilidade.")

        if not recs:
            recs.append("Excelentes respostas! Continue praticando e revisando.")

        return recs
