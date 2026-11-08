import json
import os
from http.server import BaseHTTPRequestHandler, ThreadingHTTPServer
from pathlib import Path
from agent import answer, load

ROOT = Path(__file__).resolve().parent
# Carrega .env sem sobrescrever as variáveis configuradas no servidor.
if (ROOT / '.env').exists():
    for line in (ROOT / '.env').read_text(encoding='utf-8').splitlines():
        if line.strip() and not line.lstrip().startswith('#') and '=' in line:
            k, v = line.split('=', 1)
            os.environ.setdefault(k.strip(), v.strip().strip('\"').strip("'"))
RECORDS = load()

class Handler(BaseHTTPRequestHandler):
    def send(self, status, body, content='application/json; charset=utf-8'):
        self.send_response(status)
        self.send_header('Content-Type', content)
        self.send_header('Content-Length', str(len(body)))
        self.send_header('X-Content-Type-Options', 'nosniff')
        self.end_headers()
        self.wfile.write(body)

    def do_GET(self):
        if self.path == '/':
            self.send(200, (ROOT / 'static/index.html').read_bytes(), 'text/html; charset=utf-8')
        elif self.path == '/health':
            self.send(200, json.dumps({'status': 'ok', 'registros': len(RECORDS)}).encode())
        else:
            self.send(404, b'{}')

    def do_POST(self):
        if self.path != '/api/ask':
            return self.send(404, b'{}')
        try:
            size = int(self.headers.get('Content-Length', '0'))
            if not 0 < size <= 8192:
                raise ValueError('Requisição inválida.')
            data = json.loads(self.rfile.read(size))
            if not isinstance(data, dict) or not isinstance(data.get('pergunta'), str):
                raise ValueError('Informe uma pergunta em texto.')
            result = answer(data['pergunta'], RECORDS)
            self.send(200, json.dumps(result, ensure_ascii=False).encode())
        except (ValueError, TypeError):
            self.send(400, json.dumps({'erro': 'Informe uma pergunta válida de até 1.000 caracteres.'}).encode())

if __name__ == '__main__':
    port = int(os.getenv('PORT', '8000'))
    print(f'Preço em Foco: http://localhost:{port}', flush=True)
    ThreadingHTTPServer(('0.0.0.0', port), Handler).serve_forever()
