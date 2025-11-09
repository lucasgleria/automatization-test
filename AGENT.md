# AGENT.md

Este arquivo fornece instruções para o agente de desenvolvimento que trabalha no repositório "automatization-test".

## 1. Visão Geral do Projeto

O objetivo deste projeto é criar uma suíte de automação de testes robusta e de fácil manutenção. Espera-se que o agente escreva scripts de automação limpos, eficientes e bem documentados.

## 2. Fluxo de Trabalho de Desenvolvimento

Siga estas etapas ao implementar novos recursos ou corrigir bugs:

1.  **Entenda os requisitos**: Leia atentamente a solicitação do usuário para entender completamente o escopo da tarefa.
2.  **Explore a base de código**: Antes de escrever qualquer código, explore os arquivos existentes para entender a estrutura e os padrões do projeto. Use `ls -F` e `read_file`.
3.  **Crie um plano**: Crie um plano passo a passo usando a ferramenta `set_plan`. O plano deve incluir etapas para escrever código, escrever testes e verificação.
4.  **Implemente as alterações**: Escreva o código seguindo as convenções de codificação definidas abaixo.
5.  **Escreva testes**: Todos os novos recursos devem ser acompanhados por testes.
6.  **Execute os testes**: Execute todos os testes para garantir que suas alterações estejam corretas e não tenham introduzido regressões.
7.  **Envie para revisão**: Assim que todos os testes passarem, envie suas alterações.

## 3. Convenções de Codificação

-   **Linguagem**: A linguagem principal para este projeto é JavaScript/TypeScript.
-   **Estilo**: Siga um estilo de código consistente. Use um linter e formatador, se disponível.
-   **Nomenclatura**: Use nomes descritivos para variáveis, funções e arquivos.
-   **Comentários**: Adicione comentários para explicar lógicas complexas.

## 4. Testes

-   **Framework**: Use o framework de teste designado para o projeto (por exemplo, Jest, Mocha, Cypress).
-   **Cobertura**: Busque uma alta cobertura de testes.
-   **Asserções**: Use asserções significativas para tornar os testes claros e eficazes.
-   **Executando testes**: Para executar os testes, execute o comando especificado em `package.json`, por exemplo `npm test`.

## 5. Commits e Pull Requests

-   **Mensagens de Commit**: Escreva mensagens de commit claras e concisas. A primeira linha deve ser um resumo da alteração (máx. 50 caracteres), seguida por uma linha em branco e uma explicação mais detalhada, se necessário.
-   **Pull Requests**: Crie pull requests com um título e uma descrição claros das alterações.

## 6. Verificações Programáticas

Antes de enviar seu trabalho, você DEVE executar as seguintes verificações e garantir que elas passem.

1.  **Linting**: Execute o linter para verificar problemas de estilo de código.
    ```bash
    npm run lint
    ```
2.  **Testes**: Execute toda a suíte de testes para garantir que todos os testes estejam passando.
    ```bash
    npm test
    ```
Se alguma dessas verificações falhar, você deve corrigir os problemas antes de enviar.
