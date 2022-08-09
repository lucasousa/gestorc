from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.db import transaction
from django.http import HttpResponseRedirect, JsonResponse
from django.shortcuts import get_object_or_404
from django.urls import reverse
from django.utils.decorators import method_decorator
from django.views.generic import CreateView, DetailView, ListView, UpdateView

from .forms import AddressFormsInline, CompanyForm
from .models import Company


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
    model = Company
    template_name = "company/add.html"
    form_class = CompanyForm
    formset_class = AddressFormsInline

    # def get_context_data(self, **kwargs):
    #     context = super(CompanyCreate, self).get_context_data(**kwargs)
    #     if self.request.POST:
    #         context["forms"] = CompanyForm(self.request.POST)
    #         context["formset"] = AddressFormsInline(self.request.POST)
    #     else:
    #         context["forms"] = CompanyForm()
    #         context["formset"] = AddressFormsInline()
    #     return context

    def form_valid(self, form):
        context = self.get_context_data()
        address = context["address"]
        with transaction.atomic():
            self.object = form.save()
            if address.is_valid():
                address.instance = self.object
                address.save()
        messages.success(self.request, "Cliente cadastrado com sucesso.")
        return HttpResponseRedirect(self.get_success_url())

    # def form_valid(self, form):
    #     self.object = form.save(commit=False)
    #     self.object.save()
    #     form.save()

    # def form_invalid(self, form):
    #     messages.error(self.request, "Ocorreu um erro ao cadastrar Diretor.")
    #     return self.render_to_response(self.get_context_data(form=form))

    def get_success_url(self):
        return reverse("finance:company_list")


@method_decorator(login_required, name="dispatch")
class CompanyUpdate(UpdateView):
    model = Company
    template_name = "company/add.html"
    form_class = CompanyForm

    def form_valid(self, form):
        self.object = form.save(commit=False)
        self.object.save()
        form.save()
        messages.success(self.request, "Cliente atualizado com sucesso.")
        return HttpResponseRedirect(self.get_success_url())

    def form_invalid(self, form):
        messages.error(self.request, "Ocorreu um erro ao atualizar Diretor")
        return self.render_to_response(self.get_context_data(form=form))

    def get_success_url(self):
        return reverse("finance:company_list")


@login_required
def company_delete(request, pk):
    company = get_object_or_404(Company, pk=pk)
    company.delete()
    return JsonResponse({"msg": "Cliente excluído com sucesso!", "code": "1"})
