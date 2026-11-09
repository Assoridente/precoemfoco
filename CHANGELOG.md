# Histórico de versões

As versões registram as etapas reais deste projeto. Os commits posteriores à base inicial foram organizados por assunto a partir das alterações feitas durante o desenvolvimento, sem alterar datas ou inventar etapas anteriores.

## v1.1.0 — Deploy na OCI

- Aplicação publicada em OCI Compute com Docker, Ubuntu 24.04 e acesso público na porta 8000.
- Validação externa do endpoint de saúde e de resposta Gemini com fontes da base.
- Roteiro atualizado para a hospedagem de demonstração com créditos de avaliação.

## v1.0.0 — Documentação da versão local

- Descrição da base documental, dicionário de dados e FAQ.
- Evidência do teste local com Gemini.
- Orientações para execução e deploy na OCI.
- Proteção de arquivos de ambiente e chaves SSH no Git.

Esta versão conclui a implementação local. O deploy e a evidência na OCI permanecem pendentes.

## v0.3.0 — Interface preta e roxa

- Layout responsivo, painel da base e sugestões de perguntas.
- Transições, animação de carregamento e entrada da resposta.
- Preferência por movimento reduzido e envio com Ctrl+Enter.
- Exibição organizada de fontes e avisos do provedor.

## v0.2.0 — Diagnóstico da integração

- Mensagens de falhas HTTP, conexão e tempo de espera sem expor credenciais.
- Preservação da resposta local caso Gemini falhe.
- Script de diagnóstico e teste automatizado do fallback.
- Leitura de `.env` com suporte a UTF-8 com BOM e encerramento limpo por Ctrl+C.

## v0.1.0 — Base inicial

- Conversão do XLSX em CSV rastreável.
- Consulta estruturada dos indicadores e integração Gemini.
- Interface inicial, testes, Dockerfile e roteiro OCI.
