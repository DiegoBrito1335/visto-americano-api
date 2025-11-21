# 🛠️ Scripts de Manutenção - Aprova Visto Americano

Scripts administrativos para gerenciar o banco de dados e usuários do sistema.

---

## 📋 **SCRIPTS DISPONÍVEIS**

### 👥 **Gerenciamento de Usuários**

#### `list_users.py`
Lista todos os usuários cadastrados e suas estatísticas.

```bash
python maintenance/list_users.py
```

**Exibe:**
- Lista completa de usuários
- Email, nome, plano, data de cadastro
- Estatísticas (gratuitos vs premium)

---

#### `activate_premium.py`
Atualiza usuário para plano Premium.

```bash
python maintenance/activate_premium.py
```

**Funcionalidades:**
- Lista usuários disponíveis
- Permite escolher qual atualizar
- Torna premium vitalício
- Confirmação antes de atualizar

---

#### `create_test_user.py`
Cria usuário de teste para desenvolvimento.

```bash
python maintenance/create_test_user.py
```

**Cria:**
- Email: teste@email.com
- Senha: senha123
- Plano: gratuito

---

### 📝 **Gerenciamento de Perguntas**

#### `populate_questions.py`
Popula o banco com perguntas DS-160 e Entrevista.

```bash
python maintenance/populate_questions.py
```

**Atenção:** Remove perguntas existentes antes de popular!

---

#### `analyze_questions.py`
Análise completa do banco de perguntas.

```bash
python maintenance/analyze_questions.py
```

**Exibe:**
- Total de perguntas por tipo
- Quantidade gratuitas vs premium
- Lista de perguntas DS-160
- Estatísticas detalhadas

---

#### `reduce_questions.py`
Reduz número de perguntas gratuitas.

```bash
# Reduzir para 25 gratuitas
python maintenance/reduce_questions.py --target 25

# Reduzir para 30 gratuitas
python maintenance/reduce_questions.py --target 30
```

**Funcionalidades:**
- Escolhe quantas perguntas manter gratuitas
- Mantém proporção DS-160/Entrevista
- Confirmação antes de aplicar
- Mostra preview das mudanças

---

#### `remove_duplicates.py`
Remove perguntas duplicadas do banco.

```bash
# Modo interativo (com confirmação)
python maintenance/remove_duplicates.py

# Modo automático
python maintenance/remove_duplicates.py --yes
```

**Funcionalidades:**
- Detecta duplicatas por texto
- Remove automaticamente duplicados
- Mantém apenas o primeiro ID
- Exibe estatísticas finais

---

#### `verify_options.py`
Verifica estrutura de opções em perguntas de múltipla escolha.

```bash
python maintenance/verify_options.py
```

**Útil para:**
- Debugar problemas de opções
- Ver formato JSON das opções
- Verificar integridade dos dados

---

### 🏗️ **Utilitários**

#### `generate_structure.py`
Gera estrutura de pastas do projeto.

```bash
python maintenance/generate_structure.py
```

**Cria:**
- Arquivo `ESTRUTURA_PROJETO.txt`
- Árvore completa de arquivos
- Tamanhos de arquivos
- Prévia na tela

---

## ⚙️ **CONFIGURAÇÃO**

### **Banco de Dados**

Todos os scripts usam a configuração do sistema:
- **Desenvolvimento:** SQLite local (`visto_local.db`)
- **Produção:** PostgreSQL (Railway via `DATABASE_URL`)

**Não é necessário configurar nada!** Os scripts detectam automaticamente.

### **Variáveis de Ambiente**

Configure no arquivo `.env`:

```env
# Produção (Railway fornece automaticamente)
DATABASE_URL=postgresql://user:password@host:5432/dbname

# Desenvolvimento (padrão)
DATABASE_URL=sqlite:///./visto_local.db
```

---

## 🚀 **FLUXO DE TRABALHO COMUM**

### **1. Setup Inicial**

```bash
# 1. Criar tabelas e popular perguntas
python maintenance/populate_questions.py

# 2. Criar usuário de teste
python maintenance/create_test_user.py

# 3. Verificar
python maintenance/list_users.py
python maintenance/analyze_questions.py
```

### **2. Ajustar Perguntas Gratuitas**

```bash
# 1. Ver situação atual
python maintenance/analyze_questions.py

# 2. Reduzir para 25 gratuitas
python maintenance/reduce_questions.py --target 25

# 3. Verificar resultado
python maintenance/analyze_questions.py
```

### **3. Ativar Premium em Usuário**

```bash
# 1. Ver usuários
python maintenance/list_users.py

# 2. Ativar premium
python maintenance/activate_premium.py

# 3. Confirmar
python maintenance/list_users.py
```

### **4. Limpar Duplicatas**

```bash
# 1. Remover duplicatas
python maintenance/remove_duplicates.py

# 2. Verificar
python maintenance/analyze_questions.py
```

---

## 📚 **EXEMPLOS DE USO**

### **Exemplo 1: Setup de Desenvolvimento**

```bash
# Terminal 1 - Backend
uvicorn app.main:app --reload

# Terminal 2 - Popular dados
python maintenance/populate_questions.py
python maintenance/create_test_user.py

# Testar no navegador
# Login: teste@email.com / senha123
```

### **Exemplo 2: Preparar para Produção**

```bash
# 1. Limpar duplicatas
python maintenance/remove_duplicates.py --yes

# 2. Ajustar gratuitas
python maintenance/reduce_questions.py --target 40

# 3. Verificar integridade
python maintenance/analyze_questions.py
python maintenance/verify_options.py

# 4. Deploy!
git add .
git commit -m "Database pronta para produção"
git push
```

### **Exemplo 3: Dar Premium para Cliente**

```bash
# 1. Listar usuários
python maintenance/list_users.py

# 2. Ativar premium
python maintenance/activate_premium.py
# Escolher o número do usuário

# 3. Confirmar
python maintenance/list_users.py
```

---

## ⚠️ **AVISOS IMPORTANTES**

### **🔴 PRODUÇÃO**

- ✅ **Sempre faça backup** antes de rodar scripts em produção
- ✅ **Teste localmente** primeiro
- ✅ **Use `--yes` com cuidado** (pula confirmações)

### **🔒 SEGURANÇA**

- ✅ **Nunca commite** arquivos `.db`
- ✅ **Nunca commite** arquivo `.env`
- ✅ **Credenciais** devem estar no `.env` apenas

### **📊 DADOS**

- `populate_questions.py` **DELETA** perguntas existentes
- `reduce_questions.py` **DELETA** perguntas extras
- `remove_duplicates.py` **DELETA** duplicatas

**Sempre confirme antes de prosseguir!**

---

## 🐛 **TROUBLESHOOTING**

### **Erro: "No module named 'app'"**

```bash
# Execute do diretório raiz do projeto
cd C:\Users\...\visto-americano-api
python maintenance/script.py
```

### **Erro: "Unable to open database file"**

```bash
# Certifique-se que está no diretório correto
pwd  # ou cd

# Ou especifique o DATABASE_URL no .env
```

### **Erro: "Table already exists"**

```bash
# Normal. Tabelas já existem.
# Rode populate_questions.py se quiser resetar
```

---

## 📞 **SUPORTE**

Para problemas:
1. Verifique se está no diretório raiz do projeto
2. Verifique se o `.env` está configurado
3. Verifique os logs de erro
4. Execute com `--help` para ver opções

---

## 📝 **CHANGELOG**

### **v2.0.0** (Atual)
- ✅ Removidas credenciais hardcoded
- ✅ Scripts consolidados (23 → 10)
- ✅ Usa `app.database` corretamente
- ✅ Argumentos CLI com argparse
- ✅ Documentação completa
- ✅ Códigos limpos e organizados

### **v1.0.0** (Antiga)
- ⚠️ Credenciais hardcoded
- ⚠️ Scripts duplicados
- ⚠️ Sem documentação

---

**Desenvolvido com ❤️ para o projeto Aprova Visto Americano**