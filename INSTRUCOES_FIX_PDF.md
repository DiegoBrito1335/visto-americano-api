# FIX DO BOTÃO PDF - INSTRUÇÕES

## ✅ DIAGNÓSTICO
- Endpoint existe no backend (linha 874 de app/main.py)
- Problema: Frontend não mostra o botão ou não funciona

## 📝 PASSO A PASSO

### 1. Abrir arquivo
```
frontend/resultado.html
```

### 2. Localizar seção de botões
Procure por algo como:
```html
<div class="flex gap-4">
  <button>Nova Simulação</button>
  <button>Dashboard</button>
  ...
</div>
```

### 3. Adicionar botão PDF
Adicione ESTE botão no grupo de botões:

```html
<button 
    id="btnBaixarPDF"
    onclick="baixarPDF()"
    class="bg-red-600 text-white px-6 py-3 rounded-lg hover:bg-red-700 transition-colors font-medium shadow-lg flex items-center gap-2"
>
    <i class="fas fa-file-pdf"></i>
    <span>Baixar Relatório PDF</span>
</button>
```

### 4. Adicionar função JavaScript
Procure o `<script>` no final do arquivo e adicione:

```javascript
// Função para baixar PDF
async function baixarPDF() {
    const btn = document.getElementById('btnBaixarPDF');
    const API_URL = 'https://web-production-e07b4.up.railway.app';
    
    try {
        // Pegar ID da URL
        const params = new URLSearchParams(window.location.search);
        const tentativaId = params.get('id');
        
        if (!tentativaId) {
            alert('❌ ID da tentativa não encontrado na URL');
            return;
        }
        
        // Pegar token
        const token = localStorage.getItem('token');
        if (!token) {
            alert('❌ Você precisa estar logado');
            window.location.href = '/login.html';
            return;
        }
        
        // Loading
        btn.disabled = true;
        btn.innerHTML = '<i class="fas fa-spinner fa-spin"></i> Gerando PDF...';
        
        // Requisição
        const response = await fetch(`${API_URL}/api/resultado/${tentativaId}/pdf`, {
            headers: { 'Authorization': `Bearer ${token}` }
        });
        
        if (!response.ok) throw new Error('Erro ao gerar PDF');
        
        // Download
        const blob = await response.blob();
        const url = URL.createObjectURL(blob);
        const a = document.createElement('a');
        a.href = url;
        a.download = `resultado_visto_${tentativaId}.pdf`;
        a.click();
        URL.revokeObjectURL(url);
        
        alert('✅ PDF baixado com sucesso!');
        
    } catch (error) {
        console.error(error);
        alert('❌ Erro ao baixar PDF: ' + error.message);
    } finally {
        btn.disabled = false;
        btn.innerHTML = '<i class="fas fa-file-pdf"></i> Baixar Relatório PDF';
    }
}
```

### 5. Salvar e fazer deploy
```bash
git add frontend/resultado.html
git commit -m "fix: adicionar e corrigir botão PDF"
git push origin main
```

### 6. Testar
1. Acesse: aprovavistoamericano.com.br
2. Faça uma simulação
3. Na página de resultado, clique em "Baixar Relatório PDF"
4. PDF deve baixar automaticamente

## 🐛 SE NÃO FUNCIONAR

Abra o Console do navegador (F12) e veja o erro.
Me envie o erro que aparece no console.
