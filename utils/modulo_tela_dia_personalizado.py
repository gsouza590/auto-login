
import PySimpleGUI as sg
from utils.modulo_preenchimento import preenchimento_horario_manual, preenchimento_horario_manual_personalizado

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

            sg.Checkbox('Ocorrência Desportiva', key=f'desporte_{i}', enable_events=True, default=False, pad=((0, 4), (0, 0))),
            sg.Input(size=(6, 2), key=f'entradaOcorrencia_hora_{i}', pad=(0, 0)), sg.Text(':', pad=(0, 0)),
            sg.Input(size=(6, 2), key=f'entradaOcorrencia_minuto_{i}', pad=(0, 0)),
            sg.Input(size=(6, 2), key=f'saidaOcorrencia_hora_{i}', pad=(0, 0)), sg.Text(':', pad=(0, 0)),
            sg.Input(size=(6, 2), key=f'saidaOcorrencia_minuto_{i}', pad=(0, 0))
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
            preenchimento_horario_manual_personalizado(navegador, valores)

    # Feche a janela de registros
    registro_window.close()
