# Acesso o site https://www2.ans.gov.br/ans-idp/ e utilize a biblioteca Selenium Python para localizar e inserir as seguintes informações usuário = 069.836.456-26 e a senha =Ans@2022

from selenium import webdriver
from selenium.webdriver.common.keys import Keys
driver = webdriver.Chrome()
driver.get("https://www2.ans.gov.br/ans-idp/")
user = driver.find_element_by_id("username")
user.send_keys("06983645626")
password = driver.find_element_by_id("password")
password.send_keys("Ans@2022")
driver.find_element_by_name("submit").click()