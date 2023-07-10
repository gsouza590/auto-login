import datetime
import random
import time
from PySimpleGUI import PySimpleGUI as sg
from selenium.common import StaleElementReferenceException, ElementNotInteractableException, NoSuchElementException
from selenium.webdriver import ActionChains
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
        [sg.Checkbox('Intervalos Aleatórios', key='aleat', enable_events=True, default=False),
         sg.Checkbox('Ocorrência Desportiva', key='desporte', enable_events=True, default=False)],
        [sg.Button('Horários Personalizados')],
        [sg.Button('Confirmar')]
    ]

    # Janela
    janela = sg.Window('Tela de Horário', layout, size=(400, 400))

    aleatorio = False

    # Ler os eventos
    while True:
        eventos, valores = janela.read()
        if eventos == sg.WIN_CLOSED:
            break
        if eventos == 'desporte':
            campos_desabilitados = ['horaAtvHora', 'horaAtvMinuto', 'horaAtvHora2', 'horaAtvMinuto2']
            for campo in campos_desabilitados:
                janela[campo].update(disabled= not valores['desporte'])

        if eventos == 'aleat':
            aleatorio = True

        if eventos == 'Horários Personalizados':
            modulo_tela_dia_personalizado.dia_personalizacao()
            break

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
                                                 horaAtividadeIni, horaAtividadeFim, aleatorio)
            else:
                preenchimento_horario_manual(navegador, horaEntrada, horaSaida, horaEntrada2, horaSaida2, aleatorio)


def preenchimento_horario_manual(navegador, horaEntrada, horaSaida, horaEntrada2, horaSaida2, aleatorio):
    elementos = navegador.find_elements('xpath', "//*[@id='formInclusao:opRelatorioModal:tb']/tr")
    while len(elementos) > 0:
        time.sleep(3)
        pegaTexto = navegador.find_element('xpath', '//*[@id="formInclusao:opRelatorioModal:0:j_id501"]')
        texto = pegaTexto.text
        try:
            navegador.find_element('xpath', '//*[@id="formInclusao:registrosSelecionados:noDataRow"]/td')
            pegaDados = True
        except NoSuchElementException:
            pegaDados = False

        if "Sáb" in texto or "Dom" in texto or pegaDados==False:
            time.sleep(3)
            navegador.find_element(By.ID, "formInclusao:opRelatorioModal:0:j_id507").click()
        elif aleatorio:
            horaEntradaAleatoria, horaSaidaAleatoria, horaEntradaAleatoria2, horaSaidaAleatoria2 = gerar_horarios_aleatorios(
                horaEntrada, horaSaida, horaEntrada2, horaSaida2)
            registra_tabela_manual(navegador, horaEntradaAleatoria, horaSaidaAleatoria)
            registra_tabela_manual(navegador, horaEntradaAleatoria2, horaSaidaAleatoria2)
        else:
            registra_tabela_manual(navegador, horaEntrada, horaSaida)
            registra_tabela_manual(navegador, horaEntrada2, horaSaida2)

        time.sleep(3)
        navegador.find_element(By.ID, "formInclusao:opRelatorioModal:0:j_id507").click()


# Preenchimento do horario quando ocorre ocorrência desportiva
def preenchimento_horario_ocorrencia(navegador, horaEntrada, horaSaida, horaEntrada2, horaSaida2, horaAtividadeIni,
                                     horaAtividadeFim, aleatorio):
    elementos = navegador.find_elements('xpath', "//*[@id='formInclusao:opRelatorioModal:tb']/tr")
    while len(elementos) > 0:
        time.sleep(3)
        pegaTexto = navegador.find_element('xpath', '//*[@id="formInclusao:opRelatorioModal:0:j_id501"]')
        texto = pegaTexto.text

        try:
            navegador.find_element('xpath', '//*[@id="formInclusao:registrosSelecionados:noDataRow"]/td')
            pegaDados = True
        except NoSuchElementException:
            pegaDados = False

        if "Sáb" in texto or "Dom" in texto or pegaDados == False:
            time.sleep(3)
            navegador.find_element(By.ID, "formInclusao:opRelatorioModal:0:j_id507").click()
        elif aleatorio:
            horaAtividadeIni, horaAtividadeFim = gerar_horarios_aleatorios_ocorrencia(horaAtividadeIni,
                                                                                      horaAtividadeFim)

            horaEntradaAleatoria, horaSaidaAleatoria, horaEntradaAleatoria2, horaSaidaAleatoria2 = gerar_horarios_aleatorios(
                horaEntrada, horaSaida, horaEntrada2, horaSaida2)

            registra_tabela_ocorrencia(navegador, horaAtividadeIni, horaAtividadeFim)
            registra_tabela_manual(navegador, horaEntradaAleatoria, horaSaidaAleatoria)
            registra_tabela_manual(navegador, horaEntradaAleatoria2, horaSaidaAleatoria2)
            navegador.find_element(By.ID, "formInclusao:opRelatorioModal:0:j_id501").click()
        else:
            registra_tabela_ocorrencia(navegador, horaAtividadeIni, horaAtividadeFim)
            registra_tabela_manual(navegador, horaEntrada, horaSaida)
            registra_tabela_manual(navegador, horaEntrada2, horaSaida2)
            navegador.find_element(By.ID, "formInclusao:opRelatorioModal:0:j_id501").click()

        time.sleep(3)
        navegador.find_element(By.ID, "formInclusao:opRelatorioModal:0:j_id507").click()


# Preenchimento do horario normal de trabalho
def registra_tabela_manual(navegador, horaEntrada, horaSaida):
    # Esperar até que o botão "Registro Manual de Frequência" esteja visível na página
    registro_manual = WebDriverWait(navegador, 10).until(
        EC.visibility_of_element_located((By.ID, "formInclusao:j_id574:1")))
    # Verificar se o botão está visível na página
    if registro_manual.is_displayed():
        time.sleep(10)
        # Tentar clicar no elemento usando um bloco try-except
        try:
            registro_manual.click()
        except (StaleElementReferenceException, ElementNotInteractableException):
            # Se ocorrer uma exceção, aguardar novamente até que o elemento seja encontrado
            registro_manual = WebDriverWait(navegador, 10).until(
                EC.visibility_of_element_located((By.ID, "formInclusao:j_id574:1")))
            registro_manual.click()
    else:
        print("Botão 'Registro Manual de Frequência' não está visível na página")

    time.sleep(3)
    WebDriverWait(navegador, 10).until(
        EC.visibility_of_element_located((By.ID, 'formInclusao:registrosInclusao:0:j_id606')))

    campo_inicio = navegador.find_element(By.XPATH, '//*[@id="formInclusao:registrosInclusao:0:j_id606"]/input')
    ActionChains(navegador).send_keys_to_element(campo_inicio, Keys.BACKSPACE * 4).perform()
    campo_inicio.send_keys(horaEntrada)
    campo_inicio.send_keys(Keys.TAB)
    campo_fim = navegador.find_element('xpath', '//*[@id="formInclusao:registrosInclusao:0:j_id608"]/input')
    campo_fim.send_keys(horaSaida)
    time.sleep(3)
    navegador.find_element(By.ID, "formInclusao:salvar").click()
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
    navegador.find_element(By.ID, "formInclusao:salvar").click()
    time.sleep(3)


# Realizar ajustes no horario para não recair em horário britanico.

def calcular_hora_aleatoria(hora_base, minrandom):
    try:
        hora_aleatoria = int(hora_base)
        if minrandom < 0:
            hora_aleatoria -= abs(minrandom)
        else:
            hora_aleatoria += abs(minrandom)

        horas = hora_aleatoria // 100
        minutos = hora_aleatoria % 100
        minutos_corrigidos = max(0, min(59, minutos))
        hora_datetime = datetime.datetime.now().replace(hour=horas, minute=minutos_corrigidos, second=0, microsecond=0)
        hora_datetime -= datetime.timedelta(minutes=abs(minrandom))
        hora_aleatoria = (hora_datetime.hour * 100) + hora_datetime.minute

        hora_aleatoria = str(hora_aleatoria).zfill(4)  # Adiciona zeros à esquerda, se necessário
        return hora_aleatoria
    except ValueError:
        pass


def gerar_horarios_aleatorios(hora1, hora2, hora3=None, hora4=None):
    valores = [-5, -4, -3, -2, -1, 1, 2, 3, 4, 5]
    minrandom1 = random.choice(valores)
    minrandom2 = random.choice(valores)
    horaAleatoria1 = str(calcular_hora_aleatoria(hora1, minrandom1)).zfill(4)
    horaAleatoria2 = str(calcular_hora_aleatoria(hora2, minrandom2)).zfill(4)
    horaAleatoria3 = str(calcular_hora_aleatoria(hora3, minrandom2)).zfill(4) if hora3 else ''
    horaAleatoria4 = str(calcular_hora_aleatoria(hora4, minrandom1)).zfill(4) if hora4 else ''
    return horaAleatoria1, horaAleatoria2, horaAleatoria3, horaAleatoria4


def gerar_horarios_aleatorios_ocorrencia(hora1, hora2):
    valores = [-5, -4, -3, -2, -1, 1, 2, 3, 4, 5]
    minrandom = random.choice(valores)
    horaAleatoria1 = str(calcular_hora_aleatoria(hora1, minrandom)).zfill(4)
    horaAleatoria2 = str(calcular_hora_aleatoria(hora2, minrandom)).zfill(4)
    return horaAleatoria1, horaAleatoria2