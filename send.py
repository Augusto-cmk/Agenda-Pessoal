import win32com.client as win32

def envioEmail(destino,assunto,mensagem):

    outlook = win32.Dispatch('outlook.application')

    email = outlook.CreateItem(0)

    email.To = destino

    email.Subject = assunto

    email.HTMLBody = f"""
        <p>Você possui os seguintes compromissos:</p>

        <p>{mensagem}</p>

        <p>Att,</p>
        <p>Sua agenda Pessoal.</p>
    """
    email.Send()