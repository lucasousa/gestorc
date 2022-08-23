from django.db.models import TextChoices
from django.utils.translation import gettext_lazy as _


class InvoiceStatus(TextChoices):
    PAID = "paid", _("Pago")
    OVERDUE = "overdue", _("Vencido")
    IN_DAYS = "in_days", _("Em dias")
    LATE_PAYMENT = "late_payment", _("Pago com atraso")


class ContractStatus(TextChoices):
    NO_DEBT = "no_debt", _("Sem débitos ativos")
    LATE_PAYMENT = "late_payment", _("Pagamento atrasado")
    FINISHED = "finished", _("Contrato finalizado")


class InvoiceFrequencyType(TextChoices):
    MONTHLY = "monthly", _("Mensal")
    QUARTERLY = "quarterly", _("Trimestral")
    SEMIANNUAL = "semiannual", _("Semestral")
    ANNUALLY = "annually", _("Anual")


HASHMAP_INVOICE_FREQUENCY = {
    InvoiceFrequencyType.MONTHLY.value: 1,
    InvoiceFrequencyType.QUARTERLY.value: 3,
    InvoiceFrequencyType.SEMIANNUAL.value: 6,
    InvoiceFrequencyType.ANNUALLY.value: 12,
}
