from nameparser import HumanName
import re
import time
import os
import shutil
import genderbr
import pandas as pd
from flask import url_for

prefixo_pastas_word = 'C:/Users/amantino/Documents/NIPs'
prefixo_pastas_excel = 'C:/Users/amantino/Documents/fontes'
prefixo_fonte = 'C:/Users/amantino/documents/Minhas fontes de dados'

def criar_arquivo_resposta(operadora, hoje, first_name, demanda, situacao):
    name = HumanName(first_name)
    name.capitalize(force=True)

    origem_excel = (
        f'{prefixo_pastas_excel}/{hoje}/{operadora}/{name}/{demanda}/{name}.xlsx')
    destino_excel = (f'{prefixo_fonte}/fonte.xlsx')

    try:
        shutil.copyfile(origem_excel, destino_excel)
        os.startfile(
            f"{prefixo_pastas_word}/{hoje}/{operadora}/{name}/{demanda}/{name}.docx")
    except:
        print('Erro ao copiar o arquivo')

    return (url_for('webui.responder'))
