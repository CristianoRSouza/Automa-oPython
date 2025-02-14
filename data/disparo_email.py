import pandas as pd
import smtplib
import ssl
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText

SMTP_SERVER = "smtp.gmail.com"
SMTP_PORT = 587
EMAIL_SENDER = "nicktrollfly@gmail.com"
EMAIL_PASSWORD = "pdtm guyx rhrn phri " 

df = pd.read_csv("data/resultados.csv", dtype=str)

def enviar_email(destinatario, nome, endereco):
    msg = MIMEMultipart()
    msg["From"] = EMAIL_SENDER
    msg["To"] = destinatario
    msg["Subject"] = "Confirmação de Endereço - ViaCEP"

    corpo_email = f"""
    Olá {nome},

    Estamos entrando em contato para confirmar seu endereço cadastrado:

     Logradouro: {endereco["logradouro"]}
     Bairro: {endereco["bairro"]}
     Cidade: {endereco["cidade"]} - {endereco["estado"]}
     CEP: {endereco["cep"]}

    Caso haja algum erro, entre em contato para atualização.

    Atenciosamente,  
    Equipe de Cadastro
    """

    msg.attach(MIMEText(corpo_email, "plain"))

    try:
        context = ssl.create_default_context()
        server = smtplib.SMTP(SMTP_SERVER, SMTP_PORT)
        server.starttls(context=context)
        server.login(EMAIL_SENDER, EMAIL_PASSWORD)
        server.sendmail(EMAIL_SENDER, destinatario, msg.as_string())
        server.quit()
        print(f" E-mail enviado para {destinatario}")
    except Exception as e:
        print(f"Erro ao enviar e-mail para {destinatario}: {e}")

for index, row in df.iterrows():
    destinatario = "crisvideoaulas@gmail.com"  
    nome = "Usuário"  
    endereco = {
        "cep": row["cep"],
        "logradouro": row["logradouro"],
        "bairro": row["bairro"],
        "cidade": row["cidade"],
        "estado": row["estado"],
    }
    
    enviar_email(destinatario, nome, endereco)
