# 📧 Automação de Envio de E-mails
Solução em Python para disparo de e-mails em lote com personalização, foco em produtividade operacional e boas práticas de automação.

![Capa do Projeto](https://raw.githubusercontent.com/SEU-USUARIO/SEU-REPOSITORIO/main/img/capa-email-automation.png)

## ✨ Funcionalidades
- 📬 Envio em lote a partir de planilha CSV com colunas nome e email
- 🧠 Personalização dinâmica com placeholders como {nome} e {email}
- 🧪 Modo simulação para validar campanha sem disparar e-mails reais
- ✅ Envio real controlado por flag, reduzindo riscos operacionais
- ⏱️ Controle de taxa de envio com delay entre mensagens
- 🎯 Limite de disparos por execução para testes e lotes parciais
- 📝 Templates em texto e HTML para melhor entregabilidade
- 🔐 Configuração segura via variáveis de ambiente

## 🛠️ Tecnologias Utilizadas
![Python](https://img.shields.io/badge/Python-3.10+-3776AB?style=for-the-badge&logo=python&logoColor=white)
![SMTP](https://img.shields.io/badge/SMTP-Email%20Protocol-0A66C2?style=for-the-badge&logo=gmail&logoColor=white)
![Python Dotenv](https://img.shields.io/badge/python--dotenv-Configura%C3%A7%C3%A3o%20de%20Ambiente-ECD53F?style=for-the-badge)
![HTML](https://img.shields.io/badge/HTML-Template-E34F26?style=for-the-badge&logo=html5&logoColor=white)
![CSV](https://img.shields.io/badge/CSV-Base%20de%20Contatos-2E7D32?style=for-the-badge)
![Git](https://img.shields.io/badge/Git-Versionamento-F05032?style=for-the-badge&logo=git&logoColor=white)

## 🚀 Como executar localmente
Pré-requisitos:
- Python 3.10 ou superior
- Conta de e-mail com SMTP ativo (ex.: Gmail com senha de app)

1. Clone o repositório:

```bash
git clone https://github.com/SEU-USUARIO/SEU-REPOSITORIO.git
cd SEU-REPOSITORIO
```

2. Crie e ative um ambiente virtual:

```bash
python -m venv .venv
```

No Windows (PowerShell):

```bash
.venv\Scripts\Activate.ps1
```

No Linux/macOS:

```bash
source .venv/bin/activate
```

3. Instale as dependências:

```bash
pip install -r requirements.txt
```

4. Configure as variáveis de ambiente:

```bash
copy .env.example .env
```

Preencha o arquivo .env com SMTP_HOST, SMTP_PORT, SMTP_USER, SMTP_PASSWORD, SENDER_NAME, SENDER_EMAIL e EMAIL_SUBJECT.

5. Atualize sua base de contatos em data/contatos.csv e ajuste os templates em templates/email.txt e templates/email.html.

6. Rode em modo simulação (recomendado):

```bash
python send_emails.py
```

7. Envie de fato quando validar tudo:

```bash
python send_emails.py --send
```

Exemplo com limite de lote e intervalo entre e-mails:

```bash
python send_emails.py --send --limit 50 --delay 1.5
```

## 📸 Screenshots
No momento, este repositório ainda não possui screenshots versionadas em img/ ou public/.

Sugestões de imagens para adicionar:
- Execução em modo simulação no terminal
- Execução em modo real com resumo final
- Exemplo do template HTML renderizado

## 🌐 Demonstração
Demo em vídeo (em breve): https://www.youtube.com/watch?v=SEU-LINK

Se preferir, adicione também:
- Link de execução guiada no LinkedIn
- GIF curto do fluxo completo no README

## 📌 Sobre o projeto
Este projeto foi desenvolvido como iniciativa prática de automação operacional (2026), com foco em reduzir tarefas repetitivas de comunicação e aumentar padronização de processos.

Mesmo sendo um projeto enxuto, ele demonstra habilidades altamente transferíveis para vagas de Suporte TI, Help Desk, Dados e Cloud:
- Automação de rotina com Python para ganho de produtividade
- Leitura e tratamento de dados estruturados (CSV)
- Configuração segura por variáveis de ambiente
- Organização de templates e padronização de comunicação
- Pensamento de operação: validação por simulação, controle de lote e tratamento de erros

Essa base pode evoluir para integrações com bancos de dados, dashboards de monitoramento e serviços cloud (Azure), ampliando rastreabilidade e escala.

---

Feito com ❤️ por Zhennyn

Contribuições são muito bem-vindas. Se você tiver sugestões de melhorias, abra uma issue ou envie um pull request.
