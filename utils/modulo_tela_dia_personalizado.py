import time
from selenium.common import StaleElementReferenceException, ElementNotInteractableException, NoSuchElementException
from selenium.webdriver import ActionChains
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import WebDriverWait
import PySimpleGUI as sg

def dia_personalizacao(navegador):
    # Defina o layout da janela de registros
    registro_layout = [
        [sg.Text('Dia \t\tEntrada 1\tSaida 1     \tEntrada 2  \tSaida 2    \tOcorrência Desportiva')]
    ]

    for i in range(1, 32):
        registro_layout.append([
            sg.Text(f'{i}\t'),
            sg.Input(size=(6, 2), key=f'entrada1_hora_{i}', pad=(0, 0)), sg.Text(':', pad=(0, 0)),
            sg.Input(size=(6, 2), key=f'entrada1_minuto_{i}', pad=((0, 20), (0, 0))),

            sg.Input(size=(6, 2), key=f'saida1_hora_{i}', pad=(0, 0)), sg.Text(':', pad=(0, 0)),
            sg.Input(size=(6, 2), key=f'saida1_minuto_{i}', pad=((0, 20), (0, 0))),

            sg.Input(size=(6, 2), key=f'entrada2_hora_{i}', pad=(0, 0)), sg.Text(':', pad=(0, 0)),
            sg.Input(size=(6, 2), key=f'entrada2_minuto_{i}', pad=((0, 20), (0, 0))),

            sg.Input(size=(6, 2), key=f'saida2_hora_{i}', pad=(0, 0)), sg.Text(':', pad=(0, 0)),
            sg.Input(size=(6, 2), key=f'saida2_minuto_{i}', pad=((0, 20), (0, 0))),

            sg.Checkbox(text="", key=f'ocorrencia_desportiva_{i}', pad=((0, 4), (0, 0))),
            sg.Input(size=(6, 2), key=f'entradaOcorrencia_hora_{i}', pad=(0, 0)), sg.Text(':', pad=(0, 0)),
            sg.Input(size=(6, 2), key=f'entradaOcorrencia_minuto_{i}', pad=(0, 0))
        ])
    registro_layout.append([sg.Button('Confirmar')])

    # Crie a janela de registros
    registro_window = sg.Window('Registros de Horários', registro_layout, finalize=True)

    # Loop de eventos da janela de registros
    while True:
        event, valores = registro_window.read()
        if event == sg.WINDOW_CLOSED:
            break
        if event == 'Confirmar':
            preenchimento_horario_manual(navegador, valores)

    # Feche a janela de registros
    registro_window.close()

def preenchimento_horario_manual(navegador, valores):
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
        else:
                horaEntrada = valores[f'entrada1_hora_{i}'] + valores[f'entrada1_minuto_{i}']
                horaSaida = valores[f'saida1_hora_{i}'] + valores[f'saida1_minuto_{i}']
                horaEntrada2 = valores[f'entrada2_hora_{i}'] + valores[f'entrada2_minuto_{i}']
                horaSaida2 = valores[f'saida2_hora_{i}'] + valores[f'saida2_minuto_{i}']
                registra_tabela_manual(navegador, horaEntrada, horaSaida)
                registra_tabela_manual(navegador, horaEntrada2, horaSaida2)

        time.sleep(3)
        navegador.find_element(By.ID, "formInclusao:opRelatorioModal:0:j_id507").click()

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
    campo_fim = navegador.find_element(By.XPATH, '//*[@id="formInclusao:registrosInclusao:0:j_id608"]/input')
    campo_fim.send_keys(horaSaida)
    time.sleep(3)
    navegador.find_element(By.ID, "formInclusao:salvar").click()
    time.sleep(3)

