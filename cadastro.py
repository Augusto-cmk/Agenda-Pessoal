from PySimpleGUI import PySimpleGUI as simple
from functions import verificaLogin
from functions import mostraCompromissos
from TelaPrincipal import TelaPrincipal
from telaError import TelaError

class Cadastro:

    def __init__(self,agendas):
        self.agendas = agendas

    def Login(self):
        simple.theme('Reddit')
        layout = [
            [simple.Text('Login'),simple.Input(key='login',size=(20,1))],
            [simple.Text('Senha'),simple.Input(key='senha',password_char='*',size=(20,1))],
            [simple.Button('Entrar')]
        ]

        janela = simple.Window('Tela de login',layout)

        while True:
            eventos, valores = janela.read()
            if eventos == simple.WINDOW_CLOSED:
                break
            if eventos == 'Entrar':
                self.login = valores['login']
                self.senha = valores['senha']
                agenda = verificaLogin(self.agendas,self.login,self.senha)
                if agenda == -1:
                    error = TelaError(layout,janela)
                    error.error()
                else:
                    listaCompromissos = mostraCompromissos(agenda.lista_de_compromisso)
                    telaMain = TelaPrincipal(janela,layout,listaCompromissos,agenda)
                    janela.close()
                    telaMain.tela()
                