from selenium import webdriver
import time 
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver import ActionChains





chrome_options = webdriver.ChromeOptions()
driver = webdriver.Chrome(chrome_options=chrome_options)
driver.get('https://www2.ans.gov.br/ans-idp/')

driver.find_element_by_id('input-mask').send_keys('069.836.456-26')
driver.find_element_by_id('mod-login-password').send_keys('Ans@2022') # inserir a senha
driver.find_element_by_id('botao').click() # clicar no botão de login
driver.maximize_window()
time.sleep(5)
resposta = 'YOU ASSISTÊNCIA MÉDICA LTDA.'
caminho_operadora = "//*[contains(text(),'" + resposta + "' )]"
operadora = driver.find_element(By.XPATH, caminho_operadora).click() # Selecione na tabela a operadora escolhida
time.sleep(3)
driver.find_element(By.ID, 'form:btnContinuar').click() # clicar de confirmação


                    
time.sleep(5)
actions = ActionChains(driver)

e1 = driver.find_element_by_xpath('//*[@id="form:formMenu:j_idt39"]/ul/li[6]/a/span[1]')
e2 = e1.find_element_by_xpath('//*[@id="form:formMenu:j_idt39"]/ul/li[6]/ul/li/a/span')
actions.move_to_element(e1).move_to_element(e2).perform()
e2.click()


 