#!/usr/bin/env bash
set -euo pipefail
export DEBIAN_FRONTEND=noninteractive
sudo apt-get update -qq
sudo apt-get install -y docker.io git
sudo systemctl enable --now docker
if [ ! -d "$HOME/precoemfoco/.git" ]; then
  git clone https://github.com/Assoridente/precoemfoco.git "$HOME/precoemfoco"
fi
cd "$HOME/precoemfoco"
git pull --ff-only
test -s "$HOME/precoemfoco.env"
chmod 600 "$HOME/precoemfoco.env"
sudo docker build -t preco-em-foco .
sudo docker run -d --name preco-em-foco --restart unless-stopped --env-file "$HOME/precoemfoco.env" -p 8000:8000 preco-em-foco
# Adiciona somente a porta da aplicação, sem remover regras existentes.
if command -v iptables >/dev/null 2>&1; then
  sudo iptables -C INPUT -p tcp --dport 8000 -j ACCEPT 2>/dev/null || sudo iptables -I INPUT 1 -p tcp --dport 8000 -j ACCEPT
  if command -v netfilter-persistent >/dev/null 2>&1; then
    sudo netfilter-persistent save
  fi
fi
sleep 2
curl --fail --max-time 10 http://localhost:8000/health
