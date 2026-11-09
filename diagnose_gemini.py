"""Diagnóstico manual: não imprime chaves nem cabeçalhos de autenticação."""
import json
import os
import re
from urllib.error import HTTPError, URLError
from urllib.request import Request, urlopen
import app  # carrega configuração .env

def main():
    key = os.getenv('GEMINI_API_KEY', '')
    model = os.getenv('GEMINI_MODEL', '')
    print('Chave configurada:', bool(key), '| Modelo:', model)
    if not key or not model:
        return
    base = 'https://generativelanguage.googleapis.com/v1beta/'
    for label, path, data in [
        ('Listar modelos', 'models', None),
        ('Gerar resposta simples', f'models/{model}:generateContent',
         {'contents': [{'parts': [{'text': 'Responda apenas: OK'}]}]}),
    ]:
        req = Request(base + path, data=json.dumps(data).encode() if data else None,
                      headers={'Content-Type': 'application/json', 'x-goog-api-key': key})
        try:
            with urlopen(req, timeout=20) as response:
                payload = json.load(response)
            if data:
                text = ''.join(p.get('text', '') for c in payload.get('candidates', [])
                               for p in c.get('content', {}).get('parts', []))
                print(label, 'OK:', text[:200])
            else:
                names = [m['name'] for m in payload.get('models', [])]
                print(label, 'OK; modelo encontrado:', 'models/' + model in names)
        except HTTPError as exc:
            raw = exc.read(32768).decode('utf-8', errors='replace')
            try:
                detail = json.loads(raw).get('error', {}).get('message', '')
            except ValueError:
                detail = 'Resposta não JSON do servidor.'
            safe = detail.replace(key, '[CHAVE OMITIDA]')
            safe = re.sub(r'(?:AIza|AQ\.)[\w.-]+', '[CHAVE OMITIDA]', safe)
            print(label, 'HTTP', exc.code, safe[:1500])
        except URLError as exc:
            print(label, 'falha de rede:', type(exc.reason).__name__, str(exc.reason).replace(key, '[CHAVE OMITIDA]'))
        except TimeoutError:
            print(label, 'tempo limite de 20 segundos atingido')

if __name__ == '__main__':
    main()
