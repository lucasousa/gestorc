import pytest
from django.test import Client
from django.urls import reverse
from model_bakery import baker


@pytest.fixture
def user():
    return baker.make("core.CustomUser", is_staff=True, is_superuser=True)


@pytest.fixture
def client(user):
    c = Client()
    c.force_login(user)
    return c


@pytest.mark.django_db
class TestContract:
    def test_list_contracts(self, client):
        response = client.get(reverse("finance:contract_list"))
        assert response.status_code == 200

    def test_create_contract(self, client):
        response = client.post(reverse("finance:contract_create"))
        assert response.status_code == 200

    def test_update_contract(self, client):
        response = client.put(reverse("finance:contract_update", kwargs={"pk": 2937468}))
        assert response.status_code == 404

    def test_delete_contract(self, client):
        response = client.delete(reverse("finance:contract_delete", kwargs={"pk": 2638742}))
        assert response.status_code == 404


@pytest.mark.django_db
class TestCompany:
    def test_list_companies(self, client):
        response = client.get(reverse("finance:company_list"))
        assert response.status_code == 200

    def test_create_company(self, client):
        response = client.post(reverse("finance:company_create"))
        assert response.status_code == 200

    def test_update_company(self, client):
        response = client.put(reverse("finance:company_update", kwargs={"pk": 2937468}))
        assert response.status_code == 404

    def test_delete_company(self, client):
        response = client.delete(reverse("finance:company_delete", kwargs={"pk": 2638742}))
        assert response.status_code == 404


@pytest.mark.django_db
class TestInvoice:
    def test_list_invoices(self, client):
        response = client.get(reverse("finance:invoice_list"))
        assert response.status_code == 200

    def test_create_invoice(self, client):
        response = client.post(reverse("finance:invoice_create"))
        assert response.status_code == 200

    def test_update_invoice(self, client):
        response = client.put(reverse("finance:invoice_update", kwargs={"pk": 2937468}))
        assert response.status_code == 404

    def test_delete_invoice(self, client):
        response = client.delete(reverse("finance:invoice_delete", kwargs={"pk": 2638742}))
        assert response.status_code == 404
