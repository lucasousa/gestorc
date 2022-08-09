from django import forms

from .models import Address, Company


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


AddressFormsInline = forms.inlineformset_factory(Company, Address, form=AddressForm)
