import PySimpleGUI as sg


def main_window():
    layout = [[sg.Text('Main Window')],
              [sg.Button('Open Another Window')]]

    window = sg.Window('Main Window', layout)

    while True:
        event, values = window.read()
        if event == sg.WINDOW_CLOSED:
            break
        elif event == 'Open Another Window':
            a_w = AnotherWindow()
            print("b")

    window.close()


class AnotherWindow():
    def __init__(self):
        layout = [[sg.Text('Another Window')],
                  [sg.Button('Close')]]

        window = sg.Window('Another Window', layout)

        while True:
            event, values = window.read()
            if event == sg.WINDOW_CLOSED or event == 'Close':
                break

        window.close()


main_window()
