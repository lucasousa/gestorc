from core.models import BaseModel
from django.core.validators import MaxLengthValidator, MinLengthValidator, RegexValidator
from django.db import models
from django.utils.translation import gettext_lazy as _
from django_cpf_cnpj.fields import CNPJField

from .enums import ContractStatus, InvoiceFrequencyType, InvoiceStatus


class Address(BaseModel):
    street = models.CharField(_("Rua"), max_length=500, null=True, blank=True)
    number = models.CharField(
        _("Número"), validators=[RegexValidator("^[0-9]*$", message=_("Somente números"))], max_length=60, null=True, blank=True
    )
    city = models.CharField(_("Cidade"), max_length=200, null=True, blank=True)
    state = models.CharField(_("Estado"), max_length=10, null=True, blank=True)
    zipcode = models.CharField(
        _("CEP"),
        validators=[
            RegexValidator("^[0-9]*$", message=_("Somente números")),
            MaxLengthValidator(8, message=_("Tamanho inválido")),
            MinLengthValidator(8, message=_("Tamanho inválido")),
        ],
        max_length=60,
        null=True,
        blank=True,
    )
    complement = models.CharField(_("Complemento"), max_length=200, null=True, blank=True)
    neighborhood = models.CharField(_("Bairro"), max_length=200, null=True, blank=True)
    reference = models.CharField(_("Referência"), default="", max_length=160, null=True, blank=True)

    class Meta:
        verbose_name = "Endereço"
        verbose_name_plural = "Endereços"

    def __str__(self) -> str:
        return f"Endereço Nº {self.number}"

    @property
    def full_address(self):
        return f"{self.street}, {self.number} - {self.neighborhood}. {self.city}-{self.state.upper()}"


class Company(BaseModel):
    cnpj = CNPJField(masked=False, verbose_name=_("CPNJ do cliente"), blank=False, null=False)
    fantasy_name = models.CharField(_("Nome fantasia"), max_length=50, blank=False, null=False)
    social_reason = models.CharField(_("Razão social"), max_length=50, blank=False, null=False)
    address = models.ForeignKey(
        Address,
        verbose_name=_("Endereço"),
        on_delete=models.CASCADE,
        null=False,
        blank=False,
    )
    email = models.EmailField(_("E-mail"), max_length=254)

    class Meta:
        verbose_name = "Cliente"
        verbose_name_plural = "Clientes"

    def __str__(self) -> str:
        return self.fantasy_name


class Invoice(BaseModel):
    value = models.DecimalField(_("Valor da fatura"), max_digits=7, decimal_places=2)
    client = models.ForeignKey("finance.Company", verbose_name=_("Cliente"), on_delete=models.CASCADE, blank=False, null=False)
    accountant = models.ForeignKey(
        "core.CustomUser", verbose_name=_("Contador"), on_delete=models.CASCADE, null=False, blank=False
    )
    contract = models.ForeignKey("finance.Contract", verbose_name=_("Contrato"), on_delete=models.CASCADE, null=False, blank=False)
    status = models.CharField(_("Status da fatura"), max_length=20, choices=InvoiceStatus.choices)
    payment_date = models.DateField(_("Data de pagamento"), auto_now=False, auto_now_add=False, null=True)
    due_date = models.DateField(_("Data de vencimento"), auto_now=False, auto_now_add=False)

    class Meta:
        verbose_name = "Recibo"
        verbose_name_plural = "Recibos"

    def __str__(self) -> str:
        return f"Fatura - {self.client.fantasy_name}"


class Contract(BaseModel):
    client = models.ForeignKey("finance.Company", verbose_name=_("Cliente"), on_delete=models.DO_NOTHING, blank=False, null=False)
    accountant = models.ForeignKey(
        "core.CustomUser", verbose_name=_("Contador"), on_delete=models.CASCADE, null=False, blank=False
    )
    start_date = models.DateField(_("Data de início do contrato"), auto_now=False, auto_now_add=False)
    end_date = models.DateField(_("Data de fim do contrato"), auto_now=False, auto_now_add=False)
    status = models.CharField(_("Status do contrato"), max_length=20, choices=ContractStatus.choices)
    invoice_value = models.DecimalField(_("Valor da fatura"), max_digits=7, decimal_places=2, default=50)
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

    def __str__(self) -> str:
        return f"Contrato - {self.client.fantasy_name}"
