"""
Script para reduzir número de perguntas gratuitas
Uso: python maintenance/reduce_questions.py --target 25
"""

import sys
import argparse
import random
from pathlib import Path

# Adicionar raiz ao path
sys.path.insert(0, str(Path(__file__).parent.parent))

from app.database import SessionLocal
from app.models import PerguntaDS160, PerguntaEntrevista


def reduce_questions(target_total=25):
    """Reduz perguntas gratuitas para o número alvo"""
    db = SessionLocal()
    
    try:
        print("\n" + "=" * 70)
        print(f"📉 REDUZINDO PERGUNTAS GRATUITAS PARA {target_total}")
        print("=" * 70)
        
        # Verificar situação atual
        gratuitas_ds160_atual = db.query(PerguntaDS160).filter(PerguntaDS160.gratuita == True).count()
        gratuitas_entrevista_atual = db.query(PerguntaEntrevista).filter(PerguntaEntrevista.gratuita == True).count()
        total_gratuitas_atual = gratuitas_ds160_atual + gratuitas_entrevista_atual
        
        print(f"\n📊 SITUAÇÃO ATUAL:")
        print(f"   Total gratuitas: {total_gratuitas_atual}")
        print(f"   - DS-160: {gratuitas_ds160_atual}")
        print(f"   - Entrevista: {gratuitas_entrevista_atual}")
        
        if total_gratuitas_atual <= target_total:
            print(f"\n✅ Já temos {total_gratuitas_atual} perguntas (meta: {target_total})")
            print("   Nenhuma ação necessária!")
            return
        
        # Calcular nova distribuição (60% DS-160, 40% Entrevista)
        nova_ds160 = int(target_total * 0.6)
        nova_entrevista = target_total - nova_ds160
        
        print(f"\n🎯 NOVA META:")
        print(f"   Total: {target_total}")
        print(f"   - DS-160: {nova_ds160}")
        print(f"   - Entrevista: {nova_entrevista}")
        
        # Confirmar
        resp = input("\n⚠️  Confirmar redução? (SIM para continuar): ")
        if resp != "SIM":
            print("❌ Operação cancelada.")
            return
        
        # Pegar IDs atuais
        ids_ds160 = [p.id for p in db.query(PerguntaDS160).filter(PerguntaDS160.gratuita == True).all()]
        ids_entrevista = [p.id for p in db.query(PerguntaEntrevista).filter(PerguntaEntrevista.gratuita == True).all()]
        
        # Selecionar aleatoriamente quais manter
        manter_ds160 = random.sample(ids_ds160, min(nova_ds160, len(ids_ds160)))
        manter_entrevista = random.sample(ids_entrevista, min(nova_entrevista, len(ids_entrevista)))
        
        print(f"\n🔄 Processando...")
        
        # Marcar todas como premium
        db.query(PerguntaDS160).update({"gratuita": False})
        db.query(PerguntaEntrevista).update({"gratuita": False})
        
        # Marcar selecionadas como gratuitas
        for id_p in manter_ds160:
            db.query(PerguntaDS160).filter(PerguntaDS160.id == id_p).update({"gratuita": True})
        
        for id_p in manter_entrevista:
            db.query(PerguntaEntrevista).filter(PerguntaEntrevista.id == id_p).update({"gratuita": True})
        
        db.commit()
        
        # Verificar resultado
        final_ds160 = db.query(PerguntaDS160).filter(PerguntaDS160.gratuita == True).count()
        final_entrevista = db.query(PerguntaEntrevista).filter(PerguntaEntrevista.gratuita == True).count()
        premium_ds160 = db.query(PerguntaDS160).filter(PerguntaDS160.gratuita == False).count()
        premium_entrevista = db.query(PerguntaEntrevista).filter(PerguntaEntrevista.gratuita == False).count()
        
        print(f"\n" + "=" * 70)
        print("✅ REDUÇÃO CONCLUÍDA COM SUCESSO!")
        print("=" * 70)
        
        print(f"\n📈 RESULTADO FINAL:")
        print(f"\n   🆓 GRATUITAS: {final_ds160 + final_entrevista}")
        print(f"      - DS-160: {final_ds160}")
        print(f"      - Entrevista: {final_entrevista}")
        
        print(f"\n   ⭐ PREMIUM: {premium_ds160 + premium_entrevista}")
        print(f"      - DS-160: {premium_ds160}")
        print(f"      - Entrevista: {premium_entrevista}")
        
        print(f"\n   📊 TOTAL: {final_ds160 + final_entrevista + premium_ds160 + premium_entrevista}")
        print("=" * 70 + "\n")
        
    except Exception as e:
        print(f"\n❌ Erro: {e}")
        db.rollback()
        import traceback
        traceback.print_exc()
    finally:
        db.close()


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Reduzir número de perguntas gratuitas")
    parser.add_argument("--target", type=int, default=25, help="Número alvo de perguntas gratuitas (padrão: 25)")
    
    args = parser.parse_args()
    
    reduce_questions(args.target)