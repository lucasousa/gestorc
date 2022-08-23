from django import forms
from django.forms import inlineformset_factory, modelformset_factory, modelform_factory
from django_cpf_cnpj.forms import CNPJForm
from django_cpf_cnpj.fields import CNPJField

from django.forms.fields import CharField
from django.conf import settings
from django.core.exceptions import ValidationError
from django.utils.text import format_lazy
from django.utils.translation import gettext_lazy as _
from django.core import validators

from django_cpf_cnpj.validators import validate_cpf, validate_cnpj
from django_cpf_cnpj.widgets import CPFWidget, CNPJWidget
from django_cpf_cnpj.cpf import cpf_to_python
from django_cpf_cnpj.cnpj import cnpj_to_python

from .models import Address, Company, Contract, Invoice
from .signals import create_invoices


class CustomCNPJForm(CNPJForm):
    def __init__(self, *args, masked=False, **kwargs):
        super().__init__(*args, **kwargs)
        self.widget = kwargs["widget"]
        self.masked = getattr(settings, "CNPJ_MASKED", None) or masked

        if "invalid" not in self.error_messages:
            if masked:
                example_number = "00.123.456/7890-01"
                error_message = _("Enter a valid cnpj number (e.g. {example_number})")
            else:
                example_number = "00123456789001"
                error_message = _("Enter a valid cnpj number (e.g. {example_number}).")

            self.error_messages["invalid"] = format_lazy(error_message, example_number=example_number)


class CompanyForm(forms.ModelForm):
    cnpj = forms.CharField(required=True, widget=forms.TextInput(attrs={"class": "input is-normal"}), validators=[validate_cnpj])
    fantasy_name = forms.CharField(required=True, widget=forms.TextInput(attrs={"class": "input is-normal"}))
    social_reason = forms.CharField(required=True, widget=forms.TextInput(attrs={"class": "input is-normal"}))
    email = forms.EmailField(
        required=True,
        widget=forms.TextInput(attrs={"class": "input is-normal"}),
    )

    class Meta:
        model = Company
        exclude = ["created_at", "update_at", "uuid"]

    def __init__(self, *args, **kwargs):
        super(CompanyForm, self).__init__(*args, **kwargs)
        self.fields["cnpj"].label = "CNPJ"
        self.fields["fantasy_name"].label = "Nome Fantasia"
        self.fields["social_reason"].label = "Razão Social"
        self.fields["email"].label = "E-mail"


class AddressForm(forms.ModelForm):
    cnpj = forms.CharField(required=True, widget=forms.TextInput(attrs={"class": "input is-normal"}), validators=[validate_cnpj])
    fantasy_name = forms.CharField(required=True, widget=forms.TextInput(attrs={"class": "input is-normal"}))
    social_reason = forms.CharField(required=True, widget=forms.TextInput(attrs={"class": "input is-normal"}))
    email = forms.EmailField(
        required=True,
        widget=forms.TextInput(attrs={"class": "input is-normal"}),
    )

    class Meta:
        model = Address
        fields = [
            "cnpj",
            "fantasy_name",
            "social_reason",
            "email",
            "street",
            "number",
            "city",
            "state",
            "zipcode",
            "complement",
            "neighborhood",
            "reference",
        ]

    def __init__(self, *args, **kwargs):
        super(AddressForm, self).__init__(*args, **kwargs)
        self.fields["cnpj"].label = "CNPJ"
        self.fields["fantasy_name"].label = "Nome Fantasia"
        self.fields["social_reason"].label = "Razão Social"
        self.fields["email"].label = "E-mail"

        # self.fields["cnpj"].value = self.object.company_set().first().cnpj if self.object else None
        # self.fields["fantasy_name"].value = self.object.company_set().first().fantasy_name if self.object else None
        # self.fields["social_reason"].value = self.object.company_set().first().social_reason if self.object else None
        # self.fields["email"].value = self.object.company_set().first().email if self.object else None

    def save(self, commit=True):
        address = super().save()
        if commit:
            if company := address.company_set.first():
                company.cnpj = self.data["cnpj"]
                company.fantasy_name = self.data["fantasy_name"]
                company.social_reason = self.data["social_reason"]
                company.email = self.data["email"]
                company.save()
            else:
                Company.objects.create(
                    cnpj=self.data["cnpj"],
                    fantasy_name=self.data["fantasy_name"],
                    social_reason=self.data["social_reason"],
                    email=self.data["email"],
                    address=address,
                )
        return address


class ContractForm(forms.ModelForm):
    class Meta:
        model = Contract
        exclude = ["created_at", "update_at", "uuid", "address"]

    def __init__(self, *args, **kwargs):
        super(ContractForm, self).__init__(*args, **kwargs)

    def save(self, commit=True):
        if commit and self.instance.pk is None:
            create_invoices(self.instance)
        super(ContractForm, self).save(commit=commit)


class InvoiceForm(forms.ModelForm):
    class Meta:
        model = Invoice
        exclude = ["created_at", "update_at", "uuid"]

    def __init__(self, *args, **kwargs):
        super(InvoiceForm, self).__init__(*args, **kwargs)


CompanyInlineFormSet = modelform_factory(Company, fields=["cnpj", "fantasy_name", "social_reason", "email"], form=CompanyForm)
