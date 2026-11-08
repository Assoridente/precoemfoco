# Deploy na Oracle Cloud Infrastructure

Este roteiro prepara uma demonstração em OCI Compute. A instância, a conta e o deploy não foram criados automaticamente. Confirme preços e limites da sua conta antes de provisionar.

## 1. Preparar a instância

Crie uma VM Ubuntu compatível com Docker, em subnet pública, com IP público e rota para Internet Gateway. Guarde sua chave SSH. Para SSH, permita TCP 22 somente a partir do seu IP. Para uma demonstração acessível publicamente na porta 8000, configure ingresso TCP 8000 na security list ou NSG associado à VM, origem `0.0.0.0/0`. Remova essa regra quando encerrar a demonstração.

A camada de rede da OCI e o firewall do sistema operacional precisam permitir a porta, conforme a [documentação de regras de segurança OCI](https://docs.oracle.com/en-us/iaas/Content/Network/Concepts/securityrules.htm). Não abra todas as portas.

## 2. Conectar e instalar Docker

Na sua máquina, substitua os caminhos e o IP:

```bash
ssh -i CAMINHO_DA_CHAVE ubuntu@IP_PUBLICO
```

Na VM Ubuntu:

```bash
sudo apt-get update
sudo apt-get install -y docker.io git
sudo systemctl enable --now docker
git clone https://github.com/SEU_USUARIO/preco-em-foco.git
cd preco-em-foco
cp .env.example .env
nano .env
```

Preencha `GEMINI_API_KEY` e `GEMINI_MODEL`. Mantenha `PORT=8000` e proteja o arquivo:

```bash
chmod 600 .env
sudo docker build -t preco-em-foco .
sudo docker run -d --name preco-em-foco --restart unless-stopped --env-file .env -p 8000:8000 preco-em-foco
curl http://localhost:8000/health
```

Se UFW estiver ativo, permita `8000/tcp` com `sudo ufw allow 8000/tcp`. Preserve o acesso SSH antes de alterar firewall. Não é necessário ativar ou desativar o firewall inteiro.

## 3. Validar de fora da VM

Abra `http://IP_PUBLICO:8000` no navegador da sua máquina. Confirme também `http://IP_PUBLICO:8000/health`. Faça a pergunta “Qual foi a variação mensal de laticínios em janeiro de 2019?”. Confira o valor 5,69%, a célula sheet1!K6 e o modo `RAG estruturado + Gemini`.

Se falhar, verifique: IP público, rota da subnet, ingresso do NSG/security list, firewall da VM, `sudo docker ps` e `sudo docker logs preco-em-foco`. Se só o Gemini falhar, verifique chave, identificador do modelo, quota e saída HTTPS da VM.

## 4. Registrar a evidência

Capture o navegador com a URL pública visível, pergunta, resposta, fontes e modo Gemini. Salve a imagem em `docs/evidencias/oci.png` e acrescente no README:

```markdown
Aplicação na OCI: [Preço em Foco](http://SEU_IP_PUBLICO:8000)
![Agente respondendo na OCI](docs/evidencias/oci.png)
```

Registre a data do teste. Não inclua chaves, tokens ou arquivos `.env` na imagem ou no GitHub. Um print local ou do painel da VM sem a aplicação respondendo não demonstra a aplicação funcionando publicamente.

Para uso contínuo, coloque a aplicação atrás de proxy HTTPS e configure autenticação, limite de requisições e alertas de consumo do provedor. Ao encerrar o projeto, remova os recursos desnecessários para evitar cobrança.
