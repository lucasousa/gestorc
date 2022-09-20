from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.http import HttpResponseRedirect, JsonResponse, HttpResponse
from django.shortcuts import get_object_or_404
from django.urls import reverse
from django.utils.decorators import method_decorator
from django.views.generic import View
from django.views.generic import CreateView, DetailView, ListView, UpdateView

from .forms import ContractForm, InvoiceForm, AddressForm
from .models import Company, Contract, Invoice, Address
from .helpers import render_to_pdf
from datetime import datetime
from django.template.loader import get_template


@method_decorator(login_required, name="dispatch")
class ContractList(ListView):
    model = Contract
    http_method_names = ["get"]
    template_name = "contract/list.html"
    context_object_name = "contract"
    paginate_by = 15

    def get_queryset(self):
        self.queryset = super(ContractList, self).get_queryset()
        if self.request.GET.get("search_box", False):
            self.queryset = self.queryset.filter(client__fantasy_name__icontains=self.request.GET["search_box"])
        return self.queryset

    def get_context_data(self, **kwargs):
        _super = super(ContractList, self)
        context = _super.get_context_data(**kwargs)
        adjacent_pages = 3
        page_number = context["page_obj"].number
        num_pages = context["paginator"].num_pages
        startPage = max(page_number - adjacent_pages, 1)
        if startPage <= 5:
            startPage = 1
        endPage = page_number + adjacent_pages + 1
        if endPage >= num_pages - 1:
            endPage = num_pages + 1
        page_numbers = [n for n in range(startPage, endPage) if n > 0 and n <= num_pages]
        context["holders"] = Company.objects.all()
        context.update(
            {
                "page_numbers": page_numbers,
                "show_first": 1 not in page_numbers,
                "show_last": num_pages not in page_numbers,
            }
        )
        return context


@method_decorator(login_required, name="dispatch")
class ContractDetail(DetailView):
    model = Contract
    template_name = "contract/details.html"

    def get(self, request, *args, **kwargs):
        self.object = self.get_object()
        context = self.get_context_data(object=self.object)
        return self.render_to_response(context)


@method_decorator(login_required, name="dispatch")
class ContractCreate(CreateView):
    model = Company
    template_name = "contract/add.html"
    form_class = ContractForm

    def form_valid(self, form):
        self.object = form.save(commit=False)
        form.save()
        messages.success(self.request, "Contrato cadastrado com sucesso.")
        return HttpResponseRedirect(self.get_success_url())

    def form_invalid(self, form):
        messages.error(self.request, "Ocorreu um erro ao cadastrar contrato.")
        return self.render_to_response(self.get_context_data(form=form))

    def get_success_url(self):
        return reverse("finance:contract_list")


@method_decorator(login_required, name="dispatch")
class ContractUpdate(UpdateView):
    model = Contract
    template_name = "contract/add.html"
    form_class = ContractForm

    def form_valid(self, form):
        self.object = form.save(commit=False)
        self.object.save()
        form.save()
        messages.success(self.request, "Contrato atualizado com sucesso.")
        return HttpResponseRedirect(self.get_success_url())

    def form_invalid(self, form):
        messages.error(self.request, "Ocorreu um erro ao atualizar contrato")
        return self.render_to_response(self.get_context_data(form=form))

    def get_success_url(self):
        return reverse("finance:contract_list")


@login_required
def contract_delete(request, pk):
    contract = get_object_or_404(Contract, pk=pk)
    contract.delete()
    return JsonResponse({"msg": "Contrato excluído com sucesso!", "code": "1"})


@method_decorator(login_required, name="dispatch")
class CompanyList(ListView):
    model = Company
    http_method_names = ["get"]
    template_name = "company/list.html"
    context_object_name = "company"
    paginate_by = 15

    def get_queryset(self):
        self.queryset = super(CompanyList, self).get_queryset()
        if self.request.GET.get("search_box", False):
            self.queryset = self.queryset.filter(fantasy_name__icontains=self.request.GET["search_box"])
        return self.queryset

    def get_context_data(self, **kwargs):
        _super = super(CompanyList, self)
        context = _super.get_context_data(**kwargs)
        adjacent_pages = 3
        page_number = context["page_obj"].number
        num_pages = context["paginator"].num_pages
        startPage = max(page_number - adjacent_pages, 1)
        if startPage <= 5:
            startPage = 1
        endPage = page_number + adjacent_pages + 1
        if endPage >= num_pages - 1:
            endPage = num_pages + 1
        page_numbers = [n for n in range(startPage, endPage) if n > 0 and n <= num_pages]
        context["holders"] = Company.objects.all()
        context.update(
            {
                "page_numbers": page_numbers,
                "show_first": 1 not in page_numbers,
                "show_last": num_pages not in page_numbers,
            }
        )
        return context


@method_decorator(login_required, name="dispatch")
class CompanyDetail(DetailView):
    model = Company
    template_name = "company/details.html"

    def get(self, request, *args, **kwargs):
        self.object = self.get_object()
        context = self.get_context_data(object=self.object)
        return self.render_to_response(context)


@method_decorator(login_required, name="dispatch")
class CompanyCreate(CreateView):
    model = Address
    template_name = "company/add.html"
    form_class = AddressForm

    def form_valid(self, form):
        self.object = form.save(commit=False)
        self.object.save()
        form.save()
        messages.success(self.request, "Cliente cadastrado com sucesso.")
        return HttpResponseRedirect(self.get_success_url())

    def form_invalid(self, form):
        messages.error(self.request, "Ocorreu um erro ao cadastrar Cliente.")
        return self.render_to_response(self.get_context_data(form=form))

    def get_success_url(self):
        return reverse("finance:company_list")


@method_decorator(login_required, name="dispatch")
class CompanyUpdate(UpdateView):
    model = Address
    template_name = "company/add.html"
    form_class = AddressForm

    def form_valid(self, form):
        self.object = form.save(commit=False)
        self.object.save()
        form.save()
        messages.success(self.request, "Cliente atualizado com sucesso.")
        return HttpResponseRedirect(self.get_success_url())

    def form_invalid(self, form):
        messages.error(self.request, "Ocorreu um erro ao atualizar Cliente")
        return self.render_to_response(self.get_context_data(form=form))

    def get_success_url(self):
        return reverse("finance:company_list")

    def get_initial(self):
        object = self.get_object()
        company = object.company_set.all().first()
        ret = super().get_initial()
        ret.update(
            {
                "cnpj": company.cnpj,
                "fantasy_name": company.fantasy_name,
                "social_reason": company.social_reason,
                "email": company.email,
            }
        )
        return ret


@login_required
def company_delete(request, pk):
    company = get_object_or_404(Company, pk=pk)
    company.delete()
    return JsonResponse({"msg": "Cliente excluído com sucesso!", "code": "1"})


@method_decorator(login_required, name="dispatch")
class InvoiceList(ListView):
    model = Invoice
    http_method_names = ["get"]
    template_name = "invoice/list.html"
    context_object_name = "invoice"
    paginate_by = 15

    def get_queryset(self):
        self.queryset = super(InvoiceList, self).get_queryset()
        if self.request.GET.get("search_box", False):
            self.queryset = self.queryset.filter(client__fantasy_name__icontains=self.request.GET["search_box"])
        return self.queryset

    def get_context_data(self, **kwargs):
        _super = super(InvoiceList, self)
        context = _super.get_context_data(**kwargs)
        adjacent_pages = 3
        page_number = context["page_obj"].number
        num_pages = context["paginator"].num_pages
        startPage = max(page_number - adjacent_pages, 1)
        if startPage <= 5:
            startPage = 1
        endPage = page_number + adjacent_pages + 1
        if endPage >= num_pages - 1:
            endPage = num_pages + 1
        page_numbers = [n for n in range(startPage, endPage) if n > 0 and n <= num_pages]
        context["holders"] = Company.objects.all()
        context.update(
            {
                "page_numbers": page_numbers,
                "show_first": 1 not in page_numbers,
                "show_last": num_pages not in page_numbers,
            }
        )
        return context


@method_decorator(login_required, name="dispatch")
class InvoiceDetail(DetailView):
    model = Invoice
    template_name = "invoice/details.html"

    def get(self, request, *args, **kwargs):
        self.object = self.get_object()
        context = self.get_context_data(object=self.object)
        return self.render_to_response(context)


@method_decorator(login_required, name="dispatch")
class InvoiceCreate(CreateView):
    model = Invoice
    template_name = "invoice/add.html"
    form_class = InvoiceForm

    def form_valid(self, form):
        self.object = form.save(commit=False)
        self.object.save()
        form.save()
        messages.success(self.request, "Fatura cadastrada com sucesso.")
        return HttpResponseRedirect(self.get_success_url())

    def form_invalid(self, form):
        messages.error(self.request, "Ocorreu um erro ao cadastrar fatura.")
        return self.render_to_response(self.get_context_data(form=form))

    def get_success_url(self):
        return reverse("finance:invoice_list")


@method_decorator(login_required, name="dispatch")
class InvoiceUpdate(UpdateView):
    model = Invoice
    template_name = "invoice/add.html"
    form_class = InvoiceForm

    def form_valid(self, form):
        self.object = form.save(commit=False)
        self.object.save()
        form.save()
        messages.success(self.request, "Fatura atualizado com sucesso.")
        return HttpResponseRedirect(self.get_success_url())

    def form_invalid(self, form):
        messages.error(self.request, "Ocorreu um erro ao atualizar fatura")
        return self.render_to_response(self.get_context_data(form=form))

    def get_success_url(self):
        return reverse("finance:invoice_list")


@login_required
def invoice_delete(request, pk):
    invoice = get_object_or_404(Invoice, pk=pk)
    invoice.delete()
    return JsonResponse({"msg": "Fatura excluída com sucesso!", "code": "1"})


class GeneratePDF(View):
    def get(self, request, *args, **kwargs):
        template = get_template('contract/contract_pdf.html')
        contract = Contract.objects.get(id=kwargs['id'])
        context = {
            'object':contract,
            'consultation_date': datetime.today().strftime('%d-%m-%Y %H:%M:%S')
        }
        _ = template.render(context)
        pdf = render_to_pdf('contract/contract_pdf.html', context)

        if pdf:
            response = HttpResponse(pdf, content_type='application/pdf')
            filename = "contrato_%s.pdf" % str(contract.client.fantasy_name)
            content = "inline; filename=%s" % filename
            download = request.GET.get("download")

            if download:
                content = "attachment; filename='%s'" % filename
            response['Content-Disposition'] = content
            return response

        return HttpResponse("Contrato não encontrado")