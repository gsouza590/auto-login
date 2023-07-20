import datetime
import random
import time
from selenium.common import StaleElementReferenceException, ElementNotInteractableException, NoSuchElementException
from selenium.webdriver import ActionChains
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import WebDriverWait


def espera_elemento_visivel(navegador, by, value, timeout=10):
    return WebDriverWait(navegador, timeout).until(
        EC.visibility_of_element_located((by, value))
    )


def espera_elemento_clicavel(navegador, by, value, timeout=10):
    return WebDriverWait(navegador, timeout).until(
        EC.element_to_be_clickable((by, value))
    )


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


def registra_tabela_manual(navegador, horaEntrada, horaSaida):
    registro_manual = espera_elemento_visivel(navegador, By.ID, "formInclusao:j_id574:1")

    if registro_manual.is_displayed():
        time.sleep(10)
        try:
            registro_manual.click()
        except (StaleElementReferenceException, ElementNotInteractableException):
            registro_manual = espera_elemento_visivel(navegador, By.ID, "formInclusao:j_id574:1")
            registro_manual.click()
    else:
        print("Botão 'Registro Manual de Frequência' não está visível na página")

    time.sleep(3)
    campo_inicio = navegador.find_element(By.XPATH, '//*[@id="formInclusao:registrosInclusao:0:j_id606"]/input')
    ActionChains(navegador).send_keys_to_element(campo_inicio, Keys.BACKSPACE * 4).perform()
    campo_inicio.send_keys(horaEntrada)
    campo_inicio.send_keys(Keys.TAB)
    campo_fim = navegador.find_element(By.XPATH, '//*[@id="formInclusao:registrosInclusao:0:j_id608"]/input')
    campo_fim.send_keys(horaSaida)
    time.sleep(3)
    navegador.find_element(By.ID, "formInclusao:salvar").click()
    time.sleep(3)


def registra_tabela_ocorrencia(navegador, horaAtividadeIni, horaAtividadeFim):
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


def preenchimento_horario_manual_personalizado(navegador, valores):
    elementos = navegador.find_elements('xpath', "//*[@id='formInclusao:opRelatorioModal:tb']/tr")

    for i in range(1, 32):
        time.sleep(3)
        pegaTexto = navegador.find_element('xpath', '//*[@id="formInclusao:opRelatorioModal:0:j_id501"]')
        texto = pegaTexto.text
        try:
            navegador.find_element('xpath', '//*[@id="formInclusao:registrosSelecionados:noDataRow"]/td')
            pegaDados = True
        except NoSuchElementException:
            pegaDados = False

        if "Sáb" in texto or "Dom" in texto or not pegaDados:
            time.sleep(3)
            navegador.find_element(By.ID, "formInclusao:opRelatorioModal:0:j_id507").click()
            continue

        checkbox_id = f'desporte_{i}'
        if valores[checkbox_id]:
            horaEntrada = valores[f'entrada1_hora_{i}'] + valores[f'entrada1_minuto_{i}']
            horaSaida = valores[f'saida1_hora_{i}'] + valores[f'saida1_minuto_{i}']
            horaEntrada2 = valores[f'entrada2_hora_{i}'] + valores[f'entrada2_minuto_{i}']
            horaSaida2 = valores[f'saida2_hora_{i}'] + valores[f'saida2_minuto_{i}']
            horaEntradaOcorrencia = valores[f'entradaOcorrencia_hora_{i}'] + valores[f'entradaOcorrencia_minuto_{i}']
            horaSaidaOcorrencia = valores[f'saidaOcorrencia_hora_{i}'] + valores[f'saidaOcorrencia_minuto_{i}']
            registra_tabela_manual(navegador, horaEntrada, horaSaida)
            registra_tabela_manual(navegador, horaEntrada2, horaSaida2)
            registra_tabela_ocorrencia(navegador, horaEntradaOcorrencia, horaSaidaOcorrencia)
        else:
            horaEntrada = valores[f'entrada1_hora_{i}'] + valores[f'entrada1_minuto_{i}']
            horaSaida = valores[f'saida1_hora_{i}'] + valores[f'saida1_minuto_{i}']
            horaEntrada2 = valores[f'entrada2_hora_{i}'] + valores[f'entrada2_minuto_{i}']
            horaSaida2 = valores[f'saida2_hora_{i}'] + valores[f'saida2_minuto_{i}']
            registra_tabela_manual(navegador, horaEntrada, horaSaida)
            registra_tabela_manual(navegador, horaEntrada2, horaSaida2)

        time.sleep(3)
        navegador.find_element(By.ID, "formInclusao:opRelatorioModal:0:j_id507").click()

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
#
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
