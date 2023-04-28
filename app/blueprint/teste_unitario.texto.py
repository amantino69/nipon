from flask import url_for
from utils import texto  # Importe seu objeto app Flask
import unittest
from unittest import TestCase

class TestTexto(TestCase):

    def setUp(self):
        pass

    def tearDown(self):
        pass

    def test_texto_success(self):
        # Inclua suas variáveis aqui, por exemplo:
        operadora = 'Example Operator'
        hoje = '2021-10-01'
        first_name = 'John'
        demanda = '45215425'
        situacao = 'respondido'

        with texto.test_request_context():
            result = texto(operadora, hoje, first_name, demanda, situacao)

        # Inclua suas verificações de teste (asserts) aqui
        # Por exemplo:
        self.assertTrue(result.startswith('amil','2021x-10-01', 'João Batista' , 'pondido'))

    # Adicione outros métodos de teste aqui, se necessário

    if __name__ == '__main__':
         unittest.main()
