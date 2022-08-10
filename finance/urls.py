from django.contrib.auth.decorators import permission_required
from django.urls import path

from .views import (
    CompanyCreate,
    CompanyDetail,
    CompanyList,
    CompanyUpdate,
    ContractCreate,
    ContractDetail,
    ContractList,
    ContractUpdate,
    InvoiceCreate,
    InvoiceDetail,
    InvoiceList,
    InvoiceUpdate,
    company_delete,
    contract_delete,
    invoice_delete,
)

app_name = "finance"


urlpatterns = [
    # company urls
    path(
        "company/listar/",
        permission_required("company:company_list", raise_exception=True)(CompanyList.as_view()),
        name="company_list",
    ),
    path(
        "company/<int:pk>/detalhes/",
        permission_required("company:company_details", raise_exception=True)(CompanyDetail.as_view()),
        name="company_details",
    ),
    path(
        "company/<int:pk>/editar/",
        permission_required("company:company_update", raise_exception=True)(CompanyUpdate.as_view()),
        name="company_update",
    ),
    path(
        "company/adicionar/",
        permission_required("company:company_create", raise_exception=True)(CompanyCreate.as_view()),
        name="company_create",
    ),
    path(
        "company/<int:pk>/deletar/",
        permission_required("company:company_delete", raise_exception=True)(company_delete),
        name="company_delete",
    ),
    # contract urls
    path(
        "contract/listar/",
        permission_required("contract:contract_list", raise_exception=True)(ContractList.as_view()),
        name="contract_list",
    ),
    path(
        "contract/<int:pk>/detalhes/",
        permission_required("contract:contract_details", raise_exception=True)(ContractDetail.as_view()),
        name="contract_details",
    ),
    path(
        "contract/<int:pk>/editar/",
        permission_required("contract:contract_update", raise_exception=True)(ContractUpdate.as_view()),
        name="contract_update",
    ),
    path(
        "contract/adicionar/",
        permission_required("contract:contract_create", raise_exception=True)(ContractCreate.as_view()),
        name="contract_create",
    ),
    path(
        "contract/<int:pk>/deletar/",
        permission_required("contract:contract_delete", raise_exception=True)(contract_delete),
        name="contract_delete",
    ),
    # invoice urls
    path(
        "invoice/listar/",
        permission_required("invoic:invoice_list", raise_exception=True)(InvoiceList.as_view()),
        name="invoice_list",
    ),
    path(
        "invoice/<int:pk>/detalhes/",
        permission_required("invoice:invoice_details", raise_exception=True)(InvoiceDetail.as_view()),
        name="invoice_details",
    ),
    path(
        "invoice/<int:pk>/editar/",
        permission_required("invoice:invoice_update", raise_exception=True)(InvoiceUpdate.as_view()),
        name="invoice_update",
    ),
    path(
        "invoice/adicionar/",
        permission_required("invoice:invoice_create", raise_exception=True)(InvoiceCreate.as_view()),
        name="invoice_create",
    ),
    path(
        "invoice/<int:pk>/deletar/",
        permission_required("invoice:invoice_delete", raise_exception=True)(invoice_delete),
        name="invoice_delete",
    ),
]
