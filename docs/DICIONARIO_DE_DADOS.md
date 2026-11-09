# Dicionário de dados

Arquivo: `data/indices.csv`. Codificação UTF-8, cabeçalho na primeira linha, separador vírgula e ponto como separador decimal. Textos que contêm vírgulas são delimitados conforme as regras CSV.

Cada linha representa uma observação de um indicador, de um grupo industrial e de um mês para o Brasil. A combinação `tipo` + `periodo` + `grupo` identifica a observação na base atual.

| Campo | Conteúdo | Exemplo | Regra |
| --- | --- | --- | --- |
| `tipo` | Indicador da observação | `mensal` | `mensal`, `acumulado_ano`, `anual` ou `numero_indice` |
| `periodo` | Mês e ano de referência | `janeiro 2019` | Texto em português; não é uma data ISO |
| `grupo` | Código e descrição do grupo industrial | `105 Laticínios` | Preserva a identificação do arquivo original |
| `valor` | Valor numérico normalizado | `5.69` | Vazio quando indisponível; não armazena `%` |
| `original` | Conteúdo original da célula | `5.69` ou `...` | Preservado para conferência e interpretação dos símbolos |
| `fonte` | Origem declarada do dado | `IBGE - Tabela 6723` | Mesma fonte nos registros da base atual |
| `celula` | Aba e célula do XLSX | `sheet1!K6` | Referência à origem, não à linha do CSV |

## Exemplo de registro

```csv
tipo,periodo,grupo,valor,original,fonte,celula
mensal,janeiro 2019,105 Laticínios,5.69,5.69,IBGE - Tabela 6723,sheet1!K6
```

O valor corresponde a 5,69% porque o tipo é `mensal`. Um valor de `100` para `numero_indice` representa a base do índice, não uma variação de 100%.

## Validação e atualização

Os testes automatizados verificam a reprodução dos registros a partir da planilha, um valor e célula conhecidos, o tratamento de indisponibilidade e uma comparação entre todos os grupos do mês. A contagem esperada da base atual é 2.256.

Se a estrutura ou a cobertura da planilha mudar, revise o conversor, os testes, a descrição da base e os números exibidos na interface. A aplicação lê o CSV na inicialização: reinicie o servidor depois de regenerá-lo.
