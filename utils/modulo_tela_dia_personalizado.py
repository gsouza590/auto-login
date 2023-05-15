import PySimpleGUI as sg

def dia_personalizacao():
    # Defina o layout da janela de registros
    registro_layout = [
        [sg.Text('Dia   \t\tEntrada 1    \t\tEntrada 2')]
    ]

    for i in range(1, 32):
        registro_layout.append([
            sg.Text(f'{i}\t'),
            sg.Input(size=(10, 2), key=f'entrada1_hora_{i}'), sg.Text(':'),
            sg.Input(size=(10, 2), key=f'entrada1_minuto_{i}'),
            sg.Input(size=(10, 2), key=f'entrada2_hora_{i}'), sg.Text(':'),
            sg.Input(size=(10, 2), key=f'entrada2_minuto_{i}'),
            sg.Checkbox('Ocorrência Desportiva', key=f'ocorrencia_desportiva_{i}')
        ])

    # Crie a janela de registros
    registro_window = sg.Window('Registros de Horários', registro_layout, finalize=True)

    # Loop de eventos da janela de registros
    while True:
        event, values = registro_window.read()
        if event == sg.WINDOW_CLOSED:
            break

    # Feche a janela de registros
    registro_window.close()

