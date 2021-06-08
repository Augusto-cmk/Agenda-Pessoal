from PySimpleGUI import PySimpleGUI as simple
from functions import main

class TelaError:

    def __init__(self,layout,janela):
        self.layout = layout
        self.janela = janela

    def error(self):
        simple.theme('Reddit')

        self.layout = [
            [simple.Text('Login ou senha inválidos, por favor tente novamente')],
            [simple.Button('Tentar novamente')]
        ]

        self.janela = simple.Window('Agenda',self.layout)

        while True:
            eventos,valores = self.janela.read()
            if eventos == simple.WINDOW_CLOSED:
                break
            if eventos == 'Tentar novamente':
                main()
