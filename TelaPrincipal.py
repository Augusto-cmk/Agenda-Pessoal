from PySimpleGUI import PySimpleGUI as simple

class TelaPrincipal:

    def __init__(self,janela,layout,listaCompromissos,agenda):
        self.listaCompromissos = listaCompromissos
        self.agenda = agenda
        self.janela = janela
        self.layout = layout
    
    def tela(self):
        simple.theme('Reddit')

        self.layout = [
            [simple.Text(f'Agenda do(a) {self.agenda.login}')],
            [simple.Text(f"{self.listaCompromissos}")],
            [simple.Button('Alterar compromisso')],
            [simple.Button('Excluir compromisso')],
            [simple.Button('Sair')]
        ]

        self.janela = simple.Window('Agenda',self.layout)

        while True:
            eventos,valores = self.janela.read()
            if eventos == simple.WINDOW_CLOSED:
                break
