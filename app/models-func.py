from __future__ import print_function
from selenium import webdriver
from flask import url_for
from selenium.webdriver import ActionChains
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from nameparser import HumanName
import re
import time
import os
import shutil
import genderbr
import pandas as pd

# Ju
# prefixo_pastas_word = 'C:/Users/Juliana Silva/Documents/NIPs'
# prefixo_pastas_excel = 'C:/Users/Juliana Silva/Documents/fontes'
# prefixo_fonte = 'C:/Users/Juliana Silva/documents/Minhas fontes de dados'


# Eu
prefixo_pastas_word = 'C:/Users/amantino/Documents/NIPs'
prefixo_pastas_excel = 'C:/Users/amantino/Documents/fontes'
prefixo_fonte = 'C:/Users/amantino/documents/Minhas fontes de dados'


responder = []

# Classe para criar o arquivo de resposta baseados no sistema ESPAÇO NIP da ANS
# O sitema coleta informações das diversas páginas e cria uma fonte de mesclagem
# para a criação do documento de resposta criado atraves de um modelo predefinido para
# no Word recurso do Office denaminado Mala MalaDireta


class MalaDireta():

    # O recurso Mala Direta do Office espera que a fonte de dados esteja sempre
    # na pasta \Documents\Minhas fontes de dados.
    # Esse módulo copia a fonte de dados específica de um determinado beneficiário
    # para a pasta \Documents\Minhas fontes de dados antes de realizar a mesclagem

    def texto(operadora, hoje, first_name, demanda, situacao):

        # Chama a funcão para capitular os nomes de pessoas de forma correta.
        # Esse nome será utilizado para criar a beneficiário mantendo o padrão de
        # da empresa que não utiliza caixa alta nos nomes das pastas

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

    # Essa função cria uma planilha Excel com os dados dos Dataframe apenas dos
    # do conjunto de dados que será processado de acordo com as escolhas do usuário

    def carta(responder):
        file_name = "planilha/responder.xlsx"  # File name
        sheet_name = 0  # 4th sheet
        header = 0  # The header is the 1nd row
        respNow = pd.read_excel(file_name, sheet_name, header)
        # Salvar respNow como um dataframe
        respNow = pd.DataFrame(respNow)
        # Transpor o dataframe
        # respNow = respNow.T
        respNow = pd.DataFrame(data=respNow)

        return (respNow)

    # O banco de dados da ANS é deficiente e registra todos os beneficiários como
    # sendo do sexo masculino. Essa função retorna o sexo considerando o primeiro
    # nome. O índice de acerto é superior a 99%. O sistema considera como Masculino
    # os nomes não identificados

    def find_gender(nome):
        first_name = nome.split(' ')[0]
        genero = genderbr.get_gender(first_name)
        return(genero)

    # Essa função faz um scraper no site Espaço NIP da ANS passando operadora por
    # operadora, página por página e coleta as informações. Informa os usuários e
    # senhas e navega nas páginas semelhante à ação do usuário.

    def job(resposta, dias):

        # webdriver é DRIVER que permite a biblioteca Selenium do Python acessar
        # e entender a navegação do Google Chrome. Se for outro navegador esse arquivo
        # preciso ser substituído pelo respectivo driver. O arquivo de ficar na mesma
        # pasta onde o progra será executado ou estar na path
        chrome_options = webdriver.ChromeOptions()
        # Inicia o navegador sem abrir a tela
        # chrome_options.add_argument("--headless")
        # Ignora erros de certificação digital
        chrome_options.add_argument('ignore-certificate-errors')

        navegador = webdriver.Chrome(chrome_options=chrome_options)
        navegador.get('https://www2.ans.gov.br/ans-idp/')

        # Espera até que o elemento com id 'input-mask' esteja disponível
        element = WebDriverWait(navegador, 15).until(
            EC.presence_of_element_located((By.ID, 'input-mask')))

        navegador.find_element(
            By.ID, 'input-mask').send_keys('069.836.456-26')  # inserir o cpf
        navegador.find_element(
            By.ID, 'mod-login-password').send_keys('Ans@2022')  # inserir a senha
        # clicar no botão de login
        navegador.find_element(By.ID, 'botao').click()
        navegador.maximize_window()

        caminho_operadora = "//*[contains(text(),'" + resposta + "' )]"
        element = WebDriverWait(navegador, 15).until(
            EC.presence_of_element_located((By.XPATH, caminho_operadora)))
        # Selecione na tabela a operadora escolhida

        operadora = navegador.find_element(By.XPATH, caminho_operadora).click()

        operadora = resposta
        time.sleep(3)
        # clicar de confirmação
        navegador.find_element(By.ID, 'form:btnContinuar').click()

        actions = ActionChains(navegador)

        # Se o nomo da operadora contém a palavra PREMIUM
        element = WebDriverWait(navegador, 15).until(
            EC.presence_of_element_located((By.XPATH, '//span[text()="Fiscalização"]')))
        e1 = navegador.find_element(By.XPATH, '//span[text()="Fiscalização"]')

        e2 = navegador.find_element(By.XPATH, '//span[text()="Espaço NIP"]')

        actions.move_to_element(e1).move_to_element(e2).perform()
        e2.click()

        # go to iframe
        navegador.switch_to.frame('frameConteudoDialog')

        table = navegador.find_element(By.ID, 'conteudoPrincipal')

        df = pd.read_html(table.get_attribute('outerHTML'))[1]

        elements = navegador.find_elements(By.CLASS_NAME, 'ui-paginator-pages')
        paginas = elements[-1].text

        if len(paginas) > 9:
            paginas = paginas[:-2]
        else:
            paginas = paginas[:-1]

        try:
            if int(paginas) >= 1:

                todasDF = df
                e = 2
                for e in paginas:
                    navegador.find_element(
                        By.XPATH, '//*[@id="formContent:j_idt85:tbDemandaAguardandoResposta_paginator_bottom"]/span[4]/span').click()  # clicar na próxima

                    time.sleep(5)
                    table1 = navegador.find_element(
                        By.ID, 'formContent:j_idt22')
                    time.sleep(5)
                    df1 = pd.read_html(table1.get_attribute('outerHTML'))[1]
                    todasDF = pd.concat([todasDF, df1], ignore_index=True)
                df = todasDF  # concatenar as duas tabelas
        except:
            print("Não há mais páginas")

        hoje = time.strftime('%d-%m-%Y')

        # Adicionar uma nova linha com o nome da operadora
        df.insert(0, 'Operadora', operadora)
        df.insert(0, 'Hoje', hoje)

        # Se não existir criar o diretório planilha
        if not os.path.exists('planilha'):
            os.makedirs('planilha')

        # Mantar somente linhas do df que com prazo == "1 dias úteis" e respondido = "NO"
        responder = df[(df['Prazo'] == dias + " dias úteis")
                       & (df['Respondido'] == 'NO')]

        responder.to_excel('planilha/responder.xlsx', index=False)
        df.to_excel('planilha/tarefas.xlsx', engine='xlsxwriter')

        # Fazer um loop para pegar todos os nomes
        dict_info = []

        if len(responder) > 0:
            for j in range(len(df)):
                linhas = len(df)
                first_name = df.loc[j, 'Beneficiário']
                prazo = df.loc[j, 'Prazo']
                demanda = int(df.loc[j, 'Demanda'])
                respondido = df.loc[j, 'Respondido']
                if prazo == (dias + ' dias úteis') and (respondido == 'NO'):
                    # se não existir criar pasta  com o valor de first_name
                    name = HumanName(first_name)
                    name.capitalize(force=True)

                    if not os.path.exists(f'{prefixo_pastas_word}/{hoje}/{operadora}/{name}/{demanda}/'):
                        os.makedirs(
                            f'{prefixo_pastas_word}/{hoje}/{operadora}/{name}/{demanda}/')

                    if not os.path.exists(f'{prefixo_pastas_excel}/{hoje}/{operadora}/{name}/{demanda}/'):
                        os.makedirs(
                            f'{prefixo_pastas_excel}/{hoje}/{operadora}/{name}/{demanda}/')

                    # Clicar no Botão Limpar filtro
                    navegador.find_element(By.XPATH,
                                           '//*[@id="formContent:j_idt81"]/span ').click()
                    time.sleep(3)
                    navegador.find_element(By.ID, 'formContent:idObjeto').send_keys(
                        demanda)  # inserir o Demanda
                    navegador.find_element(By.ID,
                                           'formContent:j_idt82').click()  # Clicar no Botão Buscar
                    time.sleep(5)
                    navegador.find_element(By.ID,
                                           'formContent:j_idt85:tbDemandaAguardandoResposta:0:j_idt114').click()  # Clicar no Botão Detalhes

                    time.sleep(3)

                    resumo = navegador.find_element(
                        By.ID, 'conteudo')  # Cliquei na DIV Detalhes

                    nip0 = pd.read_html(resumo.get_attribute('outerHTML'))[0]
                    nip1 = pd.read_html(resumo.get_attribute('outerHTML'))[1]
                    nip2 = pd.read_html(resumo.get_attribute('outerHTML'))[2]
                    nip3 = pd.read_html(resumo.get_attribute('outerHTML'))[3]
                    nip4 = pd.read_html(resumo.get_attribute('outerHTML'))[4]
                    nip5 = pd.read_html(resumo.get_attribute('outerHTML'))[5]

                    # Concatenar as tabelas encontradas nas páginas das NIPs
                    nip = pd.concat(
                        [nip0, nip1, nip2, nip3, nip4, nip5], ignore_index=True)

                    # # Somente a coluna 1
                    nip = nip.iloc[:, 0]

                    # exluir as 3 últimas linhas
                    nip = nip.drop(nip.index[-3:])

                    # # Localizar sinal de ? e substituir por sinal de :
                    nip = nip.str.replace('?', ':')

                    # # Utilizar : para quebrar a coluna em duas Colunas
                    nip = nip.str.split(':', n=1, expand=True)

                    # Clicar no botão VISUALIZAÇÃO para visalizar janela modal com mais
                    # informações
                    time.sleep(5)
                    navegador.find_element(By.ID,
                                           'formContent:j_idt191:0:j_idt202').click()  # Clicar no Botão Visualizar
                    time.sleep(5)

                    documento = navegador.find_element(
                        By.ID,                        'formContent:dlgDocumento')

                    notifica = pd.read_html(documento.get_attribute('outerHTML'))[
                        0]  # Cliquei na DIV Detalhes

                    # Apagar céludas repetidas
                    notifica = notifica.drop_duplicates(
                        subset=None, keep='first', inplace=False)

                    # Salva na variável protocolo o conteuno do SPAN //*[@id="formContent:obDocumento"]/table[2]/tbody/tr[1]/td/span
                    protocolo = navegador.find_element(By.XPATH,
                                                       '//*[@id="formContent:obDocumento"]/table[2]/tbody/tr[1]/td').text

                    # Extrair da variável Protocolo a parte numérica da variável protocolo e salvar na variácel numeroProtocolo

                    numeroProtocolo = re.findall(r'\d+', protocolo)

                    # Salvar na variável ano_protocolo a colula 0 da variável numeroProtocolo
                    ano_protocolo = numeroProtocolo[1]

                    # Salvar na variável digito_protocolo a colula 1 da variável numeroProtocolo
                    digito_protocolo = numeroProtocolo[0]

                    # Apagar as 6 primeiras linhas
                    notifica = notifica.drop(notifica.index[0:7])

                    # Manter apenas a coluna 0
                    notifica = notifica.iloc[:, 0]

                    # Apagar a ultima linha
                    notifica = notifica.drop(notifica.index[-1])

                    # Tratamento da variável protocoloNIP, pois alguns tem as string <<60>> atrapalhando
                    protocoloNIP = notifica.iloc[2]
                    situacao = notifica.iloc[9]

                    if len(str(protocoloNIP)) < 4:
                        protocoloNIP = notifica.iloc[3]

                    # Adicionar nova linha em nip e inserir na primeira coluna NIP e na segunda coluna o conteúdo da variável numnip
                    nip = nip.append(pd.DataFrame(
                        [['Protocolo NIP', protocoloNIP]]))

                    # Adicionar nola linha em nip e inserir na primeira coluna DEMAMDA e na segunda coluna o conteúdo da variável demanda
                    nip = nip.append(pd.DataFrame([['DEMANDA', demanda]]))

                    # # Adicionar nova linha em nip e inserir na primeira coluna PROTOCOLO e na segunda coluna o conteúdo da variável protocolo
                    nip = nip.append(pd.DataFrame([['NIP', protocolo]]))

                    # #  Adicionar nova linha em nip e inserir na primeira coluna NumPROTOCOLO e na segunda coluna o conteúdo da variável numeroProtocolo
                    nip = nip.append(pd.DataFrame(
                        [['NUMPROTOCOLO', numeroProtocolo]]))

                    #  # Adicionar nova linha em nip e inserir na primeira coluna ANO_PROTOCOLO e na segunda coluna o conteúdo da variável ano_protocolo
                    nip = nip.append(pd.DataFrame(
                        [['ANO_PROTOCOLO', ano_protocolo]]))

                    #  # Adicionar nova linha em nip e inserir na primeira coluna DIGITO_PROTOCLO e na segunda coluna o conteúdo da variável digito_protocolo
                    nip = nip.append(pd.DataFrame(
                        [['DIGITO_PROTOCOLO', digito_protocolo]]))

                    # Adicionar nova linha em nip e inserir na primeira coluna o cabeçalho Nome e na segunda coluna o conteúdo da variável first_name
                    nip = nip.append(pd.DataFrame([['Nome', first_name]]))

                    # primeiro = primeira parte de first_name

                    # Chamar a função Genero e criar campos que serão utilizados na mesclagem
                    # e personalizar o documento evitando textos comoSr(a). beneficiário(a)

                    genero = MalaDireta.find_gender(first_name)

                    if genero == 'F':
                        nip = nip.append(pd.DataFrame([['SEXO1', 'a']]))
                        nip = nip.append(pd.DataFrame([['SEXO2', 'a']]))
                    else:
                        nip = nip.append(pd.DataFrame([['SEXO1', 'o']]))
                        nip = nip.append(pd.DataFrame([['SEXO2', '']]))

                    dict_info.append({'Nome': first_name, 'Prazo': prazo,
                                     'Demanda': demanda, 'Gênero': genero, 'Situaçao': situacao})

                    # Primeira linha de nip deve ser Nome na primeira coluna e first_name na segunda coluna o conteúdo da variável
                    nip.iloc[0, 0] = 'Nome'
                    nip.iloc[0, 1] = first_name

                    # Traspor nip sem criar linha de indice
                    nip = nip.T

                    # Transformar primeira linha em cabeçalho
                    nip.columns = nip.iloc[0]

                    # Excluir segunda linha
                    nip = nip.drop(nip.index[0])

                    nip.to_excel(
                        f'{prefixo_pastas_excel}/{hoje }/{operadora}/{first_name}/{demanda}/{first_name}.xlsx')

                    time.sleep(3)

                    # Clicar no Botão Fechar visualização
                    navegador.find_element(By.ID,
                                           'formContent:j_idt218').click()

                    time.sleep(3)

                    # Rolar tela até o final de
                    navegador.execute_script(
                        "window.scrollTo(0, document.body.scrollHeight);")

                    navegador.find_element(By.ID,
                                           'formContent:pgDetalhes')  # Cliquei na DIV Detalhes

                    navegador.find_element(By.ID,
                                           'formContent:j_idt208').click()  # Clicar no Botão Voltar

                    #    Copia o arquivo GRIFOS.doc para a pasta Beneficiarios/first_name
                    name = HumanName(first_name)
                    name.capitalize(force=True)

                    # Cada operadora tem seu modelo prório com logomarca e outras partuicularides
                    # Nesse momento o sistema selciona o modelo segundo operadora e beneficiário e
                    # copia o arquivo para ser mesclado
                    shutil.copy(
                        f'grifos/{operadora}.docx', (f'{prefixo_pastas_word}/{hoje}/{operadora}/{name}/{demanda}/{name}.docx'))

            return dict_info
        return dict_info
