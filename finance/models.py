from core.models import BaseModel
from django.db import models
from django.utils.translation import gettext_lazy as _

from .enums import ContractStatus, InvoiceFrequencyType, InvoiceStatus


class Address(BaseModel):
    street = models.CharField(_("Rua"), max_length=500, null=True, blank=True)
    number = models.CharField(_("Número"), max_length=60, null=True, blank=True)
    city = models.CharField(_("Cidade"), max_length=200, null=True, blank=True)
    state = models.CharField(_("Estado"), max_length=10, null=True, blank=True)
    zipcode = models.CharField(_("CEP"), max_length=60, null=True, blank=True)
    complement = models.CharField(_("Complemento"), max_length=200, null=True, blank=True)
    neighborhood = models.CharField(_("Bairro"), max_length=200, null=True, default="neighborhood")
    reference = models.CharField(_("Referência"), default="", max_length=160, null=True, blank=True)

    class Meta:
        verbose_name = "Endereço"
        verbose_name_plural = "Endereços"


class Company(BaseModel):
    cnpj = models.CharField(_("CPNJ do cliente"), max_length=14, blank=False, null=False)
    fantasy_name = models.CharField(_("Nome fantasia"), max_length=50, blank=False, null=False)
    social_reason = models.CharField(_("Razão social"), max_length=50, blank=False, null=False)
    address = models.OneToOneField(
        "finance.Address",
        verbose_name=_("Endereço"),
        on_delete=models.CASCADE,
        null=False,
        blank=False,
    )
    email = models.EmailField(_("E-mail"), max_length=254)

    class Meta:
        verbose_name = "Cliente"
        verbose_name_plural = "Clientes"


class Invoice(BaseModel):
    value = models.DecimalField(_("Valor da fatura"), max_digits=5, decimal_places=2)
    client = models.ForeignKey("finance.Company", verbose_name=_("Cliente"), on_delete=models.CASCADE, blank=False, null=False)
    accountant = models.ForeignKey(
        "core.CustomUser", verbose_name=_("Contador"), on_delete=models.CASCADE, null=False, blank=False
    )
    status = models.CharField(_("Status da fatura"), max_length=20, choices=InvoiceStatus.choices)
    payment_date = models.DateTimeField(_("Data de pagamento"), auto_now=False, auto_now_add=False)
    due_date = models.DateTimeField(_("Data de vencimento"), auto_now=False, auto_now_add=False)

    class Meta:
        verbose_name = "Recibo"
        verbose_name_plural = "Recibos"


class Contract(BaseModel):
    client = models.ForeignKey("finance.Company", verbose_name=_("Cliente"), on_delete=models.CASCADE, blank=False, null=False)
    accountant = models.ForeignKey(
        "core.CustomUser", verbose_name=_("Contador"), on_delete=models.CASCADE, null=False, blank=False
    )
    start_date = models.DateTimeField(_("Data de início do contrato"), auto_now=False, auto_now_add=False)
    end_date = models.DateTimeField(_("Data de fim do contrato"), auto_now=False, auto_now_add=False)
    status = models.CharField(_("Status do contrato"), max_length=20, choices=ContractStatus.choices)
    invoice_frequency = models.CharField(
        _("Frequência da cobrança"),
        max_length=50,
        null=False,
        blank=False,
        choices=InvoiceFrequencyType.choices,
        default=InvoiceFrequencyType.MONTHLY.value,
    )

    class Meta:
        verbose_name = "Contrato"
        verbose_name_plural = "Contratos"
