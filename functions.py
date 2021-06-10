from PySimpleGUI import PySimpleGUI as simple
from agenda import Agenda
from compromisso import Compromisso
from datetime import datetime
from datetime import date
import calendar
from send import envioEmail
from Jarvis import Falar
from Jarvis import Ouvir

class assistente:
    
    def __init__(self,agendas,agenda,listaCompromissos,layout,janela):
        self.listaCompromissos = listaCompromissos
        self.agenda = agenda
        self.janela = janela
        self.layout = layout
        self.agendas = agendas
    
    def telaAssistente(self,metodo,notificar):
        simple.theme('Reddit')
        data = datetime.now()
        horario_print = data.strftime('%H:%M')
        data_print = data.strftime('%d/%m/%Y')
        metodo = 'Padrao'
        self.layout = [
            [simple.Text(f'Bem vindo(a) {self.agenda.login}, selecione o filtro para visualização dos compromissos.')],
            [simple.Text(f'Horário:{horario_print}')],
            [simple.Text(f'Data: {data_print}')],
            [simple.Button('Ano'),simple.Button('Mês'),simple.Button('Semana'),simple.Button('Dia'),simple.Button('Informações adicionais')],
            [simple.Button('Sair'),simple.ButtonMenu('Configuração de notificações',[['Não serve para nada'],['Habilitar notificação de login','Desabilitar notificação de login']],key='Notificar')]
        ]
        
        self.janela = simple.Window('Agenda',self.layout,resizable=True)

        if self.agenda.notificacao == 'enable' and notificar == 0:
            compromissos = self.agenda.filtroDia()
            if len(compromissos) > 1:
                txtComp = mostraCompromissosEmail(compromissos)
                envioEmail(self.agenda.email,'Compromissos do dia',txtComp)
                Falar(f'Você tem um total de {len(compromissos)} compromissos para hoje')
                Falar("Mais detalhes na opção 'dia' de sua agenda, ou em seu e-mail")
                notificar = 1

            if len(compromissos) == 1:
                txtComp = mostraCompromissosEmail(compromissos)
                envioEmail(self.agenda.email,'Compromissos do dia',txtComp)
                Falar(f'Você tem um total de {len(compromissos)} compromisso para hoje')
                Falar("Mais detalhes na opção 'dia' de sua agenda, ou em seu e-mail")
                notificar = 1

            if len(compromissos) == 0:
                Falar('Você não possui compromissos para hoje')
                notificar = 1
        i = 0
        while True:
            eventos,valores = self.janela.read()


            if eventos == simple.WINDOW_CLOSED:
                break

            if eventos == 'Informações adicionais':
                if self.agenda.notificacao == 'disable':
                    Falar('Essa opção só irá funcionar se estiver com a função de notificação ativada em sua agenda')
                if self.agenda.notificacao == 'enable':
                    if i == 0:
                        Falar('Se quiser saber os compromissos da próxima semana, diga o comando "saber mais" quando eu pedir')
                    comando = Ouvir()
                    if comando == 'saber mais':
                        txtProximaSemana = compromissosProximaSemana(self.agenda)
                        if txtProximaSemana != '':
                            Falar('Estou te enviando um e-mail com os compromissos da próxima semana')
                            envioEmail(self.agenda.email,'Compromissos da proxima semana',txtProximaSemana)
                        else:
                            Falar('Você não possui compromissos para a próxima semana')
                        i = 0
                    else:
                        Falar('Não consegui te ouvir, tente novamente')
                        i = 1
            
            if eventos == 'Notificar':
                if valores['Notificar'] == 'Habilitar notificação de login':
                    self.agenda.notificacao = 'enable'
                    Falar('Você ativou a função de notificação de sua agenda. Ao logar, você irá receber um e-mail com os compromissos do dia')
                    Falar('Para que a função de notificação de sua agenda funcione corretamente, você precisa configurar o outlook em seu computador')
                if valores['Notificar'] == 'Desabilitar notificação de login':
                    Falar('Você desativou a função de notificação de sua agenda e não receberá mais e-mails')
                    self.agenda.notificacao = 'disable'

            if eventos == 'Ano':
                filtro = filtroData(self.agendas,self.agenda,self.listaCompromissos,self.layout,self.janela)
                self.janela.close()
                filtro.ano(notificar)
                break
            if eventos == 'Mês':
                filtro = filtroData(self.agendas,self.agenda,self.listaCompromissos,self.layout,self.janela)
                self.janela.close()
                filtro.mes(notificar)
                break
            if eventos == 'Dia':
                filtro = filtroData(self.agendas,self.agenda,self.listaCompromissos,self.layout,self.janela)
                self.janela.close()
                filtro.dia(data.day,metodo,notificar)
                break

            if eventos == 'Sair':
                descarregaDados(self.agendas)
                cadastro = Cadastro(self.agendas,self.agenda,self.listaCompromissos)
                self.janela.close()
                cadastro.Login()
                break

            if eventos == 'Semana':
                filtro = filtroData(self.agendas,self.agenda,self.listaCompromissos,self.layout,self.janela)
                self.janela.close()
                filtro.semana(notificar)
                break

class filtroData:

    def __init__(self,agendas,agenda,listaCompromissos,layout,janela):
        self.listaCompromissos = listaCompromissos
        self.agenda = agenda
        self.janela = janela
        self.layout = layout
        self.agendas = agendas
    
    def ano(self,notificar):
        simple.theme('Reddit')

        compromissos_do_ano = self.agenda.filtroAno()

        lista = listaTxt(compromissos_do_ano)
        
        ano = datetime.now()
        ano_print = ano.strftime('%Y')

        self.layout = [
            [simple.Text(f'Agenda do(a) {self.agenda.login} para {ano_print}')],
            [simple.Listbox(lista,size=(50,10))],
            [simple.Button('Adicionar compromisso')],
            [simple.Button('Alterar compromisso')],
            [simple.Button('Excluir compromisso')],
            [simple.Button('Voltar')],
            [simple.Button('Sair')]
        ]
        
        self.janela = simple.Window('Agenda',self.layout,resizable=True)

        while True:
            eventos,valores = self.janela.read()
            if eventos == simple.WINDOW_CLOSED:
                descarregaDados(self.agendas)
                break
            if eventos == 'Sair':
                self.janela.close()
                descarregaDados(self.agendas)
                main()
            if eventos == 'Alterar compromisso':
                altera = alteraCompromisso(self.agendas,self.agenda,self.listaCompromissos,self.layout,self.janela)
                self.janela.close()
                altera.alteraCompromisso(periodo = 'Ano',dia = 'Ano',metodo = 'Ano',notificar=notificar)
                break
            if eventos == 'Adicionar compromisso':
                alterar = alteraCompromisso(self.agendas,self.agenda,self.listaCompromissos,self.layout,self.janela)
                self.janela.close()
                alterar.criaCompromisso(dia = 'Ano',metodo = 'Ano',periodo = 'Ano',notificar=notificar)
                break
            if eventos == 'Excluir compromisso':
                alterar = alteraCompromisso(self.agendas,self.agenda,self.listaCompromissos,self.layout,self.janela)
                self.janela.close()
                alterar.ExcluirCompromisso(dia ='Ano',metodo = 'Ano',periodo = 'Ano',notificar=notificar)
                break
            if eventos == 'Voltar':
                assistent = assistente(self.agendas,self.agenda,self.listaCompromissos,self.layout,self.janela)
                self.janela.close()
                assistent.telaAssistente(metodo = 'ano',notificar=notificar)
                break

    def mes(self,notificar):
        simple.theme('Reddit')

        compromissos_do_mes = self.agenda.filtroMes()

        lista = listaTxt(compromissos_do_mes)
        
        ano = datetime.now()
        mes_print = ano.month

        strMes = retornaNome(mes_print - 1)


        self.layout = [
            [simple.Text(f'Agenda do(a) {self.agenda.login} para {strMes}')],
            [simple.Listbox(lista,size=(50,10))],
            [simple.Button('Adicionar compromisso')],
            [simple.Button('Alterar compromisso')],
            [simple.Button('Excluir compromisso')],
            [simple.Button('Voltar')],
            [simple.Button('Sair')]
        ]
        
        self.janela = simple.Window('Agenda',self.layout,resizable=True)

        while True:
            eventos,valores = self.janela.read()
            if eventos == simple.WINDOW_CLOSED:
                descarregaDados(self.agendas)
                break
            if eventos == 'Sair':
                self.janela.close()
                descarregaDados(self.agendas)
                main()
            if eventos == 'Alterar compromisso':
                altera = alteraCompromisso(self.agendas,self.agenda,self.listaCompromissos,self.layout,self.janela)
                self.janela.close()
                altera.alteraCompromisso(dia = 'Mes',metodo ='Mes',periodo = 'Mes',notificar = notificar)
                break
            if eventos == 'Adicionar compromisso':
                alterar = alteraCompromisso(self.agendas,self.agenda,self.listaCompromissos,self.layout,self.janela)
                self.janela.close()
                alterar.criaCompromisso(dia ='Mes',metodo ='Mes',periodo = 'Mes',notificar=notificar)
                break
            if eventos == 'Excluir compromisso':
                alterar = alteraCompromisso(self.agendas,self.agenda,self.listaCompromissos,self.layout,self.janela)
                self.janela.close()
                alterar.ExcluirCompromisso(dia='Mes',metodo = 'Mes',periodo = 'Mes',notificar=notificar)
                break
            if eventos == 'Voltar':
                assistent = assistente(self.agendas,self.agenda,self.listaCompromissos,self.layout,self.janela)
                self.janela.close()
                assistent.telaAssistente(metodo ='Mes',notificar=notificar)
                break

    def dia(self,dia,metodo,notificar):
        if metodo == 'Padrao':
            simple.theme('Reddit')

            compromissos_do_dia = self.agenda.filtroDia()

            lista = listaTxt(compromissos_do_dia)

            self.layout = [
                [simple.Text(f'Compromissos do(a) {self.agenda.login} para hoje')],
                [simple.Listbox(lista,size=(50,10))],
                [simple.Button('Adicionar compromisso')],
                [simple.Button('Alterar compromisso')],
                [simple.Button('Excluir compromisso')],
                [simple.Button('Voltar')],
                [simple.Button('Sair')]
            ]
            
            self.janela = simple.Window('Agenda',self.layout,resizable=True)

            while True:
                eventos,valores = self.janela.read()
                if eventos == simple.WINDOW_CLOSED:
                    descarregaDados(self.agendas)
                    break
                if eventos == 'Sair':
                    self.janela.close()
                    descarregaDados(self.agendas)
                    main()
                if eventos == 'Alterar compromisso':
                    altera = alteraCompromisso(self.agendas,self.agenda,self.listaCompromissos,self.layout,self.janela)
                    self.janela.close()
                    altera.alteraCompromisso('Dia',dia,metodo,notificar)
                    break
                if eventos == 'Adicionar compromisso':
                    alterar = alteraCompromisso(self.agendas,self.agenda,self.listaCompromissos,self.layout,self.janela)
                    self.janela.close()
                    alterar.criaCompromisso('Dia',dia,metodo,notificar=1)
                    break
                if eventos == 'Excluir compromisso':
                    alterar = alteraCompromisso(self.agendas,self.agenda,self.listaCompromissos,self.layout,self.janela)
                    self.janela.close()
                    alterar.ExcluirCompromisso('Dia',dia,metodo,notificar=1)
                    break
                if eventos == 'Voltar':
                    assistent = assistente(self.agendas,self.agenda,self.listaCompromissos,self.layout,self.janela)
                    self.janela.close()
                    assistent.telaAssistente(metodo,notificar)
                    break
        if metodo == 'Semana':
            simple.theme('Reddit')

            compromissos_do_dia = self.agenda.filtroDiaSemana(dia)

            lista = listaTxt(compromissos_do_dia)

            self.layout = [
                [simple.Text(f'Compromissos do(a) {self.agenda.login} para o dia {dia}')],
                [simple.Listbox(lista,size=(50,10))],
                [simple.Button('Adicionar compromisso')],
                [simple.Button('Alterar compromisso')],
                [simple.Button('Excluir compromisso')],
                [simple.Button('Voltar')],
                [simple.Button('Sair')]
            ]
            
            self.janela = simple.Window('Agenda',self.layout,resizable=True)

            while True:
                eventos,valores = self.janela.read()
                if eventos == simple.WINDOW_CLOSED:
                    descarregaDados(self.agendas)
                    break
                if eventos == 'Sair':
                    self.janela.close()
                    descarregaDados(self.agendas)
                    main()
                if eventos == 'Alterar compromisso':
                    altera = alteraCompromisso(self.agendas,self.agenda,self.listaCompromissos,self.layout,self.janela)
                    self.janela.close()
                    altera.alteraCompromisso('Dia',dia,metodo,notificar)
                    break
                if eventos == 'Adicionar compromisso':
                    alterar = alteraCompromisso(self.agendas,self.agenda,self.listaCompromissos,self.layout,self.janela)
                    self.janela.close()
                    alterar.criaCompromisso('Dia',dia,metodo,notificar=1)
                    break
                if eventos == 'Excluir compromisso':
                    alterar = alteraCompromisso(self.agendas,self.agenda,self.listaCompromissos,self.layout,self.janela)
                    self.janela.close()
                    alterar.ExcluirCompromisso('Dia',dia,metodo,notificar=1)
                    break
                if eventos == 'Voltar':
                    filtro = filtroData(self.agendas,self.agenda,self.listaCompromissos,self.layout,self.janela)
                    self.janela.close()
                    filtro.semana(notificar)
                    break

    def diaSemana(self,dia,notificar):
        simple.theme('Reddit')

        compromissos_do_dia = self.agenda.filtroDiaSemana(dia)


        lista = listaTxt(compromissos_do_dia)

        self.layout = [
            [simple.Text(f'Compromissos do(a) {self.agenda.login} para o dia {dia}')],
            [simple.Listbox(lista,size=(50,10))],
            [simple.Button('Adicionar compromisso')],
            [simple.Button('Alterar compromisso')],
            [simple.Button('Excluir compromisso')],
            [simple.Button('Voltar')],
            [simple.Button('Sair')]
        ]
        
        self.janela = simple.Window('Agenda',self.layout,resizable=True)

        while True:
            eventos,valores = self.janela.read()
            metodo = 'Semana'
            if eventos == simple.WINDOW_CLOSED:
                descarregaDados(self.agendas)
                break
            if eventos == 'Sair':
                self.janela.close()
                descarregaDados(self.agendas)
                main()
            if eventos == 'Alterar compromisso':
                altera = alteraCompromisso(self.agendas,self.agenda,self.listaCompromissos,self.layout,self.janela)
                self.janela.close()
                altera.alteraCompromisso('Dia',dia,metodo,notificar)
                break

            if eventos == 'Adicionar compromisso':
                alterar = alteraCompromisso(self.agendas,self.agenda,self.listaCompromissos,self.layout,self.janela)
                self.janela.close()
                alterar.criaCompromisso('Dia',dia,metodo,notificar=1)
                break
            if eventos == 'Excluir compromisso':
                alterar = alteraCompromisso(self.agendas,self.agenda,self.listaCompromissos,self.layout,self.janela)
                self.janela.close()
                alterar.ExcluirCompromisso('Dia',dia,metodo,notificar=1)
                break
            if eventos == 'Voltar':
                filtro = filtroData(self.agendas,self.agenda,self.listaCompromissos,self.layout,self.janela)
                self.janela.close()
                filtro.semana(notificar)
                break
    
    def semana(self,notificar):
        simple.theme('Reddit')

        dias = diasSemana()

        self.layout = [
            [simple.Text('Selecione o dia da semana que deseja visualizar os comprimissos')],
            [simple.Button('Segunda'),simple.Button('Terça'),simple.Button('Quarta'),simple.Button('Quinta'),
            simple.Button('Sexta'),simple.Button('Sábado'),simple.Button('Domingo')],
            [simple.Button('Voltar')]
        ]
        
        self.janela = simple.Window('Agenda',self.layout,resizable=True)

        while True:
            eventos,valores = self.janela.read()
            metodo = 'Semana'
            if eventos == simple.WINDOW_CLOSED:
                descarregaDados(self.agendas)
                break

            if eventos == 'Segunda':
                filtro = filtroData(self.agendas,self.agenda,self.listaCompromissos,self.layout,self.janela)
                self.janela.close()
                filtro.diaSemana(dias[0],notificar)
                break

            if eventos == 'Terça':
                filtro = filtroData(self.agendas,self.agenda,self.listaCompromissos,self.layout,self.janela)
                self.janela.close()
                filtro.diaSemana(dias[1],notificar)
                break

            if eventos == 'Quarta':
                filtro = filtroData(self.agendas,self.agenda,self.listaCompromissos,self.layout,self.janela)
                self.janela.close()
                filtro.diaSemana(dias[2],notificar)
                break

            if eventos == 'Quinta':
                filtro = filtroData(self.agendas,self.agenda,self.listaCompromissos,self.layout,self.janela)
                self.janela.close()
                filtro.diaSemana(dias[3],notificar)
                break
            
            if eventos == 'Sexta':
                filtro = filtroData(self.agendas,self.agenda,self.listaCompromissos,self.layout,self.janela)
                self.janela.close()
                filtro.diaSemana(dias[4],notificar)
                break
            
            if eventos == 'Sábado':
                filtro = filtroData(self.agendas,self.agenda,self.listaCompromissos,self.layout,self.janela)
                self.janela.close()
                filtro.diaSemana(dias[5],notificar)
                break
            
            if eventos == 'Domingo':
                filtro = filtroData(self.agendas,self.agenda,self.listaCompromissos,self.layout,self.janela)
                self.janela.close()
                filtro.diaSemana(dias[6],notificar)
                break


            if eventos == 'Voltar':
                assistent = assistente(self.agendas,self.agenda,self.listaCompromissos,self.layout,self.janela)
                self.janela.close()
                assistent.telaAssistente(metodo,notificar)
                break

class TelaError:
    
    def __init__(self,agendas,agenda,listaCompromissos,layout,janela):
        self.layout = layout
        self.janela = janela
        self.agendas = agendas
        self.agenda = agenda
        self.listaCompromissos = listaCompromissos

    def errorLogin(self):
        simple.theme('Reddit')

        self.layout = [
            [simple.Text('Login ou senha inválidos, por favor tente novamente')],
            [simple.Button('Tentar novamente')]
        ]

        self.janela = simple.Window('Error',self.layout)

        while True:
            eventos,valores = self.janela.read()
            if eventos == simple.WINDOW_CLOSED:
                break
            if eventos == 'Tentar novamente':
                self.janela.close()
                main()
                break

    def errorSenhaIncompativeis(self):
        simple.theme('Reddit')

        self.layout = [
            [simple.Text('As senhas não correspondem uma com a outra, favor tentar novamente')],
            [simple.Button('Tentar novamente')]
        ]

        self.janela = simple.Window('Error',self.layout)

        while True:
            eventos,valores = self.janela.read()
            if eventos == simple.WINDOW_CLOSED:
                break
            if eventos == 'Tentar novamente':
                self.janela.close()
                cadastro = Cadastro(self.agendas,self.agenda,self.listaCompromissos)
                cadastro.newAgenda()
                break

    def errorNotFind(self,periodo,dia,metodo,notificar):
        simple.theme('Reddit')

        self.layout = [
            [simple.Text('Compromisso não existente, favor tentar novamente')],
            [simple.Button('Tentar novamente')]
        ]

        self.janela = simple.Window('Error',self.layout)

        while True:
            eventos,valores = self.janela.read()
            if eventos == simple.WINDOW_CLOSED:
                break
            if eventos == 'Tentar novamente':
                self.janela.close()
                filtro = filtroData(self.agendas,self.agenda,self.listaCompromissos,self.layout,self.janela)
                if periodo == 'Ano':
                    filtro.ano(notificar)
                if periodo == 'Mes':
                    filtro.mes(notificar)
                if periodo == 'Dia':
                    filtro.dia(dia,metodo,notificar)
                break
    
    def errorLoginExistente(self):
        simple.theme('Reddit')

        self.layout = [
            [simple.Text('Login já existente, favor tentar novamente')],
            [simple.Button('Tentar novamente')]
        ]

        self.janela = simple.Window('Error',self.layout)

        while True:
            eventos,valores = self.janela.read()
            if eventos == simple.WINDOW_CLOSED:
                break
            if eventos == 'Tentar novamente':
                self.janela.close()
                cadastro = Cadastro(self.agendas,self.agenda,self.listaCompromissos)
                cadastro.newAgenda()
                break
    
    def errorCompromissoExistente(self,periodo,dia,metodo,notificar):
        if periodo == 'Ano':
            simple.theme('Reddit')

            self.layout = [
                [simple.Text('Compromisso com titulo semelhante ja existe em sua agenda')],
                [simple.Button('Tentar novamente')]
            ]

            self.janela = simple.Window('Error',self.layout)

            while True:
                eventos,valores = self.janela.read()
                if eventos == simple.WINDOW_CLOSED:
                    break
                if eventos == 'Tentar novamente':
                    self.janela.close()
                    filtro = filtroData(self.agendas,self.agenda,self.listaCompromissos,self.layout,self.janela)
                    filtro.ano(notificar)
                    break
        
        if periodo == 'Mes':
            simple.theme('Reddit')

            self.layout = [
                [simple.Text('Compromisso com titulo semelhante ja existe em sua agenda')],
                [simple.Button('Tentar novamente')]
            ]

            self.janela = simple.Window('Error',self.layout)

            while True:
                eventos,valores = self.janela.read()
                if eventos == simple.WINDOW_CLOSED:
                    break
                if eventos == 'Tentar novamente':
                    self.janela.close()
                    filtro = filtroData(self.agendas,self.agenda,self.listaCompromissos,self.layout,self.janela)
                    filtro.mes(notificar)
                    break

        if periodo == 'Dia':
            simple.theme('Reddit')

            self.layout = [
                [simple.Text('Compromisso com titulo semelhante ja existe em sua agenda')],
                [simple.Button('Tentar novamente')]
            ]

            self.janela = simple.Window('Error',self.layout)

            while True:
                eventos,valores = self.janela.read()
                if eventos == simple.WINDOW_CLOSED:
                    break
                if eventos == 'Tentar novamente':
                    self.janela.close()
                    filtro = filtroData(self.agendas,self.agenda,self.listaCompromissos,self.layout,self.janela)
                    filtro.dia(dia,metodo,notificar)
                    break

    def errorCompromissoHorario(self,periodo,dia,metodo,notificar):
        if periodo == 'Ano':
            simple.theme('Reddit')

            self.layout = [
                [simple.Text('Compromisso com mesmo horário já existe em sua agenda')],
                [simple.Button('Tentar novamente')]
            ]

            self.janela = simple.Window('Error',self.layout)

            while True:
                eventos,valores = self.janela.read()
                if eventos == simple.WINDOW_CLOSED:
                    break
                if eventos == 'Tentar novamente':
                    self.janela.close()
                    filtro = filtroData(self.agendas,self.agenda,self.listaCompromissos,self.layout,self.janela)
                    filtro.ano(notificar)
                    break
        
        if periodo == 'Mes':
            simple.theme('Reddit')

            self.layout = [
                [simple.Text('Compromisso com mesmo horário já existe em sua agenda')],
                [simple.Button('Tentar novamente')]
            ]

            self.janela = simple.Window('Error',self.layout)

            while True:
                eventos,valores = self.janela.read()
                if eventos == simple.WINDOW_CLOSED:
                    break
                if eventos == 'Tentar novamente':
                    self.janela.close()
                    filtro = filtroData(self.agendas,self.agenda,self.listaCompromissos,self.layout,self.janela)
                    filtro.mes(notificar)
                    break

        if periodo == 'Dia':
            simple.theme('Reddit')

            self.layout = [
                [simple.Text('Compromisso com mesmo horário já existe em sua agenda')],
                [simple.Button('Tentar novamente')]
            ]

            self.janela = simple.Window('Error',self.layout)

            while True:
                eventos,valores = self.janela.read()
                if eventos == simple.WINDOW_CLOSED:
                    break
                if eventos == 'Tentar novamente':
                    self.janela.close()
                    filtro = filtroData(self.agendas,self.agenda,self.listaCompromissos,self.layout,self.janela)
                    filtro.dia(dia,metodo,notificar)
                    break

    def errorPreencher(self,periodo,dia,metodo,classe,compromisso,notificar):
        simple.theme('Reddit')

        self.layout = [
            [simple.Text('Um dos campos não foram preechidos, favor tentar novamente')],
            [simple.Button('Tentar novamente')]
        ]

        self.janela = simple.Window('Error',self.layout)

        while True:
            eventos,valores = self.janela.read()
            if eventos == simple.WINDOW_CLOSED:
                break
            if eventos == 'Tentar novamente':
                lista_verifica = ['Titulo','Data','Hora','Descricao']
                if classe in lista_verifica:
                    self.janela.close()
                    txtCompromisso = TxtCompromisso(compromisso)
                    alterar = altera(self.agendas,self.agenda,compromisso,txtCompromisso,self.layout,self.janela)
                    alterar.alteraComp(periodo,dia,metodo,notificar)
                else:
                    self.janela.close()
                    alterar = alteraCompromisso(self.agendas,self.agenda,self.listaCompromissos,self.layout,self.janela)
                    alterar.criaCompromisso(periodo,dia,metodo,notificar=1)
                break
    
    def errorPreencherCadastro(self):
        simple.theme('Reddit')

        self.layout = [
            [simple.Text('Os campos de cadastro não foram completamente preenchidos, favor tentar novamente')],
            [simple.Button('Tentar novamente')]
        ]

        self.janela = simple.Window('Error',self.layout)

        while True:
            eventos,valores = self.janela.read()
            if eventos == simple.WINDOW_CLOSED:
                break
            if eventos == 'Tentar novamente':
                self.janela.close()
                cadastro = Cadastro(self.agendas,self.agenda,self.listaCompromissos)
                cadastro.newAgenda()
                break
    
    def errorDiaPassado(self,periodo,dia,metodo):
        simple.theme('Reddit')

        self.layout = [
            [simple.Text('O dia para o qual deseja adicionar um compromisso já se passou.')],
            [simple.Button('Tentar novamente')]
        ]

        self.janela = simple.Window('Error',self.layout)

        while True:
            eventos,valores = self.janela.read()
            if eventos == simple.WINDOW_CLOSED:
                break
            if eventos == 'Tentar novamente':
                self.janela.close()
                alterar = alteraCompromisso(self.agendas,self.agenda,self.listaCompromissos,self.layout,self.janela)
                alterar.criaCompromisso(periodo,dia,metodo,notificar=1)
                break
    
    def errorHoraPassada(self,periodo,dia,metodo):
        simple.theme('Reddit')

        self.layout = [
            [simple.Text('A hora para a qual deseja adicionar neste compromissa já se passou.')],
            [simple.Button('Tentar novamente')]
        ]

        self.janela = simple.Window('Error',self.layout)

        while True:
            eventos,valores = self.janela.read()
            if eventos == simple.WINDOW_CLOSED:
                break
            if eventos == 'Tentar novamente':
                self.janela.close()
                alterar = alteraCompromisso(self.agendas,self.agenda,self.listaCompromissos,self.layout,self.janela)
                alterar.criaCompromisso(periodo,dia,metodo,notificar=1)
                break
    
class Cadastro:
    
    def __init__(self,agendas,agenda,listaCompromissos):
        self.agendas = agendas
        self.agenda = agenda
        self.listaCompromissos = listaCompromissos

    def Login(self):
        simple.theme('Reddit')
        layout = [
            [simple.Text('Login'),simple.Input(key='login',size=(20,1))],
            [simple.Text('Senha'),simple.Input(key='senha',password_char='*',size=(20,1))],
            [simple.Button('Entrar'),simple.Button('Novo cadastro')]
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
                    error = TelaError(self.agendas,self.agenda,self.listaCompromissos,layout,janela)
                    janela.close()
                    error.errorLogin()
                else:
                    listaCompromissos = mostraCompromissos(agenda.lista_de_compromisso)
                    assist = assistente(self.agendas,agenda,listaCompromissos,layout,janela)
                    Falar('Seja bem vindo a sua agenda')
                    janela.close()
                    assist.telaAssistente(' ',notificar=0)
                    break
            if eventos == 'Novo cadastro':
                cadastro = Cadastro(self.agendas,self.agenda,self.listaCompromissos)
                janela.close()
                cadastro.newAgenda()
    
    def newAgenda(self):
        simple.theme('Reddit')
        layout = [
            [simple.Text('Login'),simple.Input(key='login',size=(20,1))],
            [simple.Text('Senha'),simple.Input(key='senha',password_char='*',size=(20,1))],
            [simple.Text('Digite a senha novamente'),simple.Input(key='senhaRep',password_char='*',size=(20,1))],
            [simple.Text('Seu melhor e-mail'),simple.Input(key='email',size=(20,1))],
            [simple.Checkbox('Habilitar notificação por e-mail',key='Notificacao')],
            [simple.Button('Cadastrar'),simple.Button('Voltar')]
        ]

        janela = simple.Window('Tela de login',layout)

        while True:
            eventos, valores = janela.read()

            analise_valores = [valores['login'],valores['senha'],valores['senhaRep'],valores['email']]

            if eventos == simple.WINDOW_CLOSED:
                break
            if eventos == 'Cadastrar':
                lista = listaLogins(self.agendas)
                analise = 0

                if '' in analise_valores:
                    analise = -1

                if valores['login'] in lista:
                    janela.close()
                    error = TelaError(self.agendas,self.agenda,self.listaCompromissos,layout,janela)
                    error.errorLoginExistente()
                    break

                if valores['senha'] == valores['senhaRep'] and analise == 0:
                    if valores['Notificacao'] == True:
                        notificar = 'enable'
                    else:
                        notificar = 'disable'

                    agenda = criaAgenda(self.agendas,valores['login'],valores['senha'],valores['email'],notificar)
                    self.agendas.append(agenda)
                    login = Cadastro(self.agendas,self.agenda,self.listaCompromissos)
                    janela.close()
                    if notificar == 'enable':
                        Falar('Para que a função de notificação de sua agenda funcione corretamente, você precisa configurar o outlook em seu computador')
                    login.Login()
                    break

                if analise == -1:
                    error = TelaError(self.agendas,self.agenda,self.listaCompromissos,layout,janela)
                    janela.close()
                    error.errorPreencherCadastro()
                    break

                else:
                    error = TelaError(self.agendas,self.agenda,self.listaCompromissos,layout,janela)
                    janela.close()
                    error.errorSenhaIncompativeis()
                    break

            if eventos == 'Voltar':
                cadastro = Cadastro(self.agendas,self.agenda,self.listaCompromissos)
                janela.close()
                cadastro.Login()
                break

class alteraCompromisso:

    def __init__(self,agendas,agenda,listaCompromissos,layout,janela):
        self.layout = layout
        self.janela = janela
        self.agenda = agenda
        self.listaCompromissos = listaCompromissos
        self.agendas = agendas
    
    def alteraCompromisso(self,periodo,dia,metodo,notificar):
        if periodo == 'Ano':

            compromissos_do_ano = self.agenda.filtroAno()

            simple.theme('Reddit')
            lista = listaTxt(compromissos_do_ano)

            self.layout = [
                [simple.Listbox(lista,size=(50,10))],
                [simple.Text('Titulo do compromisso'),simple.Input(key='Titulo do compromisso',size=(20,1))],
                [simple.Button('Alterar'),simple.Button('Voltar')]
            ]

            self.janela = simple.Window('Compromisso',self.layout)

            while True:
                eventos, valores = self.janela.read()
                if eventos == simple.WINDOW_CLOSED:
                    descarregaDados(self.agendas)
                    break

                if eventos == 'Alterar':
                    compromisso,txtCompromisso = encontraCompromisso(self.agenda,valores['Titulo do compromisso'])
                    if compromisso == -1 and txtCompromisso == -1:
                        error = TelaError(self.agendas,self.agenda,self.listaCompromissos,self.layout,self.janela)
                        self.janela.close()
                        error.errorNotFind(periodo,dia,metodo,notificar)
                        break

                    else:
                        alteracao = altera(self.agendas,self.agenda,compromisso,txtCompromisso,self.layout,self.janela)
                        self.janela.close()
                        alteracao.alteraComp('Ano',dia,metodo,notificar)
                        break
                
                if eventos == 'Voltar':
                    filtro = filtroData(self.agendas,self.agenda,self.listaCompromissos,self.layout,self.janela)
                    self.janela.close()
                    filtro.ano(notificar)
                    break

        if periodo == 'Mes':
            compromissos_do_mes = self.agenda.filtroMes()

            simple.theme('Reddit')
            lista = listaTxt(compromissos_do_mes)

            self.layout = [
                [simple.Listbox(lista,size=(50,10))],
                [simple.Text('Titulo do compromisso'),simple.Input(key='Titulo do compromisso',size=(20,1))],
                [simple.Button('Alterar'),simple.Button('Voltar')]
            ]

            self.janela = simple.Window('Compromisso',self.layout)

            while True:
                eventos, valores = self.janela.read()
                if eventos == simple.WINDOW_CLOSED:
                    descarregaDados(self.agendas)
                    break

                if eventos == 'Alterar':
                    compromisso,txtCompromisso = encontraCompromisso(self.agenda,valores['Titulo do compromisso'])
                    if compromisso == -1 and txtCompromisso == -1:
                        error = TelaError(self.agendas,self.agenda,self.listaCompromissos,self.layout,self.janela)
                        self.janela.close()
                        error.errorNotFind(periodo,dia,metodo,notificar)
                        break

                    else:
                        alteracao = altera(self.agendas,self.agenda,compromisso,txtCompromisso,self.layout,self.janela)
                        self.janela.close()
                        alteracao.alteraComp('Mes',dia,metodo,notificar)
                        break

                if eventos == 'Voltar':
                    filtro = filtroData(self.agendas,self.agenda,self.listaCompromissos,self.layout,self.janela)
                    self.janela.close()
                    filtro.mes(notificar)
                    break

        if periodo == 'Dia':

            compromissos_do_dia = self.agenda.filtroDiaSemana(dia)
            
            simple.theme('Reddit')
            lista = listaTxt(compromissos_do_dia)

            self.layout = [
                [simple.Listbox(lista,size=(50,10))],
                [simple.Text('Titulo do compromisso'),simple.Input(key='Titulo do compromisso',size=(20,1))],
                [simple.Button('Alterar'),simple.Button('Voltar')]
            ]

            self.janela = simple.Window('Compromisso',self.layout)

            while True:
                eventos, valores = self.janela.read()
                if eventos == simple.WINDOW_CLOSED:
                    descarregaDados(self.agendas)
                    break

                if eventos == 'Alterar':
                    compromisso,txtCompromisso = encontraCompromisso(self.agenda,valores['Titulo do compromisso'])
                    if compromisso == -1 and txtCompromisso == -1:
                        error = TelaError(self.agendas,self.agenda,self.listaCompromissos,self.layout,self.janela)
                        self.janela.close()
                        error.errorNotFind(periodo,dia,metodo,notificar)
                        break

                    else:
                        alteracao = altera(self.agendas,self.agenda,compromisso,txtCompromisso,self.layout,self.janela)
                        self.janela.close()
                        alteracao.alteraComp('Dia',dia,metodo,notificar)
                        break

                if eventos == 'Voltar':
                    filtro = filtroData(self.agendas,self.agenda,self.listaCompromissos,self.layout,self.janela)
                    self.janela.close()
                    filtro.dia(dia,metodo,notificar)
                    break

    def criaCompromisso(self,periodo,dia,metodo,notificar):
        if periodo == 'Ano':
            simple.theme('Reddit')
            self.layout = [
                [simple.Text('Titulo do compromisso'),simple.Input(key='Titulo do compromisso',size=(20,1))],
                [simple.Text('Dia e mês do compromisso'),simple.Input(key='Dia e mes',size=(20,1))],
                [simple.Text('Horário'),simple.Input(key='Horario',size=(20,1))],
                [simple.Text('Descrição do compromisso'),simple.Input(key='Descrição',size=(20,1))],
                [simple.Button('Criar'),simple.ButtonMenu('Repetir compromisso',[['Não serve para nada'],['Repetir semanalmente','Repetir até uma data']],key='Repetir'),simple.Button('Voltar')]
            ]

            self.janela = simple.Window('Cria compromisso',self.layout)

            flag_verificaMenu = 0

            while True:
                eventos, valores = self.janela.read()

                vetor_analise = [valores['Titulo do compromisso'],valores['Dia e mes'],valores['Horario'],valores['Descrição']]

                if eventos == simple.WINDOW_CLOSED:
                    descarregaDados(self.agendas)
                    break

                if eventos == 'Repetir':
                    if valores['Repetir'] == 'Repetir semanalmente':
                        flag_verificaMenu = 1
                    if valores['Repetir'] == 'Repetir até uma data':
                        flag_verificaMenu = 2

                if eventos == 'Criar':
                    ano = datetime.now()
                    dia_atual = ano.day
                    mes_atual = ano.month
                    ano_print = ano.strftime('/%Y')
                    data = valores['Dia e mes'] + ano_print
                    compromisso = CriaCompromisso(valores['Titulo do compromisso'],data,valores['Horario'],valores['Descrição'])
                    resultado = self.agenda.verificaExistencia(compromisso)
                    resposta = self.agenda.verificaHorario(compromisso)
                    horario = valores['Horario']
                    hora_atual = ano.hour
                    minuto_atual = ano.minute
                    hora_entrada = horario[0:2]
                    minuto_entrada = horario[-2:]
                    analise = 0
                    possibilidade = 0
                    possivel_horario = 0
                    dia_entrada = data[0:2]
                    mes_entrada = data[3:5]

                    if '' in vetor_analise:
                        analise = -1
                    
                    if analise == 0:
                        if (int(dia_entrada) == dia_atual and int(mes_entrada) < mes_atual) or (int(dia_entrada) < dia_atual and int(mes_entrada) == mes_atual):
                            possibilidade = -1
                        if (dia_atual == int(dia_entrada) and mes_atual == int(mes_entrada)) and ((hora_atual == int(hora_entrada) and minuto_atual > int(minuto_entrada)) or hora_atual > int(hora_entrada)):
                            possivel_horario = -1

                    if resultado == 0 and resposta == 0 and analise == 0 and possibilidade == 0 and possivel_horario == 0:
                        if flag_verificaMenu == 0:
                            allocaCompromisso(self.agenda,compromisso)
                            descarregaDados(self.agendas)
                            self.listaCompromissos = mostraCompromissos(self.agenda.lista_de_compromisso)
                            filtro = filtroData(self.agendas,self.agenda,self.listaCompromissos,self.layout,self.janela)
                            self.janela.close()
                            filtro.ano(notificar)

                        if flag_verificaMenu == 1:
                            alterar = alteraCompromisso(self.agendas,self.agenda,self.listaCompromissos,self.layout,self.janela)
                            self.janela.close()
                            alterar.repeteCompromisso('Semanalmente',compromisso,compromisso.data,periodo,dia,metodo,notificar=1)
                            

                        if flag_verificaMenu == 2:
                            alterar = alteraCompromisso(self.agendas,self.agenda,self.listaCompromissos,self.layout,self.janela)
                            self.janela.close()
                            alterar.repeteCompromisso('Todos os dias',compromisso,compromisso.data,periodo,dia,metodo,notificar=1)

                        break

                    if resultado == -1:
                        error = TelaError(self.agendas,self.agenda,self.listaCompromissos,self.layout,self.janela)
                        self.janela.close()
                        error.errorCompromissoExistente(periodo,dia,metodo,notificar)
                        break

                    if resposta == -1:
                        error = TelaError(self.agendas,self.agenda,self.listaCompromissos,self.layout,self.janela)
                        self.janela.close()
                        error.errorCompromissoHorario(periodo,dia,metodo,notificar)
                        break

                    if analise == -1:
                        error = TelaError(self.agendas,self.agenda,self.listaCompromissos,self.layout,self.janela)
                        self.janela.close()
                        error.errorPreencher(periodo,dia,metodo,' ',' ',notificar)
                        break

                    if possibilidade == -1:
                        error = TelaError(self.agendas,self.agenda,self.listaCompromissos,self.layout,self.janela)
                        self.janela.close()
                        error.errorDiaPassado(periodo,dia,metodo)
                        break

                    if possivel_horario == -1:
                        error = TelaError(self.agendas,self.agenda,self.listaCompromissos,self.layout,self.janela)
                        self.janela.close()
                        error.errorHoraPassada(periodo,dia,metodo)
                        break
                    break
                
                if eventos == 'Voltar':
                    self.listaCompromissos = mostraCompromissos(self.agenda.lista_de_compromisso)
                    filtro = filtroData(self.agendas,self.agenda,self.listaCompromissos,self.layout,self.janela)
                    self.janela.close()
                    filtro.ano(notificar)
                    break

        if periodo == 'Mes':
            simple.theme('Reddit')
            self.layout = [
                [simple.Text('Titulo do compromisso'),simple.Input(key='Titulo do compromisso',size=(20,1))],
                [simple.Text('Dia do compromisso'),simple.Input(key='Dia',size=(20,1))],
                [simple.Text('Horário'),simple.Input(key='Horario',size=(20,1))],
                [simple.Text('Descrição do compromisso'),simple.Input(key='Descrição',size=(20,1))],
                [simple.Button('Criar'),simple.ButtonMenu('Repetir compromisso',[['Não serve para nada'],['Repetir semanalmente','Repetir até uma data']],key='Repetir'),simple.Button('Voltar')]
            ]

            self.janela = simple.Window('Cria compromisso',self.layout)
            flag_verificaMenu = 0

            while True:
                eventos, valores = self.janela.read()

                vetor_analise = [valores['Titulo do compromisso'],valores['Dia'],valores['Horario'],valores['Descrição']]

                if eventos == simple.WINDOW_CLOSED:
                    descarregaDados(self.agendas)
                    break
                if eventos == 'Repetir':
                    if valores['Repetir'] == 'Repetir semanalmente':
                        flag_verificaMenu = 1
                    if valores['Repetir'] == 'Repetir até uma data':
                        flag_verificaMenu = 2

                if eventos == 'Criar':
                    ano = datetime.now()
                    ano_print = ano.strftime('/%m/%Y')
                    data = valores['Dia'] + ano_print
                    compromisso = CriaCompromisso(valores['Titulo do compromisso'],data,valores['Horario'],valores['Descrição'])
                    resultado = self.agenda.verificaExistencia(compromisso)
                    resposta = self.agenda.verificaHorario(compromisso)
                    analise = 0
                    analise = 0
                    possibilidade = 0
                    dia_entrada = data[0:2]
                    dia_atual = ano.day
                    horario = valores['Horario']
                    hora_atual = ano.hour
                    minuto_atual = ano.minute
                    hora_entrada = horario[0:2]
                    minuto_entrada = horario[-2:]
                    possivel_horario = 0

                    if '' in vetor_analise:
                        analise = -1
                    
                    if analise == 0:
                        if int(dia_entrada) < dia_atual:
                            possibilidade = -1
                        if (int(dia_entrada) == dia_atual) and ((hora_atual == int(hora_entrada) and minuto_atual > int(minuto_entrada)) or hora_atual > int(hora_entrada)):
                            possivel_horario = -1

                    if resultado == 0 and resposta == 0 and analise == 0 and possibilidade == 0 and possivel_horario == 0:
                        
                        if flag_verificaMenu == 0:
                            allocaCompromisso(self.agenda,compromisso)
                            descarregaDados(self.agendas)
                            self.listaCompromissos = mostraCompromissos(self.agenda.lista_de_compromisso)
                            filtro = filtroData(self.agendas,self.agenda,self.listaCompromissos,self.layout,self.janela)
                            self.janela.close()
                            filtro.mes(notificar)

                        if flag_verificaMenu == 1:
                            alterar = alteraCompromisso(self.agendas,self.agenda,self.listaCompromissos,self.layout,self.janela)
                            self.janela.close()
                            alterar.repeteCompromisso('Semanalmente',compromisso,compromisso.data,periodo,dia,metodo,notificar=1)
                            

                        if flag_verificaMenu == 2:
                            alterar = alteraCompromisso(self.agendas,self.agenda,self.listaCompromissos,self.layout,self.janela)
                            self.janela.close()
                            alterar.repeteCompromisso('Todos os dias',compromisso,compromisso.data,periodo,dia,metodo,notificar=1)
                        
                        allocaCompromisso(self.agenda,compromisso)
                        descarregaDados(self.agendas)
                        self.listaCompromissos = mostraCompromissos(self.agenda.lista_de_compromisso)
                        filtro = filtroData(self.agendas,self.agenda,self.listaCompromissos,self.layout,self.janela)
                        self.janela.close()
                        filtro.mes(notificar)
                        break

                    if resultado == -1:
                        error = TelaError(self.agendas,self.agenda,self.listaCompromissos,self.layout,self.janela)
                        self.janela.close()
                        error.errorCompromissoExistente(periodo,dia,metodo,notificar)
                        break

                    if resposta == -1:
                        error = TelaError(self.agendas,self.agenda,self.listaCompromissos,self.layout,self.janela)
                        self.janela.close()
                        error.errorCompromissoHorario(periodo,dia,metodo,notificar)
                        break
                        
                    if analise == -1:
                        error = TelaError(self.agendas,self.agenda,self.listaCompromissos,self.layout,self.janela)
                        self.janela.close()
                        error.errorPreencher(periodo,dia,metodo,' ',' ',notificar)
                        break
                    
                    if possibilidade == -1:
                        error = TelaError(self.agendas,self.agenda,self.listaCompromissos,self.layout,self.janela)
                        self.janela.close()
                        error.errorDiaPassado(periodo,dia,metodo)
                        break

                    if possivel_horario == -1:
                        error = TelaError(self.agendas,self.agenda,self.listaCompromissos,self.layout,self.janela)
                        self.janela.close()
                        error.errorHoraPassada(periodo,dia,metodo)
                        break
                    break

                if eventos == 'Voltar':
                    self.listaCompromissos = mostraCompromissos(self.agenda.lista_de_compromisso)
                    filtro = filtroData(self.agendas,self.agenda,self.listaCompromissos,self.layout,self.janela)
                    self.janela.close()
                    filtro.mes(notificar)
                    break

        if periodo == 'Dia':
            simple.theme('Reddit')
            self.layout = [
                [simple.Text('Titulo do compromisso'),simple.Input(key='Titulo do compromisso',size=(20,1))],
                [simple.Text('Horário'),simple.Input(key='Horario',size=(20,1))],
                [simple.Text('Descrição do compromisso'),simple.Input(key='Descrição',size=(20,1))],
                [simple.Button('Criar'),simple.ButtonMenu('Repetir compromisso',[['Não serve para nada'],['Repetir semanalmente','Repetir até uma data']],key='Repetir'),simple.Button('Voltar')]
            ]

            self.janela = simple.Window('Cria compromisso',self.layout)
            flag_verificaMenu = 0
            while True:
                eventos, valores = self.janela.read()

                vetor_analise = [valores['Titulo do compromisso'],valores['Horario'],valores['Descrição']]

                if eventos == simple.WINDOW_CLOSED:
                    descarregaDados(self.agendas)
                    break

                if eventos == 'Repetir':
                    if valores['Repetir'] == 'Repetir semanalmente':
                        flag_verificaMenu = 1
                    if valores['Repetir'] == 'Repetir até uma data':
                        flag_verificaMenu = 2

                if eventos == 'Criar':
                    ano = datetime.now()
                    ano_print = ano.strftime('/%m/%Y')
                    
                    if dia < 10:
                        strDia = '0'+str(dia)
                    else:
                        strDia = str(dia)

                    data = strDia + ano_print
                    compromisso = CriaCompromisso(valores['Titulo do compromisso'],data,valores['Horario'],valores['Descrição'])
                    resultado = self.agenda.verificaExistencia(compromisso)
                    resposta = self.agenda.verificaHorario(compromisso)
                    analise = 0

                    dia_atual = ano.day
                    possibilidade = 0

                    horario = valores['Horario']
                    hora_atual = ano.hour
                    minuto_atual = ano.minute
                    hora_entrada = horario[0:2]
                    minuto_entrada = horario[-2:]
                    possivel_horario = 0

                    if '' in vetor_analise:
                        analise = -1
                    
                    if analise == 0:
                        if dia < dia_atual:
                            possibilidade = -1
                        if dia == dia_atual and ((hora_atual == int(hora_entrada) and minuto_atual > int(minuto_entrada)) or hora_atual > int(hora_entrada)):
                            possivel_horario = -1

                    if resultado == 0 and resposta == 0 and analise == 0 and possibilidade == 0 and possivel_horario == 0:
                        if flag_verificaMenu == 0:
                            allocaCompromisso(self.agenda,compromisso)
                            descarregaDados(self.agendas)
                            self.listaCompromissos = mostraCompromissos(self.agenda.lista_de_compromisso)
                            filtro = filtroData(self.agendas,self.agenda,self.listaCompromissos,self.layout,self.janela)
                            self.janela.close()
                            filtro.dia(dia,metodo,notificar)
                        
                        if flag_verificaMenu == 1:
                            alterar = alteraCompromisso(self.agendas,self.agenda,self.listaCompromissos,self.layout,self.janela)
                            self.janela.close()
                            alterar.repeteCompromisso('Semanalmente',compromisso,compromisso.data,periodo,dia,metodo,notificar=1)
                            

                        if flag_verificaMenu == 2:
                            alterar = alteraCompromisso(self.agendas,self.agenda,self.listaCompromissos,self.layout,self.janela)
                            self.janela.close()
                            alterar.repeteCompromisso('Todos os dias',compromisso,compromisso.data,periodo,dia,metodo,notificar=1)
                        break

                    if resultado == -1:
                        error = TelaError(self.agendas,self.agenda,self.listaCompromissos,self.layout,self.janela)
                        self.janela.close()
                        error.errorCompromissoExistente(periodo,dia,metodo,notificar)
                        break

                    if resposta == -1:
                        error = TelaError(self.agendas,self.agenda,self.listaCompromissos,self.layout,self.janela)
                        self.janela.close()
                        error.errorCompromissoHorario(periodo,dia,metodo,notificar)
                        break

                    if analise == -1:
                        error = TelaError(self.agendas,self.agenda,self.listaCompromissos,self.layout,self.janela)
                        self.janela.close()
                        error.errorPreencher(periodo,dia,metodo,' ',' ',notificar)
                        break

                    if possibilidade == -1:
                        error = TelaError(self.agendas,self.agenda,self.listaCompromissos,self.layout,self.janela)
                        self.janela.close()
                        error.errorDiaPassado(periodo,dia,metodo)
                        break
                    
                    if possivel_horario == -1:
                        error = TelaError(self.agendas,self.agenda,self.listaCompromissos,self.layout,self.janela)
                        self.janela.close()
                        error.errorHoraPassada(periodo,dia,metodo)
                        break

                    break
                
                if eventos == 'Voltar':
                    self.listaCompromissos = mostraCompromissos(self.agenda.lista_de_compromisso)
                    filtro = filtroData(self.agendas,self.agenda,self.listaCompromissos,self.layout,self.janela)
                    self.janela.close()
                    filtro.dia(dia,metodo,notificar)
                    break
    
    def repeteCompromisso(self,modo,compromisso,dataInicio,periodo,dia,metodo,notificar):
        simple.theme('Reddit')
        self.layout = [
            [simple.Text('Data final'),simple.Input(key='data final',size=(20,1))],
            [simple.Button('Feito'),simple.Button('Voltar')]
        ]

        self.janela = simple.Window('Cria compromisso',self.layout)

        while True:
            eventos, valores = self.janela.read()

            if eventos == simple.WINDOW_CLOSED:
                descarregaDados(self.agendas)
                break

            if eventos == 'Feito':
                repeteCompromisso(self.agenda,compromisso,dataInicio,valores['data final'],modo)
                self.janela.close()
                filtro = filtroData(self.agendas,self.agenda,self.listaCompromissos,self.layout,self.janela)
                if periodo == 'Ano':
                    filtro.ano(notificar)
                if periodo == 'Mes':
                    filtro.mes(notificar)
                if periodo == 'Dia':
                    filtro.dia(dia,metodo,notificar)
            if eventos == 'Voltar':
                altera = alteraCompromisso(self.agendas,self.agenda,self.listaCompromissos,self.layout,self.janela)
                self.janela.close()
                altera.criaCompromisso(periodo,dia,metodo,notificar)
            break


    def ExcluirCompromisso(self,periodo,dia,metodo,notificar):
        if periodo == 'Ano':
            simple.theme('Reddit')
            compromissos_do_ano = self.agenda.filtroAno()

            lista = listaTxt(compromissos_do_ano)

            self.layout = [
                [simple.Listbox(lista,size=(50,10))],
                [simple.Text('Titulo do compromisso'),simple.Input(key='Titulo do compromisso',size=(20,1))],
                [simple.Button('Excluir'),simple.Button('Excluir compromissos repetidos'),simple.Button('Voltar')]
            ]

            self.janela = simple.Window('Excluir Compromisso',self.layout)

            while True:
                eventos, valores = self.janela.read()
                if eventos == simple.WINDOW_CLOSED:
                    descarregaDados(self.agendas)
                    break

                if eventos == 'Excluir':
                    flag = deletaCompromisso(self.agenda,valores['Titulo do compromisso'])
                    if flag == -1:
                        error = TelaError(self.agendas,self.agenda,self.listaCompromissos,self.layout,self.janela)
                        self.janela.close()
                        error.errorNotFind(periodo,dia,metodo,notificar)
                    else:    
                        self.listaCompromissos = mostraCompromissos(self.agenda.lista_de_compromisso)
                        filtro = filtroData(self.agendas,self.agenda,self.listaCompromissos,self.layout,self.janela)
                        descarregaDados(self.agendas)
                        self.janela.close()
                        filtro.ano(notificar)
                        break
                
                if eventos == 'Excluir compromissos repetidos':
                    flag = excluiRepetidos(self.agenda,valores['Titulo do compromisso'])
                    if flag == -1:
                        error = TelaError(self.agendas,self.agenda,self.listaCompromissos,self.layout,self.janela)
                        self.janela.close()
                        error.errorNotFind(periodo,dia,metodo,notificar)
                        break
                    else:
                        self.listaCompromissos = mostraCompromissos(self.agenda.lista_de_compromisso)
                        filtro = filtroData(self.agendas,self.agenda,self.listaCompromissos,self.layout,self.janela)
                        descarregaDados(self.agendas)
                        self.janela.close()
                        filtro.ano(notificar)
                        break
                
                if eventos == 'Voltar':
                    filtro = filtroData(self.agendas,self.agenda,self.listaCompromissos,self.layout,self.janela)
                    self.janela.close()
                    filtro.ano(notificar)

        if periodo == 'Mes':
            simple.theme('Reddit')

            compromissos_do_mes = self.agenda.filtroMes()

            lista = listaTxt(compromissos_do_mes)

            self.layout = [
                [simple.Listbox(lista,size=(50,10))],
                [simple.Text('Titulo do compromisso'),simple.Input(key='Titulo do compromisso',size=(20,1))],
                [simple.Button('Excluir'),simple.Button('Excluir compromissos repetidos'),simple.Button('Voltar')]
            ]

            self.janela = simple.Window('Excluir Compromisso',self.layout)

            while True:
                eventos, valores = self.janela.read()
                if eventos == simple.WINDOW_CLOSED:
                    descarregaDados(self.agendas)
                    break

                if eventos == 'Excluir':
                    flag = deletaCompromisso(self.agenda,valores['Titulo do compromisso'])
                    if flag == -1:
                        error = TelaError(self.agendas,self.agenda,self.listaCompromissos,self.layout,self.janela)
                        self.janela.close()
                        error.errorNotFind(periodo,dia,metodo,notificar)
                    else:    
                        self.listaCompromissos = mostraCompromissos(self.agenda.lista_de_compromisso)
                        filtro = filtroData(self.agendas,self.agenda,self.listaCompromissos,self.layout,self.janela)
                        descarregaDados(self.agendas)
                        self.janela.close()
                        filtro.mes(notificar)
                        break
                
                if eventos == 'Excluir compromissos repetidos':
                    flag = excluiRepetidos(self.agenda,valores['Titulo do compromisso'])
                    if flag == -1:
                        error = TelaError(self.agendas,self.agenda,self.listaCompromissos,self.layout,self.janela)
                        self.janela.close()
                        error.errorNotFind(periodo,dia,metodo,notificar)
                        break
                    else:
                        self.listaCompromissos = mostraCompromissos(self.agenda.lista_de_compromisso)
                        filtro = filtroData(self.agendas,self.agenda,self.listaCompromissos,self.layout,self.janela)
                        descarregaDados(self.agendas)
                        self.janela.close()
                        filtro.ano(notificar)
                        break

                if eventos == 'Voltar':
                    filtro = filtroData(self.agendas,self.agenda,self.listaCompromissos,self.layout,self.janela)
                    self.janela.close()
                    filtro.mes(notificar)

        if periodo == 'Dia':
            simple.theme('Reddit')

            compromissos_do_dia = self.agenda.filtroDiaSemana(dia)

            lista = listaTxt(compromissos_do_dia)

            self.layout = [
                [simple.Listbox(lista,size=(50,10))],
                [simple.Text('Titulo do compromisso'),simple.Input(key='Titulo do compromisso',size=(20,1))],
                [simple.Button('Excluir'),simple.Button('Excluir compromissos repetidos'),simple.Button('Voltar')]
            ]

            self.janela = simple.Window('Excluir Compromisso',self.layout)

            while True:
                eventos, valores = self.janela.read()
                if eventos == simple.WINDOW_CLOSED:
                    descarregaDados(self.agendas)
                    break

                if eventos == 'Excluir':
                    flag = deletaCompromisso(self.agenda,valores['Titulo do compromisso'])
                    if flag == -1:
                        error = TelaError(self.agendas,self.agenda,self.listaCompromissos,self.layout,self.janela)
                        self.janela.close()
                        error.errorNotFind(periodo,dia,metodo,notificar)
                    else:    
                        self.listaCompromissos = mostraCompromissos(self.agenda.lista_de_compromisso)
                        filtro = filtroData(self.agendas,self.agenda,self.listaCompromissos,self.layout,self.janela)
                        descarregaDados(self.agendas)
                        self.janela.close()
                        filtro.dia(dia,metodo,notificar)
                        break
                
                if eventos == 'Excluir compromissos repetidos':
                    flag = excluiRepetidos(self.agenda,valores['Titulo do compromisso'])
                    if flag == -1:
                        error = TelaError(self.agendas,self.agenda,self.listaCompromissos,self.layout,self.janela)
                        self.janela.close()
                        error.errorNotFind(periodo,dia,metodo,notificar)
                        break

                    else:
                        self.listaCompromissos = mostraCompromissos(self.agenda.lista_de_compromisso)
                        filtro = filtroData(self.agendas,self.agenda,self.listaCompromissos,self.layout,self.janela)
                        descarregaDados(self.agendas)
                        self.janela.close()
                        filtro.ano(notificar)
                        break
                
                if eventos == 'Voltar':
                    filtro = filtroData(self.agendas,self.agenda,self.listaCompromissos,self.layout,self.janela)
                    self.janela.close()
                    filtro.dia(dia,metodo,notificar)

    

class altera:
    
    def __init__(self,agendas,agenda,compromisso,txtCompromisso,layout,janela):
        self.layout = layout
        self.janela = janela
        self.compromisso = compromisso
        self.txtCompromisso = txtCompromisso
        self.agenda = agenda
        self.agendas = agendas

    def alteraComp(self,periodo,dia,metodo,notificar):
        if periodo == 'Ano':
            simple.theme('Reddit')
            self.layout = [
                [simple.Text(f'{self.txtCompromisso}')],
                [simple.Button('Alterar titulo')],
                [simple.Button('Alterar data')],
                [simple.Button('Alterar hora')],
                [simple.Button('Alterar descricao')],
                [simple.Button('Voltar')]
            ]

            self.janela = simple.Window('Alterar compromisso',self.layout)

            while True:
                eventos, valores = self.janela.read()
                if eventos == simple.WINDOW_CLOSED:
                    descarregaDados(self.agendas)
                    break

                if eventos == 'Alterar titulo':
                    alterar = alteraTitulo(self.agendas,self.agenda,self.compromisso,self.txtCompromisso,self.layout,self.janela)
                    self.janela.close()
                    alterar.titulo('Ano',dia,metodo,'Titulo')
                    break
                
                if eventos == 'Alterar data':
                    alterar = alteraData(self.agendas,self.agenda,self.compromisso,self.txtCompromisso,self.layout,self.janela)
                    self.janela.close()
                    alterar.data('Ano',dia,metodo,'Data')
                    break

                if eventos == 'Alterar hora':
                    alterar = alteraHora(self.agendas,self.agenda,self.compromisso,self.txtCompromisso,self.layout,self.janela)
                    self.janela.close()
                    alterar.hora('Ano',dia,metodo,'Hora')
                    break

                if eventos == 'Alterar descricao':
                    alterar = alteraDescricao(self.agendas,self.agenda,self.compromisso,self.txtCompromisso,self.layout,self.janela)
                    self.janela.close()
                    alterar.descricao('Ano',dia,metodo,'Descricao')
                    break
            
                if eventos == 'Voltar':
                    listaCompromissos = mostraCompromissos(self.agenda.lista_de_compromisso)
                    filtro = filtroData(self.agendas,self.agenda,listaCompromissos,self.layout,self.janela)
                    self.janela.close()
                    filtro.ano(notificar)
                    break

        if periodo == 'Mes':
            simple.theme('Reddit')
            self.layout = [
                [simple.Text(f'{self.txtCompromisso}')],
                [simple.Button('Alterar titulo')],
                [simple.Button('Alterar data')],
                [simple.Button('Alterar hora')],
                [simple.Button('Alterar descricao')],
                [simple.Button('Voltar')]
            ]

            self.janela = simple.Window('Alterar compromisso',self.layout)

            while True:
                eventos, valores = self.janela.read()
                if eventos == simple.WINDOW_CLOSED:
                    descarregaDados(self.agendas)
                    break

                if eventos == 'Alterar titulo':
                    alterar = alteraTitulo(self.agendas,self.agenda,self.compromisso,self.txtCompromisso,self.layout,self.janela)
                    self.janela.close()
                    alterar.titulo('Mes',dia,metodo,'Titulo')
                    break
                
                if eventos == 'Alterar data':
                    alterar = alteraData(self.agendas,self.agenda,self.compromisso,self.txtCompromisso,self.layout,self.janela)
                    self.janela.close()
                    alterar.data('Mes',dia,metodo,'Data')
                    break

                if eventos == 'Alterar hora':
                    alterar = alteraHora(self.agendas,self.agenda,self.compromisso,self.txtCompromisso,self.layout,self.janela)
                    self.janela.close()
                    alterar.hora('Mes',dia,metodo,'Hora')
                    break

                if eventos == 'Alterar descricao':
                    alterar = alteraDescricao(self.agendas,self.agenda,self.compromisso,self.txtCompromisso,self.layout,self.janela)
                    self.janela.close()
                    alterar.descricao('Mes',dia,metodo,'Descricao')
                    break
            
                if eventos == 'Voltar':
                    listaCompromissos = mostraCompromissos(self.agenda.lista_de_compromisso)
                    filtro =filtroData(self.agendas,self.agenda,listaCompromissos,self.layout,self.janela)
                    self.janela.close()
                    filtro.mes(notificar)
                    break

        if periodo == 'Dia':
            simple.theme('Reddit')
            self.layout = [
                [simple.Text(f'{self.txtCompromisso}')],
                [simple.Button('Alterar titulo')],
                [simple.Button('Alterar data')],
                [simple.Button('Alterar hora')],
                [simple.Button('Alterar descricao')],
                [simple.Button('Voltar')]
            ]

            self.janela = simple.Window('Alterar compromisso',self.layout)

            while True:
                eventos, valores = self.janela.read()
                if eventos == simple.WINDOW_CLOSED:
                    descarregaDados(self.agendas)
                    break

                if eventos == 'Alterar titulo':
                    alterar = alteraTitulo(self.agendas,self.agenda,self.compromisso,self.txtCompromisso,self.layout,self.janela)
                    self.janela.close()
                    alterar.titulo('Dia',dia,metodo,'Titulo')
                    break
                
                if eventos == 'Alterar data':
                    alterar = alteraData(self.agendas,self.agenda,self.compromisso,self.txtCompromisso,self.layout,self.janela)
                    self.janela.close()
                    alterar.data('Dia',dia,metodo,'Data')
                    break

                if eventos == 'Alterar hora':
                    alterar = alteraHora(self.agendas,self.agenda,self.compromisso,self.txtCompromisso,self.layout,self.janela)
                    self.janela.close()
                    alterar.hora('Dia',dia,metodo,'Hora')
                    break

                if eventos == 'Alterar descricao':
                    alterar = alteraDescricao(self.agendas,self.agenda,self.compromisso,self.txtCompromisso,self.layout,self.janela)
                    self.janela.close()
                    alterar.descricao('Dia',dia,metodo,'Descricao')
                    break
            
                if eventos == 'Voltar':
                    listaCompromissos = mostraCompromissos(self.agenda.lista_de_compromisso)
                    filtro = filtroData(self.agendas,self.agenda,listaCompromissos,self.layout,self.janela)
                    self.janela.close()
                    filtro.dia(dia,metodo,notificar)
                    break

class alteraTitulo:

    def __init__(self,agendas,agenda,compromisso,txtCompromisso,layout,janela):
        self.compromisso = compromisso
        self.txtCompromisso = txtCompromisso
        self.layout = layout
        self.janela = janela
        self.agenda = agenda
        self.agendas = agendas

    def titulo(self,periodo,dia,metodo,classe):
        if periodo == 'Ano':
            simple.theme('Reddit')
            self.layout = [
                [simple.Text(f'{self.txtCompromisso}')],
                [simple.Text('Novo titulo'),simple.Input(key='Novo titulo',size=(20,1))],
                [simple.Button('Alterar'),simple.Button('Voltar')]
            ]

            self.janela = simple.Window('Alterar titulo',self.layout)
            while True:
                eventos, valores = self.janela.read()
                analise = 0

                if eventos == simple.WINDOW_CLOSED:
                    descarregaDados(self.agendas)
                    break
                if valores['Novo titulo'] == '':
                    analise = -1

                if eventos == 'Alterar' and analise == 0:
                    self.compromisso.alteraTitulo(valores['Novo titulo'])
                    self.txtCompromisso = TxtCompromisso(self.compromisso)
                    alterar = altera(self.agendas,self.agenda,self.compromisso,self.txtCompromisso,self.layout,self.janela)
                    self.janela.close()
                    alterar.alteraComp('Ano',dia,metodo,notificar=1)
                    break

                if eventos == 'Voltar':
                    alterar = altera(self.agendas,self.agenda,self.compromisso,self.txtCompromisso,self.layout,self.janela)
                    self.janela.close()
                    alterar.alteraComp('Ano', dia, metodo,notificar=1)
                    break

                if analise == -1:
                    self.listaCompromissos = mostraCompromissos(self.agenda.lista_de_compromisso)
                    error = TelaError(self.agendas,self.agenda,self.listaCompromissos,self.layout,self.janela)
                    self.janela.close()
                    error.errorPreencher(periodo,dia,metodo,classe,self.compromisso,notificar=1)
                    break

        if periodo == 'Mes':
            simple.theme('Reddit')
            self.layout = [
                [simple.Text(f'{self.txtCompromisso}')],
                [simple.Text('Novo titulo'),simple.Input(key='Novo titulo',size=(20,1))],
                [simple.Button('Alterar'),simple.Button('Voltar')]
            ]

            self.janela = simple.Window('Alterar titulo',self.layout)
            while True:
                eventos, valores = self.janela.read()
                if eventos == simple.WINDOW_CLOSED:
                    descarregaDados(self.agendas)
                    break

                analise = 0

                if valores['Novo titulo'] == '':
                    analise = -1

                if eventos == 'Alterar' and analise == 0:
                    self.compromisso.alteraTitulo(valores['Novo titulo'])
                    self.txtCompromisso = TxtCompromisso(self.compromisso)
                    alterar = altera(self.agendas,self.agenda,self.compromisso,self.txtCompromisso,self.layout,self.janela)
                    self.janela.close()
                    alterar.alteraComp('Mes',dia,metodo,notificar=1)
                    break

                if eventos == 'Voltar':
                    alterar = altera(self.agendas,self.agenda,self.compromisso,self.txtCompromisso,self.layout,self.janela)
                    self.janela.close()
                    alterar.alteraComp('Mes', dia, metodo,notificar=1)
                    break

                if analise == -1:
                    self.listaCompromissos = mostraCompromissos(self.agenda.lista_de_compromisso)
                    error = TelaError(self.agendas,self.agenda,self.listaCompromissos,self.layout,self.janela)
                    self.janela.close()
                    error.errorPreencher(periodo,dia,metodo,classe,self.compromisso,notificar=1)
                    break

        if periodo == 'Dia':
            simple.theme('Reddit')
            self.layout = [
                [simple.Text(f'{self.txtCompromisso}')],
                [simple.Text('Novo titulo'),simple.Input(key='Novo titulo',size=(20,1))],
                [simple.Button('Alterar'),simple.Button('Voltar')]
            ]

            self.janela = simple.Window('Alterar titulo',self.layout)
            while True:
                eventos, valores = self.janela.read()
                if eventos == simple.WINDOW_CLOSED:
                    descarregaDados(self.agendas)
                    break
                analise = 0
                if valores['Novo titulo'] == '':
                    analise = -1

                if eventos == 'Alterar' and analise == 0:
                    self.compromisso.alteraTitulo(valores['Novo titulo'])
                    self.txtCompromisso = TxtCompromisso(self.compromisso)
                    alterar = altera(self.agendas,self.agenda,self.compromisso,self.txtCompromisso,self.layout,self.janela)
                    self.janela.close()
                    alterar.alteraComp('Dia',dia,metodo,notificar=1)
                    break
                if eventos == 'Voltar':
                    alterar = altera(self.agendas,self.agenda,self.compromisso,self.txtCompromisso,self.layout,self.janela)
                    self.janela.close()
                    alterar.alteraComp('Dia', dia, metodo,notificar=1)
                    break

                if analise == -1:
                    self.listaCompromissos = mostraCompromissos(self.agenda.lista_de_compromisso)
                    error = TelaError(self.agendas,self.agenda,self.listaCompromissos,self.layout,self.janela)
                    self.janela.close()
                    error.errorPreencher(periodo,dia,metodo,classe,self.compromisso,notificar=1)
                    break

class alteraData:
    
    def __init__(self,agendas,agenda,compromisso,txtCompromisso,layout,janela):
        self.compromisso = compromisso
        self.txtCompromisso = txtCompromisso
        self.layout = layout
        self.janela = janela
        self.agenda = agenda
        self.agendas = agendas

    def data(self,periodo,dia,metodo,classe):
        if periodo == 'Ano':
            simple.theme('Reddit')
            self.layout = [
                [simple.Text(f'{self.txtCompromisso}')],
                [simple.Text('Nova data'),simple.Input(key='Nova data',size=(20,1))],
                [simple.Button('Alterar'),simple.Button('Voltar')]
            ]

            self.janela = simple.Window('Alterar data',self.layout)
            while True:
                eventos, valores = self.janela.read()
                if eventos == simple.WINDOW_CLOSED:
                    descarregaDados(self.agendas)
                    break
                analise = 0

                if valores['Nova data'] == '':
                    analise = -1

                if eventos == 'Alterar' and analise == 0:
                    self.compromisso.alteraData(valores['Nova data'])
                    self.txtCompromisso = TxtCompromisso(self.compromisso)
                    alterar = altera(self.agendas,self.agenda,self.compromisso,self.txtCompromisso,self.layout,self.janela)
                    self.janela.close()
                    alterar.alteraComp('Ano',dia,metodo,notificar=1)
                    break

                if eventos == 'Voltar':
                    alterar = altera(self.agendas,self.agenda,self.compromisso,self.txtCompromisso,self.layout,self.janela)
                    self.janela.close()
                    alterar.alteraComp('Ano', dia, metodo,notificar=1)
                    break

                if analise == -1:
                    self.listaCompromissos = mostraCompromissos(self.agenda.lista_de_compromisso)
                    error = TelaError(self.agendas,self.agenda,self.listaCompromissos,self.layout,self.janela)
                    self.janela.close()
                    error.errorPreencher(periodo,dia,metodo,classe,self.compromisso,notificar=1)
                    break
        
        if periodo == 'Mes':
            simple.theme('Reddit')
            self.layout = [
                [simple.Text(f'{self.txtCompromisso}')],
                [simple.Text('Nova data'),simple.Input(key='Nova data',size=(20,1))],
                [simple.Button('Alterar'),simple.Button('Voltar')]
            ]

            self.janela = simple.Window('Alterar data',self.layout)
            while True:
                eventos, valores = self.janela.read()
                if eventos == simple.WINDOW_CLOSED:
                    descarregaDados(self.agendas)
                    break
                analise = 0
                if valores['Nova data'] == '':
                    analise = -1

                if eventos == 'Alterar' and analise == 0:
                    self.compromisso.alteraData(valores['Nova data'])
                    self.txtCompromisso = TxtCompromisso(self.compromisso)
                    alterar = altera(self.agendas,self.agenda,self.compromisso,self.txtCompromisso,self.layout,self.janela)
                    self.janela.close()
                    alterar.alteraComp('Mes',dia,metodo,notificar=1)
                    break

                if eventos == 'Voltar':
                    alterar = altera(self.agendas,self.agenda,self.compromisso,self.txtCompromisso,self.layout,self.janela)
                    self.janela.close()
                    alterar.alteraComp('Mes', dia, metodo,notificar=1)
                    break

                if analise == -1:
                    self.listaCompromissos = mostraCompromissos(self.agenda.lista_de_compromisso)
                    error = TelaError(self.agendas,self.agenda,self.listaCompromissos,self.layout,self.janela)
                    self.janela.close()
                    error.errorPreencher(periodo,dia,metodo,classe,self.compromisso,notificar=1)
                    break
        
        if periodo == 'Dia':
            simple.theme('Reddit')
            self.layout = [
                [simple.Text(f'{self.txtCompromisso}')],
                [simple.Text('Nova data'),simple.Input(key='Nova data',size=(20,1))],
                [simple.Button('Alterar'),simple.Button('Voltar')]
            ]

            self.janela = simple.Window('Alterar data',self.layout)
            while True:
                eventos, valores = self.janela.read()
                if eventos == simple.WINDOW_CLOSED:
                    descarregaDados(self.agendas)
                    break

                analise = 0

                if valores['Nova data'] == '':
                    analise = -1

                if eventos == 'Alterar' and analise == 0:
                    self.compromisso.alteraData(valores['Nova data'])
                    self.txtCompromisso = TxtCompromisso(self.compromisso)
                    alterar = altera(self.agendas,self.agenda,self.compromisso,self.txtCompromisso,self.layout,self.janela)
                    self.janela.close()
                    alterar.alteraComp('Dia',dia,metodo,notificar=1)
                    break

                if eventos == 'Voltar':
                    alterar = altera(self.agendas, self.agenda, self.compromisso, self.txtCompromisso, self.layout,self.janela)
                    self.janela.close()
                    alterar.alteraComp('Dia', dia, metodo,notificar=1)
                    break

                if analise == -1:
                    self.listaCompromissos = mostraCompromissos(self.agenda.lista_de_compromisso)
                    error = TelaError(self.agendas,self.agenda,self.listaCompromissos,self.layout,self.janela)
                    self.janela.close()
                    error.errorPreencher(periodo,dia,metodo,classe,self.compromisso,notificar=1)
                    break
class alteraHora:
    
    def __init__(self,agendas,agenda,compromisso,txtCompromisso,layout,janela):
        self.compromisso = compromisso
        self.txtCompromisso = txtCompromisso
        self.layout = layout
        self.janela = janela
        self.agenda = agenda
        self.agendas = agendas

    def hora(self,periodo,dia,metodo,classe):
        if periodo == 'Ano':
            simple.theme('Reddit')
            self.layout = [
                [simple.Text(f'{self.txtCompromisso}')],
                [simple.Text('Novo horário'),simple.Input(key='Novo horário',size=(20,1))],
                [simple.Button('Alterar'),simple.Button('Voltar')]
            ]

            self.janela = simple.Window('Alterar horário',self.layout)
            while True:
                eventos, valores = self.janela.read()
                if eventos == simple.WINDOW_CLOSED:
                    descarregaDados(self.agendas)
                    break
                analise = 0

                if valores['Novo horário'] == '':
                    analise = -1

                if eventos == 'Alterar' and analise == 0:
                    self.compromisso.alteraHora(valores['Novo horário'])
                    self.txtCompromisso = TxtCompromisso(self.compromisso)
                    alterar = altera(self.agendas,self.agenda,self.compromisso,self.txtCompromisso,self.layout,self.janela)
                    self.janela.close()
                    alterar.alteraComp('Ano',dia,metodo,notificar=1)
                    break

                if eventos == 'Voltar':
                    alterar = altera(self.agendas,self.agenda,self.compromisso,self.txtCompromisso,self.layout,self.janela)
                    self.janela.close()
                    alterar.alteraComp('Ano', dia, metodo,notificar=1)
                    break

                if analise == -1:
                    self.listaCompromissos = mostraCompromissos(self.agenda.lista_de_compromisso)
                    error = TelaError(self.agendas,self.agenda,self.listaCompromissos,self.layout,self.janela)
                    self.janela.close()
                    error.errorPreencher(periodo,dia,metodo,classe,self.compromisso,notificar=1)
                    break

        if periodo == 'Mes':
            simple.theme('Reddit')
            self.layout = [
                [simple.Text(f'{self.txtCompromisso}')],
                [simple.Text('Novo horário'),simple.Input(key='Novo horário',size=(20,1))],
                [simple.Button('Alterar'),simple.Button('Voltar')]
            ]

            self.janela = simple.Window('Alterar horário',self.layout)
            while True:
                eventos, valores = self.janela.read()
                if eventos == simple.WINDOW_CLOSED:
                    descarregaDados(self.agendas)
                    break

                analise = 0

                if valores['Novo horário'] == '':
                    analise = -1

                if eventos == 'Alterar' and analise == 0:
                    self.compromisso.alteraHora(valores['Novo horário'])
                    self.txtCompromisso = TxtCompromisso(self.compromisso)
                    alterar = altera(self.agendas,self.agenda,self.compromisso,self.txtCompromisso,self.layout,self.janela)
                    self.janela.close()
                    alterar.alteraComp('Mes',dia,metodo,notificar=1)
                    break

                if eventos == 'Voltar':
                    alterar = altera(self.agendas,self.agenda,self.compromisso,self.txtCompromisso,self.layout,self.janela)
                    self.janela.close()
                    alterar.alteraComp('Mes', dia, metodo,notificar=1)
                    break

                if analise == -1:
                    self.listaCompromissos = mostraCompromissos(self.agenda.lista_de_compromisso)
                    error = TelaError(self.agendas,self.agenda,self.listaCompromissos,self.layout,self.janela)
                    self.janela.close()
                    error.errorPreencher(periodo,dia,metodo,classe,self.compromisso,notificar=1)
                    break
        
        if periodo == 'Dia':
            simple.theme('Reddit')
            self.layout = [
                [simple.Text(f'{self.txtCompromisso}')],
                [simple.Text('Novo horário'),simple.Input(key='Novo horário',size=(20,1))],
                [simple.Button('Alterar'),simple.Button('Voltar')]
            ]

            self.janela = simple.Window('Alterar horário',self.layout)
            while True:
                eventos, valores = self.janela.read()
                if eventos == simple.WINDOW_CLOSED:
                    descarregaDados(self.agendas)
                    break

                analise = 0

                if valores['Novo horário'] == '':
                    analise = -1

                if eventos == 'Alterar' and analise == 0:
                    self.compromisso.alteraHora(valores['Novo horário'])
                    self.txtCompromisso = TxtCompromisso(self.compromisso)
                    alterar = altera(self.agendas,self.agenda,self.compromisso,self.txtCompromisso,self.layout,self.janela)
                    self.janela.close()
                    alterar.alteraComp('Dia',dia,metodo,notificar=1)
                    break

                if eventos == 'Voltar':
                    alterar = altera(self.agendas,self.agenda,self.compromisso,self.txtCompromisso,self.layout,self.janela)
                    self.janela.close()
                    alterar.alteraComp('Dia', dia, metodo,notificar=1)
                    break

                if analise == -1:
                    self.listaCompromissos = mostraCompromissos(self.agenda.lista_de_compromisso)
                    error = TelaError(self.agendas,self.agenda,self.listaCompromissos,self.layout,self.janela)
                    self.janela.close()
                    error.errorPreencher(periodo,dia,metodo,classe,self.compromisso,notificar=1)
                    break

class alteraDescricao:
    
    def __init__(self,agendas,agenda,compromisso,txtCompromisso,layout,janela):
        self.compromisso = compromisso
        self.txtCompromisso = txtCompromisso
        self.layout = layout
        self.janela = janela
        self.agenda = agenda
        self.agendas = agendas

    def descricao(self,periodo,dia,metodo,classe):
        if periodo == 'Ano':
            simple.theme('Reddit')
            self.layout = [
                [simple.Text(f'{self.txtCompromisso}')],
                [simple.Text('Nova descrição'),simple.Input(key='Nova descrição',size=(20,1))],
                [simple.Button('Alterar'),simple.Button('Voltar')]
            ]

            self.janela = simple.Window('Alterar descrição',self.layout)
            while True:
                eventos, valores = self.janela.read()
                if eventos == simple.WINDOW_CLOSED:
                    descarregaDados(self.agendas)
                    break

                analise = 0

                if valores['Nova descrição'] == '':
                    analise = -1

                if eventos == 'Alterar' and analise == 0:
                    self.compromisso.alteraDescricao(valores['Nova descrição'])
                    self.txtCompromisso = TxtCompromisso(self.compromisso)
                    alterar = altera(self.agendas,self.agenda,self.compromisso,self.txtCompromisso,self.layout,self.janela)
                    self.janela.close()
                    alterar.alteraComp('Ano',dia,metodo,notificar=1)
                    break

                if eventos == 'Voltar':
                    alterar = altera(self.agendas,self.agenda,self.compromisso,self.txtCompromisso,self.layout,self.janela)
                    self.janela.close()
                    alterar.alteraComp('Ano', dia, metodo,notificar=1)
                    break

                if analise == -1:
                    self.listaCompromissos = mostraCompromissos(self.agenda.lista_de_compromisso)
                    error = TelaError(self.agendas,self.agenda,self.listaCompromissos,self.layout,self.janela)
                    self.janela.close()
                    error.errorPreencher(periodo,dia,metodo,classe,self.compromisso,notificar=1)
                    break

        if periodo == 'Mes':
            simple.theme('Reddit')
            self.layout = [
                [simple.Text(f'{self.txtCompromisso}')],
                [simple.Text('Nova descrição'),simple.Input(key='Nova descrição',size=(20,1))],
                [simple.Button('Alterar'),simple.Button('Voltar')]
            ]

            self.janela = simple.Window('Alterar descrição',self.layout)
            while True:
                eventos, valores = self.janela.read()
                if eventos == simple.WINDOW_CLOSED:
                    descarregaDados(self.agendas)
                    break

                analise = 0

                if valores['Nova descrição'] == '':
                    analise = -1

                if eventos == 'Alterar' and analise == 0:
                    self.compromisso.alteraDescricao(valores['Nova descrição'])
                    self.txtCompromisso = TxtCompromisso(self.compromisso)
                    alterar = altera(self.agendas,self.agenda,self.compromisso,self.txtCompromisso,self.layout,self.janela)
                    self.janela.close()
                    alterar.alteraComp('Mes',dia,metodo,notificar=1)
                    break

                if eventos == 'Voltar':
                    alterar = altera(self.agendas,self.agenda,self.compromisso,self.txtCompromisso,self.layout,self.janela)
                    self.janela.close()
                    alterar.alteraComp('Mes', dia, metodo,notificar=1)
                    break

                if analise == -1:
                    self.listaCompromissos = mostraCompromissos(self.agenda.lista_de_compromisso)
                    error = TelaError(self.agendas,self.agenda,self.listaCompromissos,self.layout,self.janela)
                    self.janela.close()
                    error.errorPreencher(periodo,dia,metodo,classe,self.compromisso,notificar=1)
                    break

        if periodo == 'Dia':
            simple.theme('Reddit')
            self.layout = [
                [simple.Text(f'{self.txtCompromisso}')],
                [simple.Text('Nova descrição'),simple.Input(key='Nova descrição',size=(20,1))],
                [simple.Button('Alterar'),simple.Button('Voltar')]
            ]

            self.janela = simple.Window('Alterar descrição',self.layout)
            while True:
                eventos, valores = self.janela.read()
                if eventos == simple.WINDOW_CLOSED:
                    descarregaDados(self.agendas)
                    break

                analise = 0

                if valores['Nova descrição'] == '':
                    analise = -1

                if eventos == 'Alterar' and analise == 0:
                    self.compromisso.alteraDescricao(valores['Nova descrição'])
                    self.txtCompromisso = TxtCompromisso(self.compromisso)
                    alterar = altera(self.agendas,self.agenda,self.compromisso,self.txtCompromisso,self.layout,self.janela)
                    self.janela.close()
                    alterar.alteraComp('Dia',dia,metodo,notificar=1)
                    break

                if eventos == 'Voltar':
                    alterar = altera(self.agendas,self.agenda,self.compromisso,self.txtCompromisso,self.layout,self.janela)
                    self.janela.close()
                    alterar.alteraComp('Dia', dia, metodo,notificar=1)
                    break

                if analise == -1:
                    self.listaCompromissos = mostraCompromissos(self.agenda.lista_de_compromisso)
                    error = TelaError(self.agendas,self.agenda,self.listaCompromissos,self.layout,self.janela)
                    self.janela.close()
                    error.errorPreencher(periodo,dia,metodo,classe,self.compromisso,notificar=1)
                    break

def criaAgenda(agendas,login,senha,email,notificacao): 
    agenda = Agenda(login,senha,email,notificacao)

    arquivo = open("Banco de Dados.txt","a")
    lines = list()
    if len(agendas) == 0:
        lines.append(agenda.login + '\n')
        lines.append(agenda.senha + '\n')
        lines.append(agenda.email + '\n')
        lines.append(agenda.notificacao)
    else:
        lines.append('\n')
        lines.append('\n')
        lines.append(agenda.login + '\n')
        lines.append(agenda.senha + '\n')
        lines.append(agenda.email + '\n')
        lines.append(agenda.notificacao)
    arquivo.writelines(lines)
    
    return agenda

def CriaCompromisso(titulo,data,hora,descricao):
    compromisso = Compromisso(titulo,data,hora,descricao)
    return compromisso

def allocaCompromisso(Agenda,Compromisso):
    Agenda.insereCompromisso(Compromisso)

def mostraCompromissos(lista):
    txtCompromissos = ''
    for compromisso in lista:
        txtCompromissos = txtCompromissos + f'---------{compromisso.titulo}---------' + '\n'
        txtCompromissos = txtCompromissos + f'Data:{compromisso.data}' + '\n'
        txtCompromissos = txtCompromissos + f'hora:{compromisso.hora}' + '\n'
        txtCompromissos = txtCompromissos + f'Descricao:{compromisso.descricao}'
        txtCompromissos = txtCompromissos + '\n' + '\n'
    return txtCompromissos

def bancoDeDados ():
    arquivo = open("Banco de Dados.txt","r")
    lines = arquivo.readlines()
    h = 0
    position = 0
    agendas = list()
    for i in range(0,len(lines),1):
        if h == 0:
            login = lines[position].replace('\n',"")
            senha = lines[position+1].replace('\n',"")
            email = lines[position+2].replace('\n',"")
            notificacao = lines[position+3].replace('\n',"")
            agenda = Agenda(login,senha,email,notificacao)
            agendas.append(agenda)
            h = position + 4
            position = position + 4
        else:
            for n in range(h,len(lines),4):
                if lines[n] != '\n':
                    titulo = lines[n].replace('\n',"")
                    data = lines[n+1].replace('\n',"")
                    hora = lines[n+2].replace('\n',"")
                    descricao = lines[n+3].replace('\n',"")
                    compromisso = Compromisso(titulo,data,hora,descricao)
                    allocaCompromisso(agenda,compromisso)
                    position = position + 4
                else:
                    break

            if position == len(lines):
                break 
            h = 0
            position = position + 1
        
    return agendas

def descarregaDados(agendas):
    arquivo = open("Banco de Dados.txt","w")
    lines = list()
    i = 0
    j = 0
    for agenda in agendas:
        if i > 0:
            lines.append('\n')
            lines.append('\n')
            j = 0
        lines.append(agenda.login + '\n')
        lines.append(agenda.senha + '\n')
        lines.append(agenda.email + '\n')
        if len(agenda.lista_de_compromisso) == 0:
            lines.append(agenda.notificacao)
        else:
            lines.append(agenda.notificacao + '\n')

        for compromissos in agenda.lista_de_compromisso:
            if j > 0:
                lines.append('\n')
            lines.append(compromissos.titulo + '\n')
            lines.append(compromissos.data  + '\n')
            lines.append(compromissos.hora + '\n')
            lines.append(compromissos.descricao)
            j = j + 1
        i = i + 1
    
    arquivo.writelines(lines)

def verificaLogin(agendas,login,senha):
    for agenda in agendas:
        if login == agenda.login and senha == agenda.senha:
            return agenda
    return -1

def main():
    
    agendas = bancoDeDados()

    cadastro = Cadastro(agendas,'','')

    cadastro.Login()

def encontraCompromisso(agenda,titulo):
    for compromisso in agenda.lista_de_compromisso:
        if compromisso.titulo == titulo:
            txtCompromisso = TxtCompromisso(compromisso)
            return compromisso,txtCompromisso
    return -1,-1

def TxtCompromisso(compromisso):
    txtCompromisso = '\n'
    txtCompromisso = txtCompromisso + f'---------{compromisso.titulo}---------' + '\n'
    txtCompromisso = txtCompromisso + f'Data:{compromisso.data}' + '\n'
    txtCompromisso = txtCompromisso + f'hora:{compromisso.hora}' + '\n'
    txtCompromisso = txtCompromisso + f'Descricao:{compromisso.descricao}'
    txtCompromisso = txtCompromisso + '\n' + '\n'
    return txtCompromisso

def deletaCompromisso(agenda,titulo):
    i = 0
    for compromisso in agenda.lista_de_compromisso:
        if compromisso.titulo == titulo:
            del(agenda.lista_de_compromisso[i])
            return agenda
        i = i + 1
    return -1

def listaLogins(agendas):
    lista = list()
    for agenda in agendas:
        lista.append(agenda.login)
    return lista

def listaTxt(Lista):
    lista = list()
    for compromisso in Lista:
        for i in range(0,4,1):
            if i == 0:
                txt = f'---------{compromisso.titulo}---------'
                lista.append(txt)
            if i == 1:
                txt = f'Data: {compromisso.data}'
                lista.append(txt)
            if i == 2:
                txt = f'Hora: {compromisso.hora}'
                lista.append(txt)
            if i == 3:
                descricao,valor = compromisso.analisaDescricao()
                if valor == -1:
                    descricao_out = ''
                    flag = 0
                    j = 0
                    i = 0
                    for value in descricao:
                        descricao_out = descricao_out + value
                        if value == '\n' and flag ==0:
                            if i == 0:
                                txt = f'Descrição: {descricao_out}'
                                lista.append(txt)
                                descricao_out = ''
                                i = 1
                            else:
                                txt = descricao_out
                                lista.append(txt)
                                descricao_out = ''
                            flag = 1
                        
                        if '\n' in descricao[j+1:]:
                            flag = 0
                        
                        else:
                            lista.append(descricao[j+1:])
                            break

                        j = j +1
                        
                if valor == 0:
                    txt = f'Descrição: {descricao}'
                    lista.append(txt)

        lista.append(' ')
    return lista

def retornaNome(mes):
    meses = ['Janeiro','Fevereiro','Março','Abril','Maio','Junho','Julho','Agosto',
    'Setembro','Outubro','Novembro','Dezembro']
    return meses[mes]

def diasSemana():
    data = datetime.now()
    diaSemana = data.weekday()
    dia = data.day

    dias = list()

    if diaSemana == 0:
        dias.append(dia)
        dias.append(dia+1)
        dias.append(dia+2)
        dias.append(dia+3)
        dias.append(dia+4)
        dias.append(dia+5)
        dias.append(dia+6)
    
    if diaSemana == 1:
        dias.append(dia - 1)
        dias.append(dia)
        dias.append(dia+1)
        dias.append(dia+2)
        dias.append(dia+3)
        dias.append(dia+4)
        dias.append(dia+5)

    if diaSemana == 2:
        dias.append(dia - 2)
        dias.append(dia - 1)
        dias.append(dia)
        dias.append(dia+1)
        dias.append(dia+2)
        dias.append(dia+3)
        dias.append(dia+4)
    
    if diaSemana == 3:
        dias.append(dia - 3)
        dias.append(dia - 2)
        dias.append(dia - 1)
        dias.append(dia)
        dias.append(dia+1)
        dias.append(dia+2)
        dias.append(dia+3)

    if diaSemana == 4:
        dias.append(dia - 4)
        dias.append(dia - 3)
        dias.append(dia - 2)
        dias.append(dia - 1)
        dias.append(dia)
        dias.append(dia+1)
        dias.append(dia+2)
    
    if diaSemana == 5:
        dias.append(dia - 5)
        dias.append(dia - 4)
        dias.append(dia - 3)
        dias.append(dia - 2)
        dias.append(dia - 1)
        dias.append(dia)
        dias.append(dia+1)
    
    if diaSemana == 6:
        dias.append(dia - 6)
        dias.append(dia - 5)
        dias.append(dia - 4)
        dias.append(dia - 3)
        dias.append(dia - 2)
        dias.append(dia - 1)
        dias.append(dia)

    return dias

def mostraCompromissosEmail(lista):
    txtCompromissos = ''
    txtCompromissos = txtCompromissos + '<p>///////Comrpomissos para hoje/////////</p>'
    for compromisso in lista:
        txtCompromissos = txtCompromissos + f'<p> ---------{compromisso.titulo}---------'
        txtCompromissos = txtCompromissos + f'<p>Data:{compromisso.data}</p>'
        txtCompromissos = txtCompromissos + f'<p>hora:{compromisso.hora}</p>'
        txtCompromissos = txtCompromissos + f'<p>Descricao:{compromisso.descricao}</p>'
        txtCompromissos = txtCompromissos + '<p></p>'
    return txtCompromissos


def diasParaRepetir(modo,DataStart,Dataend):
    data = datetime.now()
    ano = data.year


    diaStart = DataStart[0:2]
    diaStart = int(diaStart)
    mesStart = DataStart[3:5]
    mesStart = int(mesStart)

    diaFinal = Dataend[0:2]
    diaFinal = int(diaFinal)
    mesFinal = Dataend[3:5]
    mesFinal = int(mesFinal)

    datesContainer = []

    aux_data = date(ano, mesStart, diaStart)
    dia_semana = aux_data.weekday()

    if modo == 'Semanalmente':
        mesEntrada = mesStart
        diaEntrada = diaStart

        for i in range(0,mesFinal-mesStart + 1,1):

            if (i + 1) >= (mesFinal - mesStart + 1):

                last_date_of_month = diaFinal

            else: 
                last_date_of_month = calendar.monthrange(ano,mesEntrada)[1]

            listaDias = retornaDias(modo,ano,mesEntrada,diaEntrada,dia_semana,last_date_of_month)
            
            datesContainer.append(listaDias)

            diaEntrada = 1
            mesEntrada = mesEntrada + 1
        
        return datesContainer
    
    if modo == 'Todos os dias':
        mesEntrada = mesStart
        diaEntrada = diaStart

        for i in range(0,mesFinal-mesStart + 1,1):
    
            if (i + 1) >= (mesFinal - mesStart + 1):

                last_date_of_month = diaFinal

            else:

                last_date_of_month = calendar.monthrange(ano,mesEntrada)[1]

            listaDias = retornaDias(modo,ano,mesEntrada,diaEntrada,dia_semana,last_date_of_month)
            
            datesContainer.append(listaDias)

            diaEntrada = 1
            mesEntrada = mesEntrada + 1
        

        return datesContainer

def retornaDias(modo,ano,mes,diaEntrada,dayWeek,last_date_of_month):
    if modo == 'Semanalmente':
        listaDias = list()

        for j in range(diaEntrada,last_date_of_month + 1,1):
            data = date(ano, mes, j)
            indice_da_semana = data.weekday()
            if indice_da_semana == dayWeek:
                listaDias.append(j)
        return listaDias

    if modo == 'Todos os dias':
        listaDias = list()

        for j in range(diaEntrada,last_date_of_month + 1,1):
            listaDias.append(j)
        return listaDias

def repeteCompromisso(agenda,compromisso,dataStart,dataEnd,modo):
    lista_dias_meses = diasParaRepetir(modo,dataStart,dataEnd)
    mes = int(dataStart[3:5])
    data = compromisso.data
    titulo = compromisso.titulo
    hora = compromisso.hora
    descricao = compromisso.descricao
    for i in range(len(lista_dias_meses)):
        lista_aux = lista_dias_meses[i]
        for dia in lista_aux:
            compromisso_aux = Compromisso(titulo,data,hora,descricao)
            compromisso_aux.alteraDia(dia)
            compromisso_aux.alteraMes(mes)
            allocaCompromisso(agenda,compromisso_aux)
        mes = mes + 1

def excluiRepetidos(agenda,titulo):
    seguro = 0
    for compromisso in agenda.lista_de_compromisso:
        if compromisso.titulo == titulo:
            seguro = 1
        
    for i in range(len(agenda.lista_de_compromisso)):
        j = deletaCompromisso(agenda,titulo)
    
    if seguro == 1 and j == -1:
        j = 0
        
    return j

def compromissosProximaSemana(agenda):
    dias = ['Segunda','Terça','Quarta','Quinta','Sexta','Sábado','Domingo']
    diaSemana,listaDias = diasProximaSemana()
    txtProximaSemana = ''
    for i in range(7):
        txtCompromissos = ''
        lista = agenda.filtroDiaSemana(listaDias[i])
        if len(lista) > 0:
            txtCompromissos = txtCompromissos + f'<p>//////////{dias[i]}///////////</p>'
            for compromisso in lista:
                txtCompromissos = txtCompromissos + f'<p> ---------{compromisso.titulo}---------'
                txtCompromissos = txtCompromissos + f'<p>Data:{compromisso.data}</p>'
                txtCompromissos = txtCompromissos + f'<p>hora:{compromisso.hora}</p>'
                txtCompromissos = txtCompromissos + f'<p>Descricao:{compromisso.descricao}</p>'
                txtCompromissos = txtCompromissos + '<p></p>'
            txtProximaSemana = txtProximaSemana + txtCompromissos
    return txtProximaSemana

def diasProximaSemana():
    data = datetime.now()
    diaSemana = data.weekday()
    dia = data.day + 7

    dias = list()

    if diaSemana == 0:
        dias.append(dia)
        dias.append(dia + 1)
        dias.append(dia + 2)
        dias.append(dia + 3)
        dias.append(dia + 4)
        dias.append(dia + 5)
        dias.append(dia + 6)

    if diaSemana == 1:
        dias.append(dia - 1)
        dias.append(dia)
        dias.append(dia + 1)
        dias.append(dia + 2)
        dias.append(dia + 3)
        dias.append(dia + 4)
        dias.append(dia + 5)

    if diaSemana == 2:
        dias.append(dia - 2)
        dias.append(dia - 1)
        dias.append(dia)
        dias.append(dia + 1)
        dias.append(dia + 2)
        dias.append(dia + 3)
        dias.append(dia + 4)

    if diaSemana == 3:
        dias.append(dia - 3)
        dias.append(dia - 2)
        dias.append(dia - 1)
        dias.append(dia)
        dias.append(dia + 1)
        dias.append(dia + 2)
        dias.append(dia + 3)

    if diaSemana == 4:
        dias.append(dia - 4)
        dias.append(dia - 3)
        dias.append(dia - 2)
        dias.append(dia - 1)
        dias.append(dia)
        dias.append(dia + 1)
        dias.append(dia + 2)

    if diaSemana == 5:
        dias.append(dia - 5)
        dias.append(dia - 4)
        dias.append(dia - 3)
        dias.append(dia - 2)
        dias.append(dia - 1)
        dias.append(dia)
        dias.append(dia + 1)

    if diaSemana == 6:
        dias.append(dia - 6)
        dias.append(dia - 5)
        dias.append(dia - 4)
        dias.append(dia - 3)
        dias.append(dia - 2)
        dias.append(dia - 1)
        dias.append(dia)

    return diaSemana,dias
