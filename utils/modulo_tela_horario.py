from PySimpleGUI import PySimpleGUI as sg
from utils import modulo_tela_dia_personalizado
from utils.modulo_preenchimento import preenchimento_horario_ocorrencia, preenchimento_horario_manual

def tela_horario(navegador):
    # Layout
    sg.theme('Reddit')
    layout = [
        [sg.Text('\tHora  Entrada Atv'), sg.Text('\tHora Saida Atv')],
        [sg.Input(key='horaAtvHora', size=(10, 2), disabled=True), sg.Text(':'),
         sg.Input(key='horaAtvMinuto', size=(10, 2), disabled=True),
         sg.Input(key='horaAtvHora2', size=(10, 2), disabled=True), sg.Text(':'),
         sg.Input(key='horaAtvMinuto2', size=(10, 2), disabled=True)],
        [sg.Text('\tHora de Entrada 1'), sg.Text('\tHora de Saída 1')],
        [sg.Input(key='horaEntradaHora', size=(10, 2)), sg.Text(':'), sg.Input(key='horaEntradaMinuto', size=(10, 2)),
         sg.Input(key='horaSaidaHora', size=(10, 2)), sg.Text(':'), sg.Input(key='horaSaidaMinuto', size=(10, 2))],
        [sg.Text('\tHora de Entrada 2'), sg.Text('\tHora de Saída 2')],
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
                janela[campo].update(disabled=not valores['desporte'])

        if eventos == 'aleat':
            aleatorio = True

        if eventos == 'Horários Personalizados':
            modulo_tela_dia_personalizado.dia_personalizacao(navegador)


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