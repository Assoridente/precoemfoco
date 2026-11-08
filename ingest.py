"""Converte a tabela 6723 fornecida em registros CSV rastreáveis, sem dependências."""
import csv
from pathlib import Path
import xml.etree.ElementTree as ET
from zipfile import ZipFile

ROOT = Path(__file__).resolve().parent
NS = {'s': 'http://schemas.openxmlformats.org/spreadsheetml/2006/main'}
KINDS = ['mensal', 'acumulado_ano', 'anual', 'numero_indice']

def convert(source=ROOT / 'IndicesPreços/IndicesPreços.xlsx', target=ROOT / 'data/indices.csv'):
    records = []
    with ZipFile(source) as z:
        strings = [''.join(t.text or '' for t in item.findall('.//s:t', NS))
                   for item in ET.fromstring(z.read('xl/sharedStrings.xml')).findall('s:si', NS)]
        for sheet, kind in enumerate(KINDS, 1):
            xml = ET.fromstring(z.read(f'xl/worksheets/sheet{sheet}.xml'))
            rows = {}
            for row in xml.findall('.//s:row', NS):
                cells = {}
                for cell in row:
                    value = cell.find('s:v', NS)
                    text = value.text or '' if value is not None else ''
                    if cell.get('t') == 's' and text:
                        text = strings[int(text)]
                    column = ''.join(c for c in cell.get('r') if c.isalpha())
                    cells[column] = text
                rows[int(row.get('r'))] = cells
            month = ''
            for col, group in rows[5].items():
                month = rows[4].get(col, month)
                raw = rows[6].get(col, '')
                try:
                    value = str(float(raw)) if raw != '-' else '0.0'
                except ValueError:
                    value = ''
                records.append(dict(tipo=kind, periodo=month, grupo=group, valor=value,
                                    original=raw, fonte='IBGE - Tabela 6723',
                                    celula=f'sheet{sheet}!{col}6'))
    target.parent.mkdir(parents=True, exist_ok=True)
    with target.open('w', encoding='utf-8', newline='') as f:
        writer = csv.DictWriter(f, fieldnames=records[0].keys())
        writer.writeheader()
        writer.writerows(records)
    return records

if __name__ == '__main__':
    data = convert()
    print(f'{len(data)} registros convertidos para data/indices.csv')
