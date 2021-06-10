class Compromisso:
    def __init__(self,titulo,data,hora,descricao):
        self.data = data
        self.hora = hora
        self.descricao = descricao
        self.titulo = titulo
    
    def analisaDescricao(self):
        descricao = self.descricao
        if len(self.descricao) > 34:
            i = 0
            quebra_linha = 40
            for caractere in self.descricao:
                if i == quebra_linha and caractere ==' ':
                    descricao = descricao[:i+1] + '\n' + descricao[i+1:]
                    if len(self.descricao) > quebra_linha:
                        quebra_linha = quebra_linha + 40
                    else:
                        break

                if caractere != ' ' and i == quebra_linha:
                    quebra_linha = quebra_linha + 1

                i = i + 1
            return descricao,-1
        return descricao,0
        
    
    def obterData(self):
        return self.data

    def obterAno(self):
        ano = self.data[-4:]
        return ano
    
    def obterMes(self):
        mes = self.data[3:5]
        return mes
    
    def obterDia(self):
        dia = self.data[0:2]
        return dia
    
    def obterHora(self):
        return self.hora

    def obterTitulo(self):
        return self.titulo

    def obterDescricao(self):
        return self.descricao
    
    def alteraData(self,data):
        self.data = data
    
    def alteraHora(self,hora):
        self.hora = hora

    def alteraTitulo(self,titulo):
        self.titulo = titulo
    
    def alteraDescricao(self,descricao):
        self.descricao = descricao
    
    def alteraDia(self,Dia):
        mes = self.data[3:5]
        ano = self.data[-4:]

        if int(Dia) < 10:
            Dia = '0' + str(Dia)

        if int(Dia) >= 10:
            Dia = str(Dia)

        data_out = Dia + '/' + mes + '/' + ano
        self.data = data_out
    
    def alteraMes(self,Mes):
        dia = self.data[0:2]
        ano = self.data[-4:]

        if int(Mes) < 10:
            Mes = '0' + str(Mes)

        if int(Mes) >= 10:
            Mes = str(Mes)

        data_out = dia + '/' + Mes + '/' + ano
        self.data = data_out

