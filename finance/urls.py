from django.contrib.auth.decorators import permission_required
from django.urls import path

from .views import CompanyCreate, CompanyDetail, CompanyList, CompanyUpdate, company_delete

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
]
