import os
import pandas as pd
import requests
import time
import smtplib
import ssl
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from fpdf import FPDF
from dotenv import load_dotenv

load_dotenv()

INPUT_CSV = "data/ceps_lista_30.csv"
OUTPUT_CSV = "data/resultados.csv"
SMTP_SERVER = "smtp.gmail.com"
SMTP_PORT = 587
EMAIL_SENDER = os.getenv("EMAIL_SENDER")
EMAIL_PASSWORD = os.getenv("EMAIL_PASSWORD")
DESTINATARIO_PADRAO = os.getenv("DESTINATARIO_PADRAO")


class PDF(FPDF):
    def header(self):
        self.set_font("Arial", "B", 12)
        self.cell(0, 10, "Relatório Consolidado", ln=True, align="C")
        self.ln(10)

    def footer(self):
        self.set_y(-15)
        self.set_font("Arial", "I", 8)
        self.cell(0, 10, f"Página {self.page_no()}", align="C")


def buscar_endereco(cep):

    url = f"https://viacep.com.br/ws/{cep}/json/"
    response = requests.get(url)

    if response.status_code == 200:
        data = response.json()
        if "erro" not in data:
            return {
                "cep": data["cep"],
                "logradouro": data["logradouro"],
                "bairro": data["bairro"],
                "cidade": data["localidade"],
                "estado": data["uf"]
            }
    return None


def processar_ceps():

    df = pd.read_csv(INPUT_CSV, dtype=str)
    resultados = []

    for cep in df["CEP"]:
        endereco = buscar_endereco(cep)
        if endereco:
            resultados.append(endereco)
        else:
            print(f"Erro ao buscar o CEP {cep}")
        time.sleep(1)  

    df_resultados = pd.DataFrame(resultados)
    df_resultados.to_csv(OUTPUT_CSV, index=False)
    print(f" Dados salvos em {OUTPUT_CSV}")


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
        with smtplib.SMTP(SMTP_SERVER, SMTP_PORT) as server:
            server.starttls(context=context)
            server.login(EMAIL_SENDER, EMAIL_PASSWORD)
            server.sendmail(EMAIL_SENDER, destinatario, msg.as_string())
        print(f" E-mail enviado para {destinatario}")
    except Exception as e:
        print(f" Erro ao enviar e-mail para {destinatario}: {e}")


def enviar_emails():

    df = pd.read_csv(OUTPUT_CSV, dtype=str)
    for _, row in df.iterrows():
        nome = "Cristiano"  
        endereco = {
            "cep": row["cep"],
            "logradouro": row["logradouro"],
            "bairro": row["bairro"],
            "cidade": row["cidade"],
            "estado": row["estado"],
        }
        enviar_email(DESTINATARIO_PADRAO, nome, endereco)


def gerar_relatorio():

    pdf = PDF()
    pdf.set_auto_page_break(auto=True, margin=15)
    pdf.add_page()
    pdf.set_font("Arial", size=10)

    df = pd.read_csv(OUTPUT_CSV, dtype=str)

    for _, row in df.iterrows():
        pdf.set_font("Arial", "B", 10)
        pdf.cell(0, 6, "Endereço", ln=True)
        pdf.set_font("Arial", size=10)
        conteudo = (
            f"CEP: {row['cep']}\n"
            f"Logradouro: {row['logradouro']}\n"
            f"Bairro: {row['bairro']}\n"
            f"Cidade: {row['cidade']} - {row['estado']}\n"
        )
        pdf.multi_cell(0, 6, conteudo)
        pdf.ln(5)

    pdf.output("relatorio.pdf")
    print(f" Relatório gerado com sucesso: relatorio.pdf")


def main():

    print(" Iniciando consulta de CEPs...")
    processar_ceps()

    print(" Iniciando envio de e-mails...")
    enviar_emails()

    print(" Gerando relatório PDF...")
    gerar_relatorio()

    print(" Processo concluído com sucesso!")


if __name__ == "__main__":
    main()
