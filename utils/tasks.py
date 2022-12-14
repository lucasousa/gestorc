from datetime import datetime

from django.conf import settings
from django.core.mail import EmailMultiAlternatives
from django.db.models import Exists, OuterRef
from django.template.loader import render_to_string
from django.utils.html import strip_tags
from finance.enums import InvoiceStatus
from finance.helpers import aux_render_pdf
from finance.models import Contract, Invoice
from gestorc.celery import app


# @app.task(bind=True)
def check_pending_invoices(contract_id=None):
    if contract_id:
        contracts = Contract.objects.filter(id=contract_id)
    else:
        contracts = Contract.objects.filter(
            Exists(
                Invoice.objects.filter(
                    contract_id=OuterRef("pk"),
                    due_date__lte=datetime.now().date(),
                    status__in=[InvoiceStatus.OVERDUE.value, InvoiceStatus.IN_DAYS.value],
                )
            )
        )

    for contract in contracts.iterator():
        invoices = contract.invoice_set.filter(
            due_date__lte=datetime.now().date(), status__in=[InvoiceStatus.OVERDUE.value, InvoiceStatus.IN_DAYS.value]
        )
        _, file = aux_render_pdf(
            "contract/contract_pdf.html",
            {"objects": invoices},
        )
        send_invoice_email(invoices, contract.client.email, file.getvalue())


def send_invoice_email(invoices, client_email, file):
    context = {"invoices": invoices, "email": client_email}

    send_custom_email(
        template_path="core/email.html", context=context, to_email=client_email, subject="Informação sobre fatura", file=file
    )


def send_custom_email(template_path, context, to_email, subject, file):
    to = [f"{to_email}"]

    html_content = render_to_string(template_path, context)
    text_content = strip_tags(html_content)
    from_email = settings.EMAIL_HOST_USER
    msg = EmailMultiAlternatives(subject, text_content, from_email, to)
    msg.attach_alternative(html_content, "text/html")
    msg.attach("invoice.pdf", content=file, mimetype="application/pdf")
    msg.send()
