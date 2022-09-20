from datetime import datetime, timedelta
from io import BytesIO

from django.http import HttpResponse
from django.template.loader import get_template
from xhtml2pdf import pisa

from .enums import HASHMAP_INVOICE_FREQUENCY, InvoiceStatus
from .models import Invoice


def create_invoices(instance):
    amount_of_months_between = HASHMAP_INVOICE_FREQUENCY[instance.invoice_frequency]
    total_months = (instance.end_date - instance.start_date).days // 30
    for period in range(total_months // amount_of_months_between):
        due_date = instance.start_date + timedelta(days=30 * (period + 1) * amount_of_months_between)
        if due_date.isoweekday() == 7:
            due_date += timedelta(days=1)
        elif due_date.isoweekday() == 6:
            due_date += timedelta(days=2)

        Invoice.objects.create(
            value=instance.invoice_value,
            client=instance.client,
            accountant=instance.accountant,
            status=InvoiceStatus.IN_DAYS.value,
            due_date=due_date,
            contract=instance,
        )


def aux_render_pdf(template_src, context_dict={}):
    template = get_template(template_src)
    html = template.render(context_dict)
    result = BytesIO()
    pdf = pisa.pisaDocument(html, result)
    return pdf, result


def render_to_pdf(template_src, context_dict={}):
    pdf, result = aux_render_pdf(template_src, context_dict)
    if not pdf.err:
        return HttpResponse(result.getvalue(), content_type="application/pdf")
    return None
