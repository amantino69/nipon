from __future__ import print_function
from selenium import webdriver
from flask import url_for
from selenium.webdriver import ActionChains
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import re
import time
import os
import shutil
import genderbr
import pandas as pd

resposta = "PREMIUM"


chrome_options = webdriver.ChromeOptions()


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

time.sleep(30)
