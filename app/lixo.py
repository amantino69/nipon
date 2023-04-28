import time
import pyautogui
from selenium import webdriver

chrome_options = webdriver.ChromeOptions()
chrome_options.add_argument("--ignore-certificate-errors")

driver = webdriver.Chrome(options=chrome_options)
driver.set_window_size(1024, 768)
driver.get("https://www2.ans.gov.br/ans-idp/")

# Aguardar a janela de seleção do certificado
time.sleep(5)

# Localizar e interagir com a janela de seleção do certificado
offset_y = 1  # Ajuste de acordo com a posição na lista
pos_x, pos_y = pyautogui.locateCenterOnScreen("planilha/Certificado.PNG")
pyautogui.click(pos_x, pos_y + offset_y)
pyautogui.press("enter")

# Adicione seu código de scraping aqui

# Fechar driver
driver.quit()
