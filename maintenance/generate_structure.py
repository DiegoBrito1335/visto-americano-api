import os
import json

def gerar_estrutura(diretorio, nivel=0, output=[]):
    try:
        items = sorted(os.listdir(diretorio))
        for item in items:
            # Ignorar
            if item in ['venv', '__pycache__', 'node_modules', '.git', '.env', '.vercel']:
                continue
            
            caminho = os.path.join(diretorio, item)
            indent = '│   ' * nivel
            
            if os.path.isdir(caminho):
                output.append(f'{indent}├── 📁 {item}/')
                gerar_estrutura(caminho, nivel + 1, output)
            else:
                # Mostrar tamanho do arquivo
                tamanho = os.path.getsize(caminho)
                if tamanho < 1024:
                    tam_str = f'{tamanho}B'
                elif tamanho < 1024*1024:
                    tam_str = f'{tamanho/1024:.1f}KB'
                else:
                    tam_str = f'{tamanho/(1024*1024):.1f}MB'
                
                output.append(f'{indent}├── 📄 {item} ({tam_str})')
    except PermissionError:
        pass
    
    return output

print('Gerando estrutura do projeto...\n')

estrutura = ['📦 VISTO-AMERICANO-API/']
gerar_estrutura('.', 0, estrutura)

# Salvar em arquivo
with open('ESTRUTURA_PROJETO.txt', 'w', encoding='utf-8') as f:
    f.write('\n'.join(estrutura))

print('✅ Estrutura salva em: ESTRUTURA_PROJETO.txt')
print(f'Total de linhas: {len(estrutura)}')

# Mostrar prévia
print('\n' + '='*60)
print('PRÉVIA:')
print('='*60)
for linha in estrutura[:30]:
    print(linha)
if len(estrutura) > 30:
    print(f'\n... e mais {len(estrutura)-30} itens')
