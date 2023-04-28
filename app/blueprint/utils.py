import genderbr
from nameparser import HumanName
import shutil
from flask import url_for
import os
import datetime
from dotenv import load_dotenv

import pandas as pd

responder = []

load_dotenv()

prefixo_pastas_word = os.getenv("PREFIXO_PASTAS_WORD")
prefixo_pastas_excel = os.getenv("PREFIXO_PASTAS_EXCEL")
prefixo_fonte = os.getenv("PREFIXO_FONTE")
prefixo_pasta_downloads = os.getenv("PREFIXO_PASTA_DOWNLOADS")
prefixo_pasta_documentos = os.getenv("PREFIXO_PASTA_DOCUMENTOS")
email_padrao = os.getenv("EMAIL_PADRAO")
password_padrao = os.getenv("PASSWORD_PADRAO")


def find_gender(nome):
    first_name = nome.split(" ")[0]
    genero = genderbr.get_gender(first_name)
    return genero

    # O recurso Mala Direta do Office espera que a fonte de dados esteja sempre
    # na pasta \Documents\Minhas fontes de dados.
    # Esse módulo copia a fonte de dados específica de um determinado beneficiário
    # para a pasta \Documents\Minhas fontes de dados antes de realizar a mesclagem


def texto(operadora, hoje, first_name, demanda, situacao):
    print("=========================================", f"Operadora: {operadora}")
    print("=========================================", f"Hoje: {hoje}")
    print("=========================================", f"Nome: {first_name}")
    print("=========================================", f"Demanda: {demanda}")
    print("=========================================", f"Situação: {situacao}")

    hoje = datetime.datetime.now().strftime("%d/%m/%Y")
    # Substituir "/" por "-" na variável hoje
    hoje = hoje.replace("/", "-")

    # Chama a funcão para capitular os nomes de pessoas de forma correta.
    # Esse nome será utilizado para criar a beneficiário mantendo o padrão de
    # da empresa que não utiliza caixa alta nos nomes das pastas

    name = HumanName(first_name)
    name.capitalize(force=True)

    origem_excel = (
        f"{prefixo_pastas_excel}/{hoje}/{operadora}/{name}/{demanda}/{name}.xlsx"
    )
    destino_excel = f"{prefixo_fonte}/fonte.xlsx"
    print("=========================================", f"Origem: {origem_excel}")
    print("=========================================", f"Destino: {destino_excel}")

    try:
        shutil.copyfile(origem_excel, destino_excel)
        os.startfile(
            f"{prefixo_pastas_word}/{hoje}/{operadora}/{name}/{demanda}/{name}.docx"
        )
        print("Arquivo copiado com sucesso")

        # Imprimir f"{prefixo_pastas_word}/{hoje}/{operadora}/{name}/{demanda}/{name}.docx")

    except Exception as e:
        print(
            "=========================================",
            f"Erro ao copiar o arquivo: {e}",
        )

    return url_for("webui.responder")


def carta(responder):
    try:
        file_name = "planilha/responder.xlsx"  # File name
        sheet_name = 0  # 4th sheet
        header = 0  # The header is the 1nd row
        respNow = pd.read_excel(file_name, sheet_name, header)
        # Salvar respNow como um dataframe
        respNow = pd.DataFrame(respNow)
        # Transpor o dataframe
        # respNow = respNow.T
        respNow = pd.DataFrame(data=respNow)
    except Exception as e:
        print(e)

    return respNow
