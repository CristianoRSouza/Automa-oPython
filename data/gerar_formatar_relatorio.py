from fpdf import FPDF

def gerar_relatorio(dados: dict, nome_arquivo: str = "relatorio.pdf"):
    class PDF(FPDF):
        def header(self):
            self.set_font("Arial", "B", 12)
            self.cell(0, 10, "Relatorio Consolidado", ln=True, align="C")
            self.ln(10)

        def footer(self):
            self.set_y(-15)
            self.set_font("Arial", "I", 8)
            self.cell(0, 10, f"Pagina {self.page_no()}", align="C")

    pdf = PDF()
    pdf.set_auto_page_break(auto=True, margin=15)
    pdf.add_page()
    pdf.set_font("Arial", size=10)

    for titulo, conteudo in dados.items():
        pdf.set_font("Arial", "B", 10)
        pdf.cell(0, 6, titulo, ln=True)
        pdf.set_font("Arial", size=10)
        pdf.multi_cell(0, 6, conteudo)
        pdf.ln(5)

    pdf.output(nome_arquivo)
    print(f"Relatorio salvo como {nome_arquivo}")

dados_exemplo = {
    "Resumo": "Este é um relatório consolidado com informações coletadas.",
    "Dados 1": "Informação detalhada sobre o primeiro conjunto de dados.",
    "Dados 2": "Mais detalhes sobre o segundo conjunto de dados.",
}

gerar_relatorio(dados_exemplo)
