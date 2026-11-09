# FAQ — Preço em Foco

## O que posso perguntar?

Você pode consultar um indicador de um grupo industrial em um mês e ano, ou comparar os grupos disponíveis no mesmo período.

- Qual foi a variação mensal de laticínios em janeiro de 2019?
- Qual grupo teve a maior variação mensal em janeiro de 2019?
- Qual foi a variação acumulada no ano do açúcar em dezembro de 2020?
- Qual o número-índice do café em setembro de 2026?
- Qual período e quais grupos existem na base?

## Como escrever uma pergunta?

Informe o indicador, o mês e o ano. Use o nome do grupo ou seu código, como `105` para laticínios. Sem um grupo específico, a aplicação consulta todos os seis grupos do mês.

## O que significa a resposta de 5,69% para laticínios em janeiro de 2019?

É o valor da variação mensal registrado para o grupo 105 naquele período. A origem é a tabela 6723 do IBGE, primeira aba da planilha, célula K6. O dado não informa o preço de uma embalagem de leite nem uma variação de vendas.

## Por que o agente pede um mês ou um indicador?

A consulta precisa distinguir variação mensal, acumulada no ano, anual e número-índice. O sistema foi implementado para um único mês e ano por pergunta; períodos amplos ou comparações entre datas precisam ser reformulados.

## O que acontece quando um valor está indisponível?

O agente informa a indisponibilidade e preserva o símbolo original. Não inventa um valor nem o substitui por zero. Um ranking considera somente os valores disponíveis no recorte e informa os grupos empatados.

## Como conferir uma resposta?

Abra “Conferir fontes da resposta”. Cada item mostra a fonte, o grupo, o período, o tipo do indicador, o valor original e a célula na planilha. As citações `[1]`, `[2]` e seguintes correspondem a esses registros.

## Qual a diferença entre os modos exibidos?

| Modo | Funcionamento |
| --- | --- |
| RAG estruturado + Gemini | Recupera os registros e usa Gemini para redigir a resposta |
| Consulta local, sem LLM | Usa regras e valores da base, sem geração por modelo |
| Consulta local, Gemini indisponível | A chamada ao provedor falhou e o sistema preservou a resposta local |

Consultas sobre a cobertura da base e pedidos de esclarecimento são respondidos localmente.

## O agente consulta a internet ou atualiza os índices?

Não. A fonte numérica é o CSV preparado a partir da planilha fornecida. A chamada ao Gemini serve para redigir a resposta com o contexto recuperado, sem busca na web.

## Ele consegue explicar por que um índice aumentou?

A base não contém causas econômicas. O agente não deve atribuir uma causa ao movimento nem fazer previsões com esses dados.

## Posso perguntar sobre uma política de reembolso ou de privacidade?

Esse conteúdo não faz parte da base atual. O projeto foi personalizado para indicadores industriais; as sugestões de documentos de lojas, escolas e bancos pertencem a outros cenários do desafio.

## Por que apareceu um aviso do Gemini?

A API pode rejeitar uma chave, negar acesso a um modelo, atingir uma quota ou demorar para responder. Confira o aviso exibido, a configuração do `.env` e os limites do projeto no AI Studio. Reinicie o servidor ao alterar a configuração. Nunca compartilhe a chave no chat, em prints ou no GitHub.

## A aplicação salva minhas perguntas?

O código atual não implementa histórico persistente de perguntas. Quando Gemini está ativo, a pergunta e os registros recuperados são enviados ao provedor para geração. A aplicação não deve receber dados pessoais ou confidenciais desnecessários.

## O print local já comprova o deploy?

Não. Ele demonstra o funcionamento local. Para comprovar a OCI, publique a aplicação e registre uma resposta com a URL pública da instância visível. O roteiro está em [OCI.md](OCI.md).
