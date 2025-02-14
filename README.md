# Consultador de CEPs com ViaCEP
==========================

Um sistema automatizado para consultar endereços através da API ViaCEP, processar dados em CSV e gerar relatórios em PDF com confirmação por e-mail.

## Funcionalidades Principais
---------------------------

- Consulta automática de endereços através da API ViaCEP
- Processamento de lista de CEPs em formato CSV
- Geração de relatórios em PDF
- Envio automático de confirmações por e-mail
- Tratamento de erros e logs

## Requisitos
-------------

### Bibliotecas Necessárias

* `requests`: Para requisições à API ViaCEP
* `pandas`: Para manipulação de dados CSV
* `fpdf`: Para geração de relatórios PDF
* `dotenv`: Para gerenciamento de variáveis de ambiente
* `smtplib`: Para envio de e-mails

### Configurações Iniciais

1. Instale as dependências:
   ```bash
pip install requests pandas fpdf python-dotenv
```

2. Configure o arquivo `.env`:
   ```makefile
EMAIL_SENDER=seu_email@gmail.com
EMAIL_PASSWORD=sua_senha_app
DESTINATARIO_PADRAO=destinatario@email.com
```

3. Estrutura de diretórios necessária:
   ```
data/
├── ceps_lista_30.csv  # Lista de CEPs para consulta
└── resultados.csv     # Resultados das consultas
```

## Como Usar
-------------

1. Prepare o arquivo CSV de entrada (`ceps_lista_30.csv`) com uma coluna chamada "CEP":
   ```csv
CEP
01001-000
01101-001
```

2. Execute o programa:
   ```bash
python main.py
```

## Limitações Atuais
-------------------

1. Taxa de requisição fixa de 1 segundo por consulta
2. Necessidade de configuração manual do SMTP para envio de e-mails
3. Processamento sequencial dos CEPs
4. Dependência direta da disponibilidade da API ViaCEP

## Possíveis Melhorias
---------------------

1. Implementar sistema de rate limiting configurável
2. Adicionar suporte a múltiplas APIs de CEP
3. Implementar processamento paralelo para maior eficiência
4. Criar interface gráfica para configuração
5. Adicionar mais opções de formato de relatório
6. Implementar cache de consultas recentes
7. Adicionar tratamento mais robusto de erros de rede

## Contribuição
--------------

Para contribuir com o projeto:

1. Faça um fork deste repositório
2. Crie uma branch para sua feature (`git checkout -b minha-feature`)
3. Envie um pull request com suas alterações

