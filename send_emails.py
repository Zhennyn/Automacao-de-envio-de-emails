import argparse
import csv
import os
import smtplib
import time
from dataclasses import dataclass
from email.message import EmailMessage
from pathlib import Path
from typing import Iterable, List

from dotenv import load_dotenv


@dataclass
class Contact:
    nome: str
    email: str


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description="Automacao de envio de emails")
    parser.add_argument(
        "--csv",
        default="data/contatos.csv",
        help="Caminho para arquivo CSV com as colunas nome,email",
    )
    parser.add_argument(
        "--html-template",
        default="templates/email.html",
        help="Template HTML do email",
    )
    parser.add_argument(
        "--text-template",
        default="templates/email.txt",
        help="Template texto do email (fallback)",
    )
    parser.add_argument(
        "--delay",
        type=float,
        default=2.0,
        help="Delay em segundos entre envios",
    )
    parser.add_argument(
        "--limit",
        type=int,
        default=0,
        help="Limite maximo de emails (0 = sem limite)",
    )
    parser.add_argument(
        "--send",
        action="store_true",
        help="Envia de verdade. Sem essa flag, roda em modo de simulacao.",
    )
    return parser.parse_args()


def get_required_env(name: str) -> str:
    value = os.getenv(name, "").strip()
    if not value:
        raise ValueError(f"Variavel obrigatoria ausente: {name}")
    return value


def load_contacts(csv_path: Path) -> List[Contact]:
    if not csv_path.exists():
        raise FileNotFoundError(f"CSV nao encontrado: {csv_path}")

    contacts: List[Contact] = []
    with csv_path.open("r", encoding="utf-8-sig", newline="") as f:
        reader = csv.DictReader(f)
        for row in reader:
            nome = (row.get("nome") or "").strip()
            email = (row.get("email") or "").strip()
            if not nome or not email:
                continue
            contacts.append(Contact(nome=nome, email=email))
    return contacts


def render_template(template: str, contact: Contact) -> str:
    return template.format(nome=contact.nome, email=contact.email)


def build_email(
    sender_email: str,
    sender_name: str,
    to_email: str,
    subject: str,
    html_body: str,
    text_body: str,
) -> EmailMessage:
    msg = EmailMessage()
    msg["Subject"] = subject
    msg["From"] = f"{sender_name} <{sender_email}>"
    msg["To"] = to_email
    msg.set_content(text_body)
    msg.add_alternative(html_body, subtype="html")
    return msg


def send_messages(
    contacts: Iterable[Contact],
    smtp_host: str,
    smtp_port: int,
    smtp_user: str,
    smtp_password: str,
    sender_name: str,
    sender_email: str,
    subject: str,
    html_template: str,
    text_template: str,
    delay_seconds: float,
    dry_run: bool,
    limit: int,
) -> None:
    sent_count = 0
    errors = 0

    server = None
    if not dry_run:
        server = smtplib.SMTP(smtp_host, smtp_port, timeout=30)
        server.ehlo()
        server.starttls()
        server.ehlo()
        server.login(smtp_user, smtp_password)

    try:
        for index, contact in enumerate(contacts, start=1):
            if limit > 0 and sent_count >= limit:
                break

            try:
                html_body = render_template(html_template, contact)
                text_body = render_template(text_template, contact)
                msg = build_email(
                    sender_email=sender_email,
                    sender_name=sender_name,
                    to_email=contact.email,
                    subject=subject,
                    html_body=html_body,
                    text_body=text_body,
                )

                if dry_run:
                    print(f"[SIMULACAO] #{index} -> {contact.email}")
                else:
                    assert server is not None
                    server.send_message(msg)
                    print(f"[ENVIADO] #{index} -> {contact.email}")

                sent_count += 1
                if delay_seconds > 0:
                    time.sleep(delay_seconds)
            except Exception as exc:
                errors += 1
                print(f"[ERRO] #{index} -> {contact.email}: {exc}")

    finally:
        if server is not None:
            server.quit()

    mode = "SIMULACAO" if dry_run else "ENVIO REAL"
    print("\nResumo")
    print(f"Modo: {mode}")
    print(f"Processados: {sent_count + errors}")
    print(f"Sucesso: {sent_count}")
    print(f"Erros: {errors}")


def main() -> None:
    load_dotenv()
    args = parse_args()

    smtp_host = get_required_env("SMTP_HOST")
    smtp_port = int(get_required_env("SMTP_PORT"))
    smtp_user = get_required_env("SMTP_USER")
    smtp_password = get_required_env("SMTP_PASSWORD")
    sender_name = get_required_env("SENDER_NAME")
    sender_email = get_required_env("SENDER_EMAIL")
    subject = get_required_env("EMAIL_SUBJECT")

    html_template_path = Path(args.html_template)
    text_template_path = Path(args.text_template)

    if not html_template_path.exists():
        raise FileNotFoundError(f"Template HTML nao encontrado: {html_template_path}")
    if not text_template_path.exists():
        raise FileNotFoundError(f"Template texto nao encontrado: {text_template_path}")

    html_template = html_template_path.read_text(encoding="utf-8")
    text_template = text_template_path.read_text(encoding="utf-8")

    contacts = load_contacts(Path(args.csv))
    if not contacts:
        print("Nenhum contato valido encontrado no CSV.")
        return

    dry_run = not args.send
    send_messages(
        contacts=contacts,
        smtp_host=smtp_host,
        smtp_port=smtp_port,
        smtp_user=smtp_user,
        smtp_password=smtp_password,
        sender_name=sender_name,
        sender_email=sender_email,
        subject=subject,
        html_template=html_template,
        text_template=text_template,
        delay_seconds=args.delay,
        dry_run=dry_run,
        limit=args.limit,
    )


if __name__ == "__main__":
    main()
