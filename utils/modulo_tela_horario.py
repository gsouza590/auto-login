import time

from PySimpleGUI import PySimpleGUI as sg
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import WebDriverWait
from utils import modulo_tela_dia_personalizado


def tela_horario(navegador):
    # Layout
    sg.theme('Reddit')
    layout = [
        [sg.Text('       Hora de Entrada 1       '), sg.Text('       Hora de Entrada 2       ')],
        [sg.Input(key='horaEntradaHora', size=(10, 2)), sg.Text(':'), sg.Input(key='horaEntradaMinuto', size=(10, 2)),
         sg.Input(key='horaEntradaHora2', size=(10, 2)), sg.Text(':'), sg.Input(key='horaEntradaMinuto2', size=(10, 2))],
        [sg.Text('       Hora de Saída 1         '), sg.Text('       Hora de Saída 2         ')],
        [sg.Input(key='horaSaidaHora', size=(10, 2)), sg.Text(':'), sg.Input(key='horaSaidaMinuto', size=(10, 2)),
         sg.Input(key='horaSaidaHora2', size=(10, 2)), sg.Text(':'), sg.Input(key='horaSaidaMinuto2', size=(10, 2))],
        [sg.Checkbox('Intervalos Aleatórios', key='random')],
        [sg.Button('Horários Personalizados')],
        [sg.Button('Confirmar')]
    ]
    # Janela
    janela = sg.Window('Tela de Horário', layout, size=(400, 400))

    # Ler os eventos
    while True:
        eventos, valores = janela.read()  # chama-se unpacking dentro do python
        if eventos == sg.WIN_CLOSED:
            break
        if eventos == 'Confirmar':
            horaEntrada = valores['horaEntradaHora'] + valores['horaEntradaMinuto']  # Obtém o valor do campo de usuário
            horaSaida = valores['horaSaidaHora'] + valores['horaSaidaMinuto']  # Obtém o valor do campo de senha
            janela.close()
            preenchimento_horario(navegador,horaEntrada, horaSaida)
        if eventos=='Horários Personalizados':
            modulo_tela_dia_personalizado.dia_personalizacao()
            break


def preenchimento_horario(navegador,horaEntrada, horaSaida):

    elementos = navegador.find_elements('xpath', "//*[@id='formConteudo:j_id274:opRelatorio:tb']/tr")
    for elemento in elementos:
        time.sleep(3)
        pegaTexto = navegador.find_element('xpath', '//*[@id="formInclusao:opRelatorioModal:0:j_id495"]')
        texto = pegaTexto.text

        if "Sáb" in texto or "Dom" in texto:
            time.sleep(3)
            navegador.find_element('xpath', '//*[@id="formInclusao:opRelatorioModal:0:j_id501"]').click()

        else:
            # Esperar até que o botão "Registro Manual de Frequência" esteja visível na página
            registro_manual = WebDriverWait(navegador, 10).until(
                EC.visibility_of_element_located((By.ID, "formInclusao:j_id568:1")))
            # Verificar se o botão está visível na página
            if registro_manual.is_displayed():
                time.sleep(3)
                registro_manual.click()
            else:
                print("Botão 'Registro Manual de Frequência' não está visível na página")

            time.sleep(3)
            registro_horario = WebDriverWait(navegador, 10).until(
                EC.visibility_of_element_located((By.NAME, 'formInclusao:registrosInclusao:0:j_id601')))

            campo_inicio = navegador.find_element('xpath', '//*[@id="formInclusao:registrosInclusao:0:j_id600"]/input')
            campo_inicio.send_keys(Keys.BACKSPACE * 4)
            campo_inicio.send_keys(horaEntrada)
            campo_inicio.send_keys(Keys.TAB)
            campo_fim = navegador.find_element('xpath', '//*[@id="formInclusao:registrosInclusao:0:j_id602"]/input')
            campo_fim.send_keys(horaSaida)

            time.sleep(3)
            navegador.find_element('xpath', '//*[@id="formInclusao:salvar"]').click()

            time.sleep(3)
            navegador.find_element('xpath', '//*[@id="formInclusao:opRelatorioModal:0:j_id501"]').click()

