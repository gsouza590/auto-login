import time

from PySimpleGUI import PySimpleGUI as sg
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import WebDriverWait


def tela_login(navegador):
    navegador.get("https://projetos.dpf.gov.br/siseg/siseg.php")
    # Layout
    sg.theme('Reddit')
    layout = [
        [sg.Text('Usuario'), sg.Input(key='usuario', size=(40, 10))],
        [sg.Text('Senha  '), sg.Input(key='senha', password_char='*', size=(40, 10))],
        [sg.Button('Entrar')]
    ]

    # Janela

    janela = sg.Window('Tela de Login', layout, size=(400, 100))

    # Ler os eventos
    while True:
        eventos, valores = janela.read()  # chama-se unpacking dentro do python
        if eventos == sg.WIN_CLOSED:
            break
        if eventos == 'Entrar':
            email = valores['usuario']  # Obtém o valor do campo de usuário
            senha = valores['senha']  # Obtém o valor do campo de senha
            janela.close()
            preencher_formulario(navegador,email, senha)
            break


def preencher_formulario(navegador,email,senha):

    while True:

        navegador.find_element('xpath', '//*[@id="emailcti"]').send_keys(email)
        navegador.find_element('xpath', '//*[@id="senhacti"]').send_keys(senha)
        navegador.find_element('xpath', '//*[@id="acessarcti"]').click()
        time.sleep(2)
        try:
            # Aguardar até que o elemento seja visível
            elemento = WebDriverWait(navegador, 3).until(
                EC.visibility_of_element_located((By.XPATH, '//*[@id="statususerdados"]'))
            )
            auth = elemento.text.upper()

            if "SENHA" in auth:
                print('Senha Incorreta, tente novamente!')
                navegador.find_element('xpath', '//*[@id="emailcti"]').clear()
                navegador.find_element('xpath', '//*[@id="senhacti"]').clear()
                tela_login()
            else:
                break
        except Exception:
            break