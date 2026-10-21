## 🚀 Como Rodar (Demo Local)

Você pode testar o projeto de duas formas: no **Modo Simulação** (sem necessidade de chave de API) ou no **Modo Real** (com a API da Anthropic).

---

### 1. Modo Simulação / Avaliação Rápida (Recomendado para Teste)
*Não requer chave de API da Anthropic. Executa a triagem com dados simulados e guardrails ativos.*

**No Windows (PowerShell):**
```powershell
pip install -r requirements.txt
$env:ITOPS_SIMULACAO="1"
$env:ITOPS_DRY_RUN="1"
python demo.py
```

**No Linux / macOS (Bash):**
```bash
pip install -r requirements.txt
export ITOPS_SIMULACAO=1
export ITOPS_DRY_RUN=1
python demo.py
```

---

### 2. Modo Real (Integração Direta com Claude 3.5 Sonnet)

**No Windows (PowerShell):**
```powershell
$env:ANTHROPIC_API_KEY="sua-chave-api-aqui"
python demo.py
```

**No Linux / macOS (Bash):**
```bash
export ANTHROPIC_API_KEY="sua-chave-api-aqui"
python demo.py
```
