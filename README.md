# 🧩 PLANEJAMENTO COMPLETO – INTEGRAÇÃO DE WORKFLOW CHATGPT + CLAUDE

*(Execução local via terminal – coleta, análise e estudo final automatizados)*

---

## 1. 🎯 Objetivo Geral

Criar um **workflow automatizado** que utiliza **duas IAs** de forma complementar:

* **ChatGPT (OpenAI)** → responsável por **buscar, coletar e organizar informações** provenientes exclusivamente de uma lista pré-definida de fontes confiáveis.
* **Claude (Anthropic)** → responsável por **interpretar, analisar e redigir um estudo final completo** com base nos arquivos produzidos pelo ChatGPT.

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
├─ 03_final/         # Estudo gerado pelo Claude
├─ meta.json         # Metadados e uso de tokens
└─ task.txt          # Descrição original da tarefa
```

E, no terminal, exibição de:

```
ChatGPT: 5k tokens utilizados de 8k tokens
Claude: 50k tokens utilizados de 80k tokens
```

---

## 3. 🧱 Estrutura de Pastas e Arquivos

```text
projeto-ia-workflow/
│
├─ config/
│   ├─ chatgpt_config.yaml         # Configuração do modelo ChatGPT
│   ├─ claude_config.yaml          # Configuração do modelo Claude
│
├─ prompts/
│   ├─ chatgpt_system.md           # Instruções gerais do ChatGPT
│   ├─ chatgpt_sources.md          # Regras sobre como usar as fontes
│   ├─ claude_system.md            # Instruções gerais do Claude
│   ├─ claude_format.md            # Estrutura e formatação do estudo
│   ├─ fontes_confiaveis.md        # Lista de URLs que o ChatGPT deve obrigatoriamente consultar
│
├─ workflow/
│   ├─ chatgpt_stage.py            # Etapa 1 – coleta e organização
│   ├─ claude_stage.py             # Etapa 2 – análise e estudo
│   ├─ orchestrator.py             # Orquestrador das etapas
│
├─ data/
│   ├─ sessions/
│       ├─ {timestamp}/            # Sessão individual (gerada a cada execução)
│
├─ .env                            # Chaves das APIs (OPENAI_API_KEY, ANTHROPIC_API_KEY)
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
   * `run_claude_stage(...)`
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

    claude_result, claude_usage = run_claude_stage(user_task, session_dir, chatgpt_result)
    print(f"Claude: {claude_usage['used_k']:.1f}k tokens utilizados de {claude_usage['max_k']:.1f}k tokens")

    save_meta(session_dir, user_task, chatgpt_usage, claude_usage)
```

---

## 5. 🧩 Etapa 1 – ChatGPT (Coleta e Organização de Informações)

### Função:

Atuar como **“search engine rebuscada”**, coletando, filtrando e estruturando informações apenas a partir das URLs listadas em `prompts/fontes_confiaveis.md`.

### Regras:

* Consultar **todas as fontes listadas**.
* **Não acessar nenhuma fonte externa** fora do arquivo.
* Respeitar a ordem de prioridade (de cima para baixo).
* Gerar saídas padronizadas:

  * `summary.md` → resumo geral
  * `sources.json` → metadados das fontes
  * `notes/` → notas temáticas em Markdown

### 5.1. Arquivo `fontes_confiaveis.md`

Exemplo de formato:

```md
# Fontes confiáveis (ordem de prioridade)
https://www.gov.br/...
https://www.inep.gov.br/...
https://www.scielo.br/...
https://pubmed.ncbi.nlm.nih.gov/...
https://data.worldbank.org/...
```

### 5.2. Inserção no prompt

O arquivo é lido e injetado no `system prompt`:

```python
trusted_sources = load_trusted_sources("prompts/fontes_confiaveis.md")
trusted_block = "\n".join(f"- {url}" for url in trusted_sources)

system_prompt = (
    load_file("prompts/chatgpt_system.md")
    + "\n\n"
    + load_file("prompts/chatgpt_sources.md")
    + "\n\nLISTA DE FONTES CONFIÁVEIS (USO OBRIGATÓRIO, NESSA ORDEM):\n"
    + trusted_block
)
```

### 5.3. Exemplo de instruções (`chatgpt_system.md`)

> Seu papel é atuar como um **motor de busca especializado**, coletando e organizando informações apenas a partir das fontes confiáveis fornecidas.
>
> * Você deve **consultar todas as URLs listadas**.
> * Não acesse ou cite nenhuma outra fonte.
> * Produza arquivos separados:
>
>   * `SUMMARY` → visão geral,
>   * `SOURCES` → lista estruturada com metadados (título, autor, link, data, confiabilidade),
>   * `NOTES` → notas temáticas agrupadas.
> * Mantenha o texto em português claro e técnico.

### 5.4. Registro de uso de tokens (ChatGPT)

Após a execução da API:

```python
used_tokens = response.usage.total_tokens
max_tokens = config["max_context_tokens"]
print(f"ChatGPT: {used_tokens/1000:.1f}k tokens utilizados de {max_tokens/1000:.1f}k tokens")
```

---

## 6. 🧠 Etapa 2 – Claude (Estudo Final)

### Função:

Elaborar um **estudo analítico completo** com base nos arquivos produzidos pelo ChatGPT.

### Fontes de entrada:

* `01_raw/summary.md`
* `01_raw/sources.json`
* `01_raw/notes/`

### Saída esperada:

`03_final/estudo_final.md`

### 6.1. Instruções (`claude_system.md`)

> Seu papel é **produzir um estudo analítico** com base nas informações coletadas por outra IA.
>
> * Não busque novas fontes.
> * Analise criticamente os dados fornecidos.
> * Identifique convergências, divergências e lacunas.
> * Gere um estudo acadêmico e claro, conforme o formato definido.

### 6.2. Formatação do estudo (`claude_format.md`)

> Estrutura obrigatória:
>
> 1. Título
> 2. Resumo Executivo
> 3. Introdução
> 4. Contexto Teórico
> 5. Análise e Discussão
> 6. Conclusão
> 7. Referências (Autor – Título – Link – Data)
>
> Regras:
>
> * Texto em português (Brasil).
> * Linguagem formal e analítica.
> * Mínimo de X palavras.
> * Subtítulos claros e consistentes.

### 6.3. Contagem de tokens (Claude)

Após a execução da API:

```python
input_tokens = resp.usage.input_tokens
output_tokens = resp.usage.output_tokens
used_tokens = input_tokens + output_tokens
max_tokens = config["max_context_tokens"]

print(f"Claude: {used_tokens/1000:.1f}k tokens utilizados de {max_tokens/1000:.1f}k tokens")
```

---

## 7. 📊 Configurações e Limites

### 7.1. ChatGPT

`config/chatgpt_config.yaml`

```yaml
model: gpt-4o-mini
max_context_tokens: 8000
temperature: 0.2
```

### 7.2. Claude

`config/claude_config.yaml`

```yaml
model: claude-3-sonnet
max_context_tokens: 80000
temperature: 0.3
```

Esses valores definem os limites que serão usados na exibição e controle de tokens no terminal.

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
  "claude": {
    "model": "claude-3-sonnet",
    "used_tokens": 50213,
    "max_context_tokens": 80000
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
[OK] Etapa 2 (Claude) concluída. Estudo final em data/sessions/2025-11-07_14-33/03_final/estudo_final.md
Claude: 50.2k tokens utilizados de 80.0k tokens
```

---

## 10. 🧩 Componentes-Chave do Planejamento

| **Componente**         | **Responsabilidade**                                  |
| ---------------------- | ----------------------------------------------------- |
| `run_pipeline.py`      | Ponto único de entrada via terminal                   |
| `orchestrator.py`      | Coordena as etapas e exibe tokens                     |
| `chatgpt_stage.py`     | Coleta e organiza dados conforme fontes confiáveis    |
| `claude_stage.py`      | Produz o estudo final com base nos arquivos coletados |
| `fontes_confiaveis.md` | Lista de URLs obrigatórias e exclusivas               |
| `meta.json`            | Registro de uso de tokens e metadados                 |
| `prompts/*.md`         | Regras explícitas que guiam as decisões das IAs       |
| `config/*.yaml`        | Limites e parâmetros dos modelos                      |

---

## 11. 🚀 Próximos Passos

1. Criar os arquivos `prompts/*.md` conforme o modelo descrito.
2. Preencher `fontes_confiaveis.md` com as URLs desejadas.
3. Configurar as chaves da API em `.env`.
4. Implementar as funções básicas de cada etapa (`chatgpt_stage`, `claude_stage`, `orchestrator`, `run_pipeline`).
5. Testar o fluxo completo com uma tarefa real.

---

✅ **Resumo final:**
Este sistema cria um **pipeline automatizado, local e controlado**, onde o ChatGPT atua como **coletor de dados confiáveis** (obedecendo a uma lista fixa de fontes) e o Claude como **sintetizador analítico**. Ambos trabalham sob regras explícitas de comportamento, formatação e limitação de tokens, com total rastreabilidade e controle sobre o processo de ponta a ponta.
