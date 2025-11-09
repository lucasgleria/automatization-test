# AGENT.md

Este arquivo fornece instruções para o agente de desenvolvimento que trabalha no repositório **"ia-workflow-pipeline"**.

---

## 1. Visão Geral do Projeto

O objetivo deste projeto é criar um **pipeline local automatizado** que integre duas IAs — **ChatGPT (OpenAI)** e **Claude (Anthropic)** — para executar tarefas de **coleta, análise e geração de estudos estruturados** a partir de fontes confiáveis pré-definidas.

O ChatGPT será responsável por **buscar e organizar dados** a partir de URLs contidas em `fontes_confiaveis.md`, enquanto o Claude será encarregado de **interpretar e montar o estudo final**, seguindo um formato fixo de relatório.

O agente deve garantir que:

* O fluxo funcione **de ponta a ponta com um único comando de terminal**.
* Todo o código seja **modular, documentado e rastreável**.
* O uso de tokens de cada modelo seja **registrado e exibido no terminal**.

---

## 2. Fluxo de Trabalho de Desenvolvimento

Siga estas etapas ao implementar novos recursos, corrigir erros ou atualizar o pipeline:

1. **Entenda o escopo da tarefa**
   Leia cuidadosamente a solicitação do usuário para compreender o propósito da modificação.
   Avalie se ela afeta o comportamento do ChatGPT, do Claude ou do orquestrador principal.

2. **Explore a estrutura do projeto**
   Antes de codar, familiarize-se com a árvore de diretórios:

   ```
   config/
   prompts/
   workflow/
   data/
   ```

   Use `ls -F` e `read_file` para inspecionar arquivos e entender a hierarquia.

3. **Planeje a execução**
   Crie um plano usando a ferramenta `set_plan`.
   O plano deve descrever as etapas de implementação, teste e integração com as APIs da OpenAI e Anthropic.

4. **Implemente as alterações**
   Adicione ou modifique módulos seguindo as convenções abaixo (seções 3 e 4).
   Mantenha compatibilidade com o fluxo `run_pipeline.py → orchestrator.py → chatgpt_stage.py → claude_stage.py`.

5. **Adicione logs e verificações**
   Cada função deve registrar no terminal o progresso e a quantidade de tokens utilizados.

6. **Execute e valide o fluxo completo**
   Teste o pipeline com uma tarefa real, por exemplo:

   ```bash
   python run_pipeline.py "Impacto da IA na educação básica no Brasil"
   ```

   Certifique-se de que o resultado contenha os diretórios `01_raw/` e `03_final/`, além do `meta.json`.

7. **Envie para revisão**
   Após validar o fluxo e garantir que não houve regressões, envie as alterações para análise.

---

## 3. Convenções de Codificação

* **Linguagem:** Python 3.10+
* **Estilo:** Utilize `black` e `flake8` para formatação e linting.
* **Estrutura:**

  * Cada módulo deve ter uma função principal (`run_*_stage`) e funções auxiliares documentadas.
  * As funções devem retornar tuplas `(resultado, usage_dict)` para permitir o cálculo e exibição de tokens.
* **Nomenclatura:**

  * Use nomes descritivos (`run_chatgpt_stage`, `run_claude_stage`, `save_meta`, etc.).
* **Comentários e Docstrings:**

  * Use docstrings (`"""Descrição da função"""`) em todas as funções públicas.
  * Inclua comentários explicando a lógica de etapas críticas (como parsing de prompts ou chamadas de API).

---

## 4. Testes

### 4.1. Estrutura de Testes

* Todos os novos recursos devem incluir testes unitários em `tests/`.
* Os testes devem verificar:

  * Geração correta de arquivos de saída (`summary.md`, `sources.json`, `estudo_final.md`);
  * Presença de logs de token no terminal;
  * Leitura correta de `fontes_confiaveis.md`.

### 4.2. Framework de Teste

* Utilize **pytest** como framework padrão.

### 4.3. Exemplos de Comandos

```bash
pytest -v
```

---

## 5. Commits e Pull Requests

* **Mensagens de Commit:**

  * Primeira linha: resumo curto (máx. 50 caracteres).
  * Corpo: explicação detalhada, se necessário.
  * Exemplo:

    ```
    feat: adicionar exibição de tokens no terminal

    Agora o ChatGPT e Claude exibem o uso de tokens após cada execução.
    ```
* **Pull Requests:**

  * Inclua título e descrição claros.
  * Mencione a funcionalidade ou módulo alterado (ex: `workflow/chatgpt_stage.py`).

---

## 6. Verificações Programáticas

Antes de enviar seu trabalho, execute **todas as verificações obrigatórias**:

1. **Linting:**

   ```bash
   black . && flake8 .
   ```
2. **Testes:**

   ```bash
   pytest
   ```
3. **Execução manual do pipeline:**

   ```bash
   python run_pipeline.py "Teste de integração IA"
   ```

Certifique-se de que:

* O pipeline roda sem erros.
* Os arquivos esperados são gerados.
* Os tokens utilizados são exibidos corretamente no terminal.

---

## 7. Diretrizes Específicas do Projeto

1. **Fontes Confiáveis (`prompts/fontes_confiaveis.md`):**

   * O ChatGPT **deve usar exclusivamente** as URLs listadas nesse arquivo.
   * O código deve ler esse arquivo e injetar as URLs no `system prompt` automaticamente.
   * Nenhuma fonte externa pode ser consultada.

2. **Prompts e Instruções:**

   * Todos os prompts (`*.md`) devem permanecer modulares e editáveis.
   * O comportamento do ChatGPT e Claude deve ser controlado unicamente pelos arquivos de prompt, não pelo código.

3. **Contagem de Tokens:**

   * Cada etapa (ChatGPT e Claude) deve imprimir no terminal:

     ```
     ChatGPT: Xk tokens utilizados de Yk tokens
     Claude: Xk tokens utilizados de Yk tokens
     ```
   * O `meta.json` da sessão deve registrar esses dados.

4. **Padrões de Saída:**

   * ChatGPT → `01_raw/summary.md`, `sources.json`, `notes/`
   * Claude → `03_final/estudo_final.md`

5. **Ambiente Local:**

   * As chaves das APIs devem ser configuradas em `.env`:

     ```
     OPENAI_API_KEY=...
     ANTHROPIC_API_KEY=...
     ```

6. **Resiliência e Logs:**

   * Em caso de erro, o pipeline deve interromper o fluxo e registrar o erro no terminal e em `data/sessions/{id}/logs/`.

---

## 8. Objetivo do Agente

O agente de desenvolvimento deve garantir que o projeto:

* Seja **totalmente automatizado e local**;
* Produza resultados **consistentes, rastreáveis e auditáveis**;
* Permita fácil manutenção, expansão e customização;
* Respeite integralmente os princípios do planejamento principal (coleta → análise → estudo).
