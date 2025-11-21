"""
Script para análise completa do banco de perguntas
Uso: python maintenance/analyze_questions.py
"""

import sys
from pathlib import Path

# Adicionar raiz ao path
sys.path.insert(0, str(Path(__file__).parent.parent))

from app.database import SessionLocal
from app.models import PerguntaDS160, PerguntaEntrevista


def analyze_questions():
    """Análise completa do banco de perguntas"""
    db = SessionLocal()
    
    try:
        print("\n" + "=" * 80)
        print("📊 ANÁLISE COMPLETA DO BANCO DE PERGUNTAS")
        print("=" * 80)
        
        # Contar DS-160
        total_ds160 = db.query(PerguntaDS160).count()
        gratuitas_ds160 = db.query(PerguntaDS160).filter(PerguntaDS160.gratuita == True).count()
        premium_ds160 = total_ds160 - gratuitas_ds160
        
        # Contar Entrevista
        total_entrevista = db.query(PerguntaEntrevista).count()
        gratuitas_entrevista = db.query(PerguntaEntrevista).filter(PerguntaEntrevista.gratuita == True).count()
        premium_entrevista = total_entrevista - gratuitas_entrevista
        
        # Exibir estatísticas
        print(f"\n📋 PERGUNTAS DS-160:")
        print(f"   Total: {total_ds160}")
        print(f"   🆓 Gratuitas: {gratuitas_ds160}")
        print(f"   ⭐ Premium: {premium_ds160}")
        
        print(f"\n💬 PERGUNTAS ENTREVISTA:")
        print(f"   Total: {total_entrevista}")
        print(f"   🆓 Gratuitas: {gratuitas_entrevista}")
        print(f"   ⭐ Premium: {premium_entrevista}")
        
        print(f"\n🎯 RESUMO GERAL:")
        print(f"   Total: {total_ds160 + total_entrevista} perguntas")
        print(f"   🆓 Gratuitas: {gratuitas_ds160 + gratuitas_entrevista}")
        print(f"   ⭐ Premium: {premium_ds160 + premium_entrevista}")
        
        # Listar todas DS-160
        print(f"\n" + "=" * 80)
        print(f"📋 TODAS AS PERGUNTAS DS-160 ({total_ds160}):")
        print("=" * 80)
        
        perguntas = db.query(PerguntaDS160).order_by(PerguntaDS160.id).all()
        
        for p in perguntas:
            tipo = "🆓 GRÁTIS" if p.gratuita else "⭐ PREMIUM"
            texto = p.pergunta_texto[:70] + "..." if len(p.pergunta_texto) > 70 else p.pergunta_texto
            print(f"ID {p.id:3d} [{tipo}] {texto}")
        
        # Listar todas Entrevista
        print(f"\n" + "=" * 80)
        print(f"💬 TODAS AS PERGUNTAS ENTREVISTA ({total_entrevista}):")
        print("=" * 80)
        
        perguntas = db.query(PerguntaEntrevista).order_by(PerguntaEntrevista.id).all()
        
        for p in perguntas:
            tipo = "🆓 GRÁTIS" if p.gratuita else "⭐ PREMIUM"
            texto = p.pergunta_texto[:70] + "..." if len(p.pergunta_texto) > 70 else p.pergunta_texto
            print(f"ID {p.id:3d} [{tipo}] {texto}")
        
        print(f"\n" + "=" * 80 + "\n")
        
    except Exception as e:
        print(f"\n❌ Erro: {e}")
        import traceback
        traceback.print_exc()
    finally:
        db.close()


if __name__ == "__main__":
    analyze_questions()