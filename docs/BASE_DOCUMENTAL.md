# Base documental — Preço em Foco

## Cenário do desafio

Uma equipe de análise precisa consultar os índices de preços ao produtor de diferentes grupos industriais. Procurar cada valor nas abas de uma planilha exige conhecer sua estrutura, localizar o período e distinguir os indicadores. O Preço em Foco permite fazer essas consultas em português e conferir as células que sustentam a resposta.

Este cenário é uma aplicação acadêmica. Não representa uma contratação real nem uma ferramenta oficial do IBGE.

## Documento escolhido

- **Original:** `IndicesPreços/IndicesPreços.xlsx`, fornecido para o projeto.
- **Fonte declarada na planilha:** IBGE — Índice de Preços ao Produtor, tabela 6723.
- **Documento consultado pela aplicação:** `data/indices.csv`, extraído da planilha por `ingest.py`.
- **Localidade:** Brasil.
- **Período:** dezembro de 2018 a setembro de 2026, 94 meses.
- **Dimensões:** seis grupos industriais e quatro indicadores.
- **Quantidade:** 2.256 registros, incluindo observações com valores indisponíveis.

O período descreve o arquivo fornecido. A aplicação não busca novos dados no site do IBGE.

## Indicadores

| Identificador | Comparação | Unidade |
| --- | --- | --- |
| `mensal` | Mês contra o mês imediatamente anterior | % |
| `acumulado_ano` | Mês contra dezembro do ano anterior | % |
| `anual` | Mês contra o mesmo mês do ano anterior | % |
| `numero_indice` | Número-índice com base dezembro de 2018 = 100 | pontos de índice |

Os indicadores não são intercambiáveis. Uma variação mensal não deve ser apresentada como variação anual. O número-índice não é um preço em reais.

## Grupos disponíveis

| Código | Descrição presente na base |
| --- | --- |
| 101 | Abate e fabricação de produtos de carne |
| 104 | Fabricação de óleos e gorduras vegetais e animais |
| 105 | Laticínios |
| 106 | Moagem, fabricação de produtos amiláceos e de alimentos para animais |
| 107 | Fabricação e refino de açúcar |
| 108 | Torrefação e moagem de café |

## Processamento e rastreabilidade

1. O conversor abre o XLSX como um arquivo ZIP e lê os textos e células XML.
2. Processa as quatro primeiras abas. A aba de notas não é carregada como conteúdo consultável pelo agente.
3. Associa cada grupo ao mês indicado no cabeçalho, propagando o mês entre as colunas de um mesmo bloco.
4. Gera um registro para cada combinação de indicador, período e grupo.
5. Mantém o conteúdo original da célula e registra a coordenada correspondente.

O arquivo original permanece preservado. A conversão pode ser reproduzida com `python ingest.py`.

As referências `sheet1`, `sheet2`, `sheet3` e `sheet4` identificam, respectivamente, as abas de variação mensal, acumulado no ano, variação anual e número-índice. Por exemplo, `sheet1!K6` é a origem do valor mensal de laticínios em janeiro de 2019: 5,69%.

## Valores indisponíveis

O campo `original` preserva símbolos como `...`. Se o conteúdo não puder ser interpretado como número, `valor` fica vazio e o agente informa a indisponibilidade. Esses registros não entram nas comparações de maior e menor.

O símbolo `-` é tratado como zero absoluto, de acordo com a legenda da planilha. Um zero numérico também é mantido como zero; ausência de dado não é transformada em zero.

## Limites da base e das respostas

O agente consulta um único mês e ano por pergunta. Pode retornar um grupo ou comparar os seis grupos disponíveis. Não estima dados ausentes, prevê índices, calcula correção monetária ou identifica causas econômicas das variações. Também não responde sobre preços de varejo, vendas, receitas ou produtos individuais.

A geração com Gemini usa os registros recuperados, mas sua redação pode conter erros. As fontes permitem conferir os números na planilha.

## Relação com as sugestões da Alura

Políticas de devolução, termos de uso e documentos de atendimento são exemplos de bases para outros cenários. Neste projeto, a base é uma tabela de indicadores industriais. O CSV atende ao formato de documento previsto no enunciado fornecido; não é necessário inventar políticas de uma loja ou de um banco.

Este documento, o dicionário de dados e o FAQ explicam a solução para quem vai usar ou avaliar o projeto. Eles não são carregados automaticamente pelo agente. O conteúdo consultado em execução continua sendo `data/indices.csv`.
