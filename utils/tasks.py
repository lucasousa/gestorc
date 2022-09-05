from datetime import datetime

from django.conf import settings
from django.core.mail import EmailMultiAlternatives
from django.db.models import Exists, OuterRef
from django.template.loader import render_to_string
from django.utils.html import strip_tags

from gestorc.celery import app
from finance.models import Contract, Invoice
from finance.enums import InvoiceStatus


@app.task(bind=True)
def check_pending_invoices():
    contracts = Contract.objects.filter(
        Exists(
            Invoice.objects.filter(
                contract_id=OuterRef("pk"),
                due_date__date__lte=datetime.now().date(),
                status__in=[InvoiceStatus.OVERDUE.value, InvoiceStatus.IN_DAYS.value]
            )
        )
    )

    for contract in contracts.iterator():
        invoices = contract.invoice_set.filter(
            due_date__date__lte=datetime.now().date(),
            status__in=[InvoiceStatus.OVERDUE.value, InvoiceStatus.IN_DAYS.value]
        )
        send_invoice_email(invoices, contract.client.email)


def send_invoice_email(invoices, client_email):
    context = {
        "invoices": invoices,
        "email": client_email
    }

    send_custom_email(
        template_path="core/email.html",
        context=context,
        to_email=client_email,
        subject="Informação sobre fatura",
    )


def send_custom_email(template_path, context, to_email, subject):
    to = [f"{to_email}"]

    html_content = render_to_string(template_path, context)
    text_content = strip_tags(html_content)
    from_email = settings.EMAIL_HOST_USER
    msg = EmailMultiAlternatives(subject, text_content, from_email, to)
    msg.attach_alternative(html_content, "text/html")
    msg.send()
