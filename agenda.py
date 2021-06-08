from datetime import datetime

class Agenda:
    def __init__(self,login,senha):
        self.lista_de_compromisso = []
        self.login = login
        self.senha = senha

    def obterLogin(self):
        return self.login
    
    def obterSenha(self):
        return self.senha

    def alteraLogin(self,login):
        self.login = login
    
    def alteraSenha(self,senha):
        self.senha = senha
    
    def insereCompromisso(self,compromisso):
        self.lista_de_compromisso.append(compromisso)

    def retornaCompromissos(self):
        return self.lista_de_compromisso
    
    def filtroAno(self):
        Ano = datetime.now()
        ano_print = Ano.strftime('%Y')
        lista = list()
        for compromisso in self.lista_de_compromisso:
            ano = compromisso.obterAno()
            if ano == ano_print:
                lista.append(compromisso)
        return lista
    
    def filtroMes(self):
        Ano = datetime.now()
        mes_print = Ano.strftime('%m')
        ano_print = Ano.strftime('%Y')
        lista = list()
        for compromisso in self.lista_de_compromisso:
            mes = compromisso.obterMes()
            ano = compromisso.obterAno()
            if mes == mes_print and ano == ano_print:
                lista.append(compromisso)
        return lista

    def filtroDia(self):
        Ano = datetime.now()
        dia_print = Ano.strftime('%d')
        mes_print = Ano.strftime('%m')
        ano_print = Ano.strftime('%Y')
        lista = list()
        for compromisso in self.lista_de_compromisso:
            mes = compromisso.obterMes()
            ano = compromisso.obterAno()
            dia = compromisso.obterDia()
            if mes == mes_print and ano == ano_print and int(dia) == int(dia_print):
                lista.append(compromisso)
        return lista

    def filtroDiaSemana(self,Dia):
        Ano = datetime.now()
        mes_print = Ano.strftime('%m')
        ano_print = Ano.strftime('%Y')
        lista = list()
        for compromisso in self.lista_de_compromisso:
            mes = compromisso.obterMes()
            ano = compromisso.obterAno()
            dia = compromisso.obterDia()
            if mes == mes_print and ano == ano_print and int(dia) == Dia:
                lista.append(compromisso)
        return lista
    
    def verificaExistencia(self,compromisso):
        for compromissos in self.lista_de_compromisso:
            if compromissos.titulo == compromisso.titulo:
                return -1
        return 0
    
    def verificaHorario(self,compromisso):
        for compromissos in self.lista_de_compromisso:
            if (compromissos.data == compromisso.data) and (compromissos.hora == compromisso.hora):
                return -1
        return 0