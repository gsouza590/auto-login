from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from webdriver_manager.chrome import ChromeDriverManager
from utils import modulo_login
from utils import modulo_transacao_pagina
from utils import modulo_tela_horario



# Inicio do programa

#Programa Principal

servico = Service(ChromeDriverManager().install())
navegador = webdriver.Chrome(service=servico)

modulo_login.tela_login(navegador)
modulo_transacao_pagina.transicao_paginas(navegador)
modulo_tela_horario.tela_horario(navegador)
input()
