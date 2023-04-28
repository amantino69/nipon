from email.mime import application
import re
from webbrowser import get
from docx import Document
from xml.dom.minidom import Document
from selenium import webdriver # 
import time
import pandas as pd
import os
import shutil
import os
import genderbr
from flask import url_for, render_template, request, redirect, flash, session, abort, jsonify
from selenium.webdriver import ActionChains
from selenium.webdriver.common.by import By
        
        
        
        
        
        
        
        
        
        
        
        
        
        
        
        
        
        
        
        
        
        
        
        chrome_options = webdriver.ChromeOptions()
        # chrome_options.add_argument("--headless")
        chrome_options.add_argument('ignore-certificate-errors')
        
        

        navegador = webdriver.Chrome(chrome_options=chrome_options)
        navegador.get('https://www2.ans.gov.br/ans-idp/')


        navegador.find_element_by_id('input-mask').send_keys('069.836.456-26') # inserir o cpf
        navegador.find_element_by_id('mod-login-password').send_keys('Ans@2022') # inserir a senha
        navegador.find_element_by_id('botao').click() # clicar no botão de login
        navegador.maximize_window()

        caminho_operadora = "//*[contains(text(),'" + resposta + "' )]"
        operadora = navegador.find_element(By.XPATH, caminho_operadora).click() # Selecione na tabela a operadora escolhida
        time.sleep(3)
        navegador.find_element(By.ID, 'form:btnContinuar').click() # clicar de confirmação
        # for i in range(len(operadoras)): Trecho desabilitado por enquanto tratar somente Premium
        time.sleep(3)
        actions = ActionChains(navegador)

        
        #Se o nomo da operadora contém a palavra PREMIUM
        if 'PREMIUM' in resposta:
            e1 = navegador.find_element_by_xpath('//*[@id="form:formMenu:j_idt39"]/ul/li/a')
            e2 = e1.find_element_by_xpath('//*[@id="form:formMenu:j_idt39"]/ul/li/ul/li/a')
                      
        else:
            e1 = navegador.find_element_by_xpath('//*[@id="form:formMenu:j_idt39"]/ul/li[6]/a/span[1]')
            e2 = e1.find_element_by_xpath('//*[@id="form:formMenu:j_idt39"]/ul/li[6]/ul/li/a/span')
                                       
        actions.move_to_element(e1).move_to_element(e2).perform()
        e2.click()
        
      
        # go to iframe
        navegador.switch_to.frame('frameConteudoDialog')

        # back to previous frame
        # navegador.switch_to.parent_frame()
                

        table = navegador.find_element(By.ID,'conteudoPrincipal')
                                         
               
        df =  pd.read_html(table.get_attribute('outerHTML'))[1]
        
        elements = navegador.find_elements_by_class_name('ui-paginator-pages')
        paginas = elements[-1].text




<a href="#" class="ui-menuitem-link ui-submenu-link ui-corner-all" tabindex="-1"><span class="ui-menuitem-text">Fiscalização</span><span class="ui-icon ui-icon-triangle-1-s"></span></a>
<a href="#" class="ui-menuitem-link ui-submenu-link ui-corner-all" tabindex="-1"><span class="ui-menuitem-text">Fiscalização</span><span class="ui-icon ui-icon-triangle-1-s"></span></a>


//*[@id="form:formMenu:j_idt39"]/ul/li[6]/a
//*[@id="form:formMenu:j_idt39"]/ul/li/a



<span class="ui-menuitem-text">Fiscalização</span>
//*[@id="form:formMenu:j_idt39"]/ul/li/a/span[1]


//*[@id="form:formMenu:j_idt39"]/ul/li/a funciona para o primeiro menu PREMIUM
//*[@id="form:formMenu:j_idt39"]
//*[@id="form:formMenu:j_idt39"]/ul/li[6]/a
//*[@id="form:formMenu:j_idt39"]/ul/li[6]/a/span[1]




//*[@id="form:formMenu:j_idt39"]/ul/li/ul/li/a
//*[@id="form:formMenu:j_idt39"]/ul/li/ul/li/a