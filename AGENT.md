# AGENT.md

Este arquivo fornece instruções para o agente de desenvolvimento que trabalha no repositório **"ia-workflow-pipeline"**.

---

## 1. Visão Geral do Projeto

O objetivo deste projeto é criar um **pipeline local automatizado** que integre duas IAs — **ChatGPT (OpenAI)** e **Gemini (Google)** — para executar tarefas de **coleta, análise e geração de estudos estruturados** a partir de fontes confiáveis pré-definidas.

O ChatGPT será responsável por **buscar e organizar dados** a partir de URLs contidas em `fontes_confiaveis.md`, enquanto o Gemini será encarregado de **interpretar e montar o estudo final**, seguindo um formato fixo de relatório.

O agente deve garantir que:

* O fluxo funcione **de ponta a ponta com um único comando de terminal**.
* Todo o código seja **modular, documentado e rastreável**.
* O uso de tokens de cada modelo seja **registrado e exibido no terminal**.

---

## 2. Fluxo de Trabalho de Desenvolvimento

Siga estas etapas ao implementar novos recursos, corrigir erros ou atualizar o pipeline:

1. **Entenda o escopo da tarefa**
   Leia cuidadosamente a solicitação do usuário para compreender o propósito da modificação.
   Avalie se ela afeta o comportamento do ChatGPT, do Gemini ou do orquestrador principal.

2. **Explore a estrutura do projeto**
   Antes de codar, familiarize-se com a árvore de diretórios.

3. **Planeje a execução**
   Crie um plano usando a ferramenta `set_plan`.
   O plano deve descrever as etapas de implementação, teste e integração com as APIs da OpenAI e Google.

4. **Implemente as alterações**
   Mantenha compatibilidade com o fluxo `run_pipeline.py → orchestrator.py → chatgpt_stage.py → gemini_stage.py`.

5. **Adicione logs e verificações**
   Cada função deve registrar no terminal o progresso e a quantidade de tokens utilizados.

6. **Execute e valide o fluxo completo**
   Teste o pipeline com uma tarefa real, por exemplo:

   ```bash
   python run_pipeline.py "Impacto da IA na educação básica no Brasil"
   ```

   Certifique-se de que o resultado contenha os diretórios `01_raw/` e `03_final/`, além do `meta.json`.

---

## 3. Convenções de Codificação

* **Nomenclatura:**
  * Use nomes descritivos (`run_chatgpt_stage`, `run_gemini_stage`, `save_meta`, etc.).

---

## 5. Commits e Pull Requests

* **Exemplo de Mensagem de Commit:**

    ```
    feat: adicionar exibição de tokens no terminal

    Agora o ChatGPT e Gemini exibem o uso de tokens após cada execução.
    ```

---

## 7. Diretrizes Específicas do Projeto

2. **Prompts e Instruções:**
   * O comportamento do ChatGPT e Gemini deve ser controlado unicamente pelos arquivos de prompt, não pelo código.

3. **Contagem de Tokens:**
   * Cada etapa (ChatGPT e Gemini) deve imprimir no terminal:

     ```
     ChatGPT: Xk tokens utilizados de Yk tokens
     Gemini: Xk tokens utilizados de Yk tokens
     ```
   * O `meta.json` da sessão deve registrar esses dados.

4. **Padrões de Saída:**
   * ChatGPT → `01_raw/summary.md`, `sources.json`, `notes/`
   * Gemini → `03_final/estudo_final.md`

5. **Ambiente Local:**
   * As chaves das APIs devem ser configuradas em `.env`:

     ```
     OPENAI_API_KEY=...
     GOOGLE_API_KEY=...
     ```

---
(O restante do documento permanece o mesmo)
