#!/usr/bin/env python3
"""
Script para remover perguntas duplicadas do banco Railway
Não precisa do psql instalado - usa Python!
Execute: python remover_duplicatas.py
"""
import psycopg2
import sys

# Connection string público do Railway
DATABASE_URL = "postgresql://postgres:yLqSvgitoigRDPJCDdzuVfVnuqPMyfQz@ballast.proxy.rlwy.net:38147/railway"

def main():
    print("="*60)
    print("🗑️  REMOVENDO PERGUNTAS DUPLICADAS")
    print("="*60)
    
    try:
        # Conectar ao banco
        print("\n🔗 Conectando ao banco Railway...")
        conn = psycopg2.connect(DATABASE_URL)
        cursor = conn.cursor()
        print("✅ Conectado!")
        
        # PASSO 1: Ver duplicatas DS-160
        print("\n" + "="*60)
        print("1️⃣ VERIFICANDO DUPLICATAS DS-160...")
        print("="*60)
        
        cursor.execute("""
            SELECT pergunta_texto, COUNT(*) as qtd, ARRAY_AGG(id ORDER BY id) as ids
            FROM perguntas_ds160
            GROUP BY pergunta_texto
            HAVING COUNT(*) > 1
            ORDER BY qtd DESC;
        """)
        
        dup_ds160 = cursor.fetchall()
        
        if dup_ds160:
            print(f"\n❌ Encontradas {len(dup_ds160)} perguntas duplicadas:")
            for i, (texto, qtd, ids) in enumerate(dup_ds160[:5], 1):
                print(f"   {i}. {qtd}x - {texto[:60]}... (IDs: {ids})")
            if len(dup_ds160) > 5:
                print(f"   ... e mais {len(dup_ds160) - 5} duplicatas")
        else:
            print("✅ Nenhuma duplicata encontrada")
        
        # PASSO 2: Ver duplicatas Entrevista
        print("\n" + "="*60)
        print("2️⃣ VERIFICANDO DUPLICATAS ENTREVISTA...")
        print("="*60)
        
        cursor.execute("""
            SELECT pergunta_texto, COUNT(*) as qtd, ARRAY_AGG(id ORDER BY id) as ids
            FROM perguntas_entrevista
            GROUP BY pergunta_texto
            HAVING COUNT(*) > 1
            ORDER BY qtd DESC;
        """)
        
        dup_entrevista = cursor.fetchall()
        
        if dup_entrevista:
            print(f"\n❌ Encontradas {len(dup_entrevista)} perguntas duplicadas:")
            for i, (texto, qtd, ids) in enumerate(dup_entrevista[:5], 1):
                print(f"   {i}. {qtd}x - {texto[:60]}... (IDs: {ids})")
            if len(dup_entrevista) > 5:
                print(f"   ... e mais {len(dup_entrevista) - 5} duplicatas")
        else:
            print("✅ Nenhuma duplicata encontrada")
        
        # Se não há duplicatas, encerrar
        total_duplicatas = len(dup_ds160) + len(dup_entrevista)
        
        if total_duplicatas == 0:
            print("\n" + "="*60)
            print("✅ BANCO LIMPO! Nenhuma duplicata para remover.")
            print("="*60)
            conn.close()
            return
        
        # Confirmar remoção
        print("\n" + "="*60)
        print(f"⚠️  TOTAL: {total_duplicatas} grupos de duplicatas")
        print("="*60)
        
        resposta = input("\n❓ Deseja remover as duplicatas? (SIM para confirmar): ").strip().upper()
        
        if resposta != "SIM":
            print("\n❌ Operação cancelada pelo usuário")
            conn.close()
            return
        
        # PASSO 3: Remover duplicatas DS-160
        print("\n" + "="*60)
        print("3️⃣ REMOVENDO DUPLICATAS DS-160...")
        print("="*60)
        
        cursor.execute("""
            WITH duplicatas AS (
                SELECT id, ROW_NUMBER() OVER (PARTITION BY pergunta_texto ORDER BY id) as rn
                FROM perguntas_ds160
            )
            DELETE FROM perguntas_ds160
            WHERE id IN (SELECT id FROM duplicatas WHERE rn > 1);
        """)
        
        removidos_ds160 = cursor.rowcount
        print(f"✅ Removidas {removidos_ds160} perguntas duplicadas de DS-160")
        
        # PASSO 4: Remover duplicatas Entrevista
        print("\n" + "="*60)
        print("4️⃣ REMOVENDO DUPLICATAS ENTREVISTA...")
        print("="*60)
        
        cursor.execute("""
            WITH duplicatas AS (
                SELECT id, ROW_NUMBER() OVER (PARTITION BY pergunta_texto ORDER BY id) as rn
                FROM perguntas_entrevista
            )
            DELETE FROM perguntas_entrevista
            WHERE id IN (SELECT id FROM duplicatas WHERE rn > 1);
        """)
        
        removidos_entrevista = cursor.rowcount
        print(f"✅ Removidas {removidos_entrevista} perguntas duplicadas de Entrevista")
        
        # Commit
        conn.commit()
        
        # PASSO 5: Verificar resultado
        print("\n" + "="*60)
        print("5️⃣ VERIFICANDO RESULTADO FINAL...")
        print("="*60)
        
        cursor.execute("""
            SELECT 'DS-160' as tipo, 
                   COUNT(*) as total,
                   COUNT(*) FILTER (WHERE gratuita = true) as gratuitas,
                   COUNT(*) FILTER (WHERE gratuita = false) as premium
            FROM perguntas_ds160
            
            UNION ALL
            
            SELECT 'Entrevista' as tipo,
                   COUNT(*) as total,
                   COUNT(*) FILTER (WHERE gratuita = true) as gratuitas,
                   COUNT(*) FILTER (WHERE gratuita = false) as premium
            FROM perguntas_entrevista;
        """)
        
        totais = cursor.fetchall()
        
        print("\n📊 TOTAIS ATUAIS:")
        print(f"\n   {'Tipo':<15} {'Total':<10} {'Gratuitas':<12} {'Premium':<10}")
        print("   " + "-"*50)
        
        total_geral = 0
        total_gratuitas = 0
        total_premium = 0
        
        for tipo, total, gratuitas, premium in totais:
            print(f"   {tipo:<15} {total:<10} {gratuitas:<12} {premium:<10}")
            total_geral += total
            total_gratuitas += gratuitas
            total_premium += premium
        
        print("   " + "-"*50)
        print(f"   {'TOTAL':<15} {total_geral:<10} {total_gratuitas:<12} {total_premium:<10}")
        
        # Verificar se ainda há duplicatas
        cursor.execute("""
            SELECT COUNT(*) FROM (
                SELECT pergunta_texto FROM perguntas_ds160 
                GROUP BY pergunta_texto HAVING COUNT(*) > 1
            ) s;
        """)
        dup_restantes_ds160 = cursor.fetchone()[0]
        
        cursor.execute("""
            SELECT COUNT(*) FROM (
                SELECT pergunta_texto FROM perguntas_entrevista 
                GROUP BY pergunta_texto HAVING COUNT(*) > 1
            ) s;
        """)
        dup_restantes_entrevista = cursor.fetchone()[0]
        
        print("\n📋 VERIFICAÇÃO FINAL:")
        print(f"   DS-160 duplicadas restantes: {dup_restantes_ds160}")
        print(f"   Entrevista duplicadas restantes: {dup_restantes_entrevista}")
        
        if dup_restantes_ds160 == 0 and dup_restantes_entrevista == 0:
            print("\n" + "="*60)
            print("✅ SUCESSO! TODAS AS DUPLICATAS FORAM REMOVIDAS!")
            print("="*60)
            print(f"\n📊 RESUMO:")
            print(f"   - Removidas {removidos_ds160} perguntas DS-160")
            print(f"   - Removidas {removidos_entrevista} perguntas Entrevista")
            print(f"   - Total de perguntas: {total_geral}")
            print(f"   - Gratuitas: {total_gratuitas}")
            print(f"   - Premium: {total_premium}")
        else:
            print("\n⚠️ ATENÇÃO: Ainda existem duplicatas!")
        
        conn.close()
        print("\n✅ Script concluído!")
        
    except psycopg2.Error as e:
        print(f"\n❌ ERRO no banco de dados:")
        print(f"   {e}")
        sys.exit(1)
        
    except Exception as e:
        print(f"\n❌ ERRO inesperado:")
        print(f"   {e}")
        sys.exit(1)

if __name__ == "__main__":
    main()