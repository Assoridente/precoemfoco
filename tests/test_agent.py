import unittest
from agent import answer, load
from ingest import convert
from tempfile import TemporaryDirectory
from pathlib import Path

class AgentTests(unittest.TestCase):
    def test_known_value_and_cell(self):
        r = answer('Qual a variação mensal de laticínios em janeiro de 2019?')
        self.assertEqual(r['fontes'][0]['valor'], '5.69')
        self.assertEqual(r['fontes'][0]['celula'], 'sheet1!K6')

    def test_unavailable_is_not_zero(self):
        r = answer('Qual a variação mensal de laticínios em dezembro de 2018?')
        self.assertIn('indisponível', r['resposta'])

    def test_missing_period(self):
        self.assertFalse(answer('Qual variação mensal em janeiro de 2040?')['fontes'])

    def test_ranking_complete_slice(self):
        r = answer('Qual grupo teve a maior variação mensal em janeiro de 2019?')
        self.assertEqual(len(r['fontes']), 6)
        self.assertIn('Destaque', r['resposta'])
        self.assertIn('105 Laticínios (5,69%)', r['resposta'])

    def test_explicit_indicator(self):
        self.assertIn('Informe o indicador', answer('Quanto custou leite em janeiro de 2019?')['resposta'])

    def test_conversion_preserves_all_records(self):
        with TemporaryDirectory() as d:
            records = convert(target=Path(d) / 'test.csv')
        self.assertEqual(records, load())
        self.assertEqual(len(records), 2256)

if __name__ == '__main__':
    unittest.main()
