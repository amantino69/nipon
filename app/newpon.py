from selenium import webdriver

# Definir as informações de login
usuario = '069.836.456-26'
senha = 'Ans@2022'

# Iniciar o driver do Selenium
driver = webdriver.Chrome()

# Abrir o site de login
driver.get('https://www2.ans.gov.br/ans-idp/')

# Preencher o campo de usuário
user_field = driver.find_element_by_name('username')
user_field.send_keys(usuario)

# Preencher o campo de senha
password_field = driver.find_element_by_name('password')
password_field.send_keys(senha)

# Clicar no botão de login
login_button = driver.find_element_by_xpath("//button[contains(text(), 'Acessar')]")
login_button.click()

# Fechar o driver do Selenium
driver.quit()
