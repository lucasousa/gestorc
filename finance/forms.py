from django import forms

from .models import Address, Company, Contract, Invoice


class AddressForm(forms.ModelForm):
    class Meta:
        model = Address
        exclude = ["created_at", "update_at", "uuid"]

    def __init__(self, *args, **kwargs):
        super(AddressForm, self).__init__(*args, **kwargs)


class CompanyForm(forms.ModelForm):
    class Meta:
        model = Company
        exclude = ["created_at", "update_at", "uuid"]

    def __init__(self, *args, **kwargs):
        super(CompanyForm, self).__init__(*args, **kwargs)


class ContractForm(forms.ModelForm):
    class Meta:
        model = Contract
        exclude = ["created_at", "update_at", "uuid"]

    def __init__(self, *args, **kwargs):
        super(ContractForm, self).__init__(*args, **kwargs)


class InvoiceForm(forms.ModelForm):
    class Meta:
        model = Invoice
        exclude = ["created_at", "update_at", "uuid"]

    def __init__(self, *args, **kwargs):
        super(InvoiceForm, self).__init__(*args, **kwargs)
