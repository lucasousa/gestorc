from datetime import datetime, timedelta

from django.db.models.signals import post_save, pre_save
from django.dispatch import receiver

from .enums import HASHMAP_INVOICE_FREQUENCY, InvoiceStatus
from .models import Contract, Invoice


def create_invoices(instance):
    amount_of_months_between = HASHMAP_INVOICE_FREQUENCY[instance.invoice_frequency]
    total_months = (instance.end_date - instance.start_date).days // 30
    for period in range(total_months // amount_of_months_between):
        due_date = datetime.now() + timedelta(days=30 * period * amount_of_months_between)
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
        )
