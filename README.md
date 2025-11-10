# 🧩 PLANEJAMENTO COMPLETO – INTEGRAÇÃO DE WORKFLOW CHATGPT + GEMINI

*(Execução local via terminal – coleta, análise e estudo final automatizados)*

---

## 1. 🎯 Objetivo Geral

Criar um **workflow automatizado** que utiliza **duas IAs** de forma complementar:

* **ChatGPT (OpenAI)** → responsável por **buscar, coletar e organizar informações** provenientes exclusivamente de uma lista pré-definida de fontes confiáveis.
* **Gemini (Google)** → responsável por **interpretar, analisar e redigir um estudo final completo** com base nos arquivos produzidos pelo ChatGPT.

Tudo isso deverá ser executado **localmente**, por meio de **um único comando de terminal**, com controle total sobre instruções, fontes e formato final.

---

## 2. ⚙️ Fluxo de Execução (Visão Geral)

### Entrada:

```bash
python run_pipeline.py "Tema ou pergunta principal"
```

### Saída:

Uma pasta de sessão com:

```
data/sessions/{timestamp}/
├─ 01_raw/           # Dados e notas coletadas pelo ChatGPT
├─ 02_processed/     # (opcional) Normalização intermediária
├─ 03_final/         # Estudo gerado pelo Gemini
├─ meta.json         # Metadados e uso de tokens
└─ task.txt          # Descrição original da tarefa
```

E, no terminal, exibição de:

```
ChatGPT: 5k tokens utilizados de 8k tokens
Gemini: 50k tokens utilizados de 80k tokens
```

---

## 3. 🧱 Estrutura de Pastas e Arquivos

```text
projeto-ia-workflow/
│
├─ config/
│   ├─ chatgpt_config.yaml         # Configuração do modelo ChatGPT
│   ├─ gemini_config.yaml          # Configuração do modelo Gemini
│
├─ prompts/
│   ├─ chatgpt_system.md           # Instruções gerais do ChatGPT
│   ├─ chatgpt_sources.md          # Regras sobre como usar as fontes
│   ├─ gemini_system.md            # Instruções gerais do Gemini
│   ├─ gemini_format.md            # Estrutura e formatação do estudo
│   ├─ fontes_confiaveis.md        # Lista de URLs que o ChatGPT deve obrigatoriamente consultar
│
├─ workflow/
│   ├─ chatgpt_stage.py            # Etapa 1 – coleta e organização
│   ├─ gemini_stage.py             # Etapa 2 – análise e estudo
│   ├─ orchestrator.py             # Orquestrador das etapas
│
├─ data/
│   ├─ sessions/
│       ├─ {timestamp}/            # Sessão individual (gerada a cada execução)
│
├─ .env                            # Chaves das APIs (OPENAI_API_KEY, GOOGLE_API_KEY)
├─ run_pipeline.py                 # Script principal (entrada única)
└─ requirements.txt
```

---

## 4. 🔄 Fluxo Lógico de Execução

### 4.1. Orquestrador (`workflow/orchestrator.py`)

Responsável por:

1. Criar o ID da sessão.
2. Criar a estrutura de pastas da sessão.
3. Salvar a tarefa original (`task.txt`).
4. Executar em sequência:

   * `run_chatgpt_stage(...)`
   * `run_gemini_stage(...)`
5. Exibir e registrar a contagem de tokens.
6. Salvar metadados em `meta.json`.

**Pseudoestrutura:**

```python
def run_pipeline(user_task):
    session_id = create_session_id()
    session_dir = create_session_dir(session_id)

    save_text(session_dir / "task.txt", user_task)

    chatgpt_result, chatgpt_usage = run_chatgpt_stage(user_task, session_dir)
    print(f"ChatGPT: {chatgpt_usage['used_k']:.1f}k tokens utilizados de {chatgpt_usage['max_k']:.1f}k tokens")

    gemini_result, gemini_usage = run_gemini_stage(user_task, session_dir, chatgpt_result)
    print(f"Gemini: {gemini_usage['used_k']:.1f}k tokens utilizados de {gemini_usage['max_k']:.1f}k tokens")

    save_meta(session_dir, user_task, chatgpt_usage, gemini_usage)
```

---

## 5. 🧩 Etapa 1 – ChatGPT (Coleta e Organização de Informações)

(Esta seção permanece inalterada)

---

## 6. 🧠 Etapa 2 – Gemini (Estudo Final)

### Função:

Elaborar um **estudo analítico completo** com base nos arquivos produzidos pelo ChatGPT.

### Fontes de entrada:

* `01_raw/summary.md`
* `01_raw/sources.json`
* `01_raw/notes/`

### Saída esperada:

`03_final/estudo_final.md`

### 6.1. Instruções (`gemini_system.md`)

> Seu papel é **produzir um estudo analítico** com base nas informações coletadas por outra IA.
>
> * Não busque novas fontes.
> * Analise criticamente os dados fornecidos.
> * Identifique convergências, divergências e lacunas.
> * Gere um estudo acadêmico e claro, conforme o formato definido.

### 6.2. Formatação do estudo (`gemini_format.md`)

> Estrutura obrigatória:
>
> 1. Título
> 2. Resumo Executivo
> 3. Introdução
> 4. Contexto Teórico
> 5. Análise e Discussão
> 6. Conclusão
> 7. Referências (Autor – Título – Link – Data)

---

## 7. 📊 Configurações e Limites

### 7.1. ChatGPT

`config/chatgpt_config.yaml` (Inalterado)

### 7.2. Gemini

`config/gemini_config.yaml`

```yaml
model: gemini-1.5-pro-latest
max_context_tokens: 1048576
temperature: 0.4
```

---

## 8. 📁 Registro de Sessão e Logs

Ao final da execução, o arquivo `meta.json` salva todas as informações da sessão:

```json
{
  "task": "Impacto da IA no mercado de trabalho brasileiro",
  "chatgpt": {
    "model": "gpt-4o-mini",
    "used_tokens": 5320,
    "max_context_tokens": 8000
  },
  "gemini": {
    "model": "gemini-1.5-pro-latest",
    "used_tokens": 0,
    "max_context_tokens": 1048576
  }
}
```

---

## 9. 💻 Execução via Terminal

Exemplo prático:

```bash
python run_pipeline.py "Impacto da IA na educação básica no Brasil"
```

Saída esperada:

```
[OK] Sessão 2025-11-07_14-33 criada.
[OK] Etapa 1 (ChatGPT) concluída. Arquivos em data/sessions/2025-11-07_14-33/01_raw
ChatGPT: 5.3k tokens utilizados de 8.0k tokens
[OK] Etapa 2 (Gemini) concluída. Estudo final em data/sessions/2025-11-07_14-33/03_final/estudo_final.md
Gemini: 0.0k tokens utilizados de 1048.6k tokens
```

---

## 10. 🧩 Componentes-Chave do Planejamento

| **Componente**         | **Responsabilidade**                                  |
| ---------------------- | ----------------------------------------------------- |
| `run_pipeline.py`      | Ponto único de entrada via terminal                   |
| `orchestrator.py`      | Coordena as etapas e exibe tokens                     |
| `chatgpt_stage.py`     | Coleta e organiza dados conforme fontes confiáveis    |
| `gemini_stage.py`      | Produz o estudo final com base nos arquivos coletados |
| `fontes_confiaveis.md` | Lista de URLs obrigatórias e exclusivas               |
| `meta.json`            | Registro de uso de tokens e metadados                 |
| `prompts/*.md`         | Regras explícitas que guiam as decisões das IAs       |
| `config/*.yaml`        | Limites e parâmetros dos modelos                      |

---

## 11. 🚀 Próximos Passos

1. Criar os arquivos `prompts/*.md`.
2. Preencher `fontes_confiaveis.md`.
3. Configurar as chaves da API em `.env`.
4. Implementar as funções de cada etapa.
5. Testar o fluxo completo com uma tarefa real.

---

✅ **Resumo final:**
Este sistema cria um **pipeline automatizado, local e controlado**, onde o ChatGPT atua como **coletor de dados confiáveis** e o Gemini como **sintetizador analítico**.
