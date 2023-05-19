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
        [sg.Text('       Hora  Entrada Atv      '), sg.Text('       Hora Saida Atv     ')],
        [sg.Input(key='horaAtvHora', size=(10, 2), disabled=True), sg.Text(':'),
         sg.Input(key='horaAtvMinuto', size=(10, 2), disabled=True),
         sg.Input(key='horaAtvHora2', size=(10, 2), disabled=True), sg.Text(':'),
         sg.Input(key='horaAtvMinuto2', size=(10, 2), disabled=True)],
        [sg.Text('Hora de Entrada 1'), sg.Text('Hora de Saída 1')],
        [sg.Input(key='horaEntradaHora', size=(10, 2)), sg.Text(':'), sg.Input(key='horaEntradaMinuto', size=(10, 2)),
         sg.Input(key='horaSaidaHora', size=(10, 2)), sg.Text(':'), sg.Input(key='horaSaidaMinuto', size=(10, 2))],
        [sg.Text('Hora de Entrada 2'), sg.Text('Hora de Saída 2')],
        [sg.Input(key='horaEntradaHora2', size=(10, 2)), sg.Text(':'), sg.Input(key='horaEntradaMinuto2', size=(10, 2)),
         sg.Input(key='horaSaidaHora2', size=(10, 2)), sg.Text(':'), sg.Input(key='horaSaidaMinuto2', size=(10, 2))],
        [sg.Checkbox('Intervalos Aleatórios', key='random'),
         sg.Checkbox('Ocorrência Desportiva', key='desporte', enable_events=True, default=False)],
        [sg.Button('Horários Personalizados')],
        [sg.Button('Confirmar')]
    ]

    # Janela
    janela = sg.Window('Tela de Horário', layout, size=(400, 400))
    horaEntrada = ''
    horaSaida = ''
    horaEntrada2 = ''
    horaSaida2 = ''
    # Ler os eventos

    while True:
        eventos, valores = janela.read()
        if eventos == sg.WIN_CLOSED:
            break
        if eventos == 'desporte':
            janela['horaAtvHora'].update(disabled=False)
            janela['horaAtvMinuto'].update(disabled=False)
            janela['horaAtvHora2'].update(disabled=False)
            janela['horaAtvMinuto2'].update(disabled=False)

        if eventos == 'Confirmar':
            horaEntrada = valores['horaEntradaHora'] + valores['horaEntradaMinuto']
            horaSaida = valores['horaSaidaHora'] + valores['horaSaidaMinuto']
            horaEntrada2 = valores['horaEntradaHora2'] + valores['horaEntradaMinuto2']
            horaSaida2 = valores['horaSaidaHora2'] + valores['horaSaidaMinuto2']
            janela.close()

            if valores['desporte']:
                horaAtividadeIni = valores['horaAtvHora'] + valores['horaAtvMinuto']
                horaAtividadeFim = valores['horaAtvHora2'] + valores['horaAtvMinuto2']
                preenchimento_horario_ocorrencia(navegador, horaEntrada, horaSaida, horaEntrada2, horaSaida2,
                                                 horaAtividadeIni, horaAtividadeFim)
            else:
                preenchimento_horario_manual(navegador, horaEntrada, horaSaida, horaEntrada2, horaSaida2)

            if eventos == 'Horários Personalizados':
                modulo_tela_dia_personalizado.dia_personalizacao()
                break


def preenchimento_horario_manual(navegador, horaEntrada, horaSaida, horaEntrada2, horaSaida2):
    elementos = navegador.find_elements('xpath', "//*[@id='formInclusao:opRelatorioModal:tb']/tr")
    while len(elementos) > 0:
        time.sleep(3)
        pegaTexto = navegador.find_element('xpath', '//*[@id="formInclusao:opRelatorioModal:0:j_id501"]')
        texto = pegaTexto.text

        if "Sáb" in texto or "Dom" in texto:
            time.sleep(3)
            navegador.find_element('xpath', '//*[@id="formInclusao:opRelatorioModal:0:j_id507"]').click()
        else:
            registra_tabela_manual(navegador, horaEntrada, horaSaida)
            registra_tabela_manual(navegador, horaEntrada2, horaSaida2)
            navegador.find_element('xpath', '//*[@id="formInclusao:opRelatorioModal:0:j_id507"]').click()

        elementos = navegador.find_elements('xpath', "//*[@id='formInclusao:opRelatorioModal:tb']/tr")


def preenchimento_horario_ocorrencia(navegador, horaEntrada, horaSaida, horaEntrada2, horaSaida2, horaAtividadeIni,
                                     horaAtividadeFim):
    elementos = navegador.find_elements('xpath', "//*[@id='formInclusao:opRelatorioModal:tb']/tr")
    while len(elementos) > 0:
        time.sleep(3)
        pegaTexto = navegador.find_element('xpath', '//*[@id="formInclusao:opRelatorioModal:0:j_id501"]')
        texto = pegaTexto.text

        if "Sáb" in texto or "Dom" in texto:
            time.sleep(3)
            navegador.find_element('xpath', '//*[@id="formInclusao:opRelatorioModal:0:j_id507"]').click()
        else:
            registra_tabela_ocorrencia(navegador, horaAtividadeIni, horaAtividadeFim)
            registra_tabela_manual(navegador, horaEntrada, horaSaida)
            registra_tabela_manual(navegador, horaEntrada2, horaSaida2)
            navegador.find_element('xpath', '//*[@id="formInclusao:opRelatorioModal:0:j_id501"]').click()

        elementos = navegador.find_elements('xpath', "//*[@id='formInclusao:opRelatorioModal:tb']/tr")


def registra_tabela_manual(navegador, horaEntrada, horaSaida):
    # Esperar até que o botão "Registro Manual de Frequência" esteja visível na página
    registro_manual = WebDriverWait(navegador, 10).until(
        EC.visibility_of_element_located((By.ID, "formInclusao:j_id574:1")))
    # Verificar se o botão está visível na página
    if registro_manual.is_displayed():
        time.sleep(3)
        registro_manual.click()
    else:
        print("Botão 'Registro Manual de Frequência' não está visível na página")

    time.sleep(3)
    WebDriverWait(navegador, 10).until(
        EC.visibility_of_element_located((By.ID, 'formInclusao:registrosInclusao:0:j_id606')))

    campo_inicio = navegador.find_element('xpath', '//*[@id="formInclusao:registrosInclusao:0:j_id606"]/input')
    campo_inicio.send_keys(Keys.BACKSPACE * 4)
    campo_inicio.send_keys(horaEntrada)
    campo_inicio.send_keys(Keys.TAB)
    campo_fim = navegador.find_element('xpath', '//*[@id="formInclusao:registrosInclusao:0:j_id608"]/input')
    campo_fim.send_keys(horaSaida)
    time.sleep(3)
    navegador.find_element('xpath', '//*[@id="formInclusao:salvar"]').click()
    time.sleep(3)


def registra_tabela_ocorrencia(navegador, horaAtividadeIni, horaAtividadeFim):
    # Selecionar a Ocorrencia Desportiva

    select_element = navegador.find_element(By.XPATH,
                                            "//select[@id='formInclusao:j_id582:selectOcorrencia']/option[text()='Prática desportiva']")
    select_element.click()
    time.sleep(3)
    WebDriverWait(navegador, 10).until(
        EC.visibility_of_element_located((By.ID, 'formInclusao:registrosInclusao:0:j_id606')))

    campo_inicio = navegador.find_element('xpath', '//*[@id="formInclusao:registrosInclusao:0:j_id606"]/input')
    campo_inicio.send_keys(Keys.BACKSPACE * 4)
    campo_inicio.send_keys(horaAtividadeIni)
    campo_inicio.send_keys(Keys.TAB)
    campo_fim = navegador.find_element('xpath', '//*[@id="formInclusao:registrosInclusao:0:j_id608"]/input')
    campo_fim.send_keys(horaAtividadeFim)
    time.sleep(3)
    navegador.find_element('xpath', '//*[@id="formInclusao:salvar"]').click()
    time.sleep(3)
