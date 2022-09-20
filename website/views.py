from django.views.generic import TemplateView


class IndexView(TemplateView):
    template_name = "website/index.html"

    # def get_context_data(self, *args, **kwargs):
    #     context = super().get_context_data(**kwargs)
    #     context["news"] = Notice.objects.filter(published=True, publication_date__lte=datetime.now()).order_by(
    #         "-publication_date"
    #     )[:3]
    #     context["videos"] = Video.objects.filter(published=True).order_by("-created_at")[:3]
    #     context["directors"] = Directors.objects.all()[:3]
    #     context["banners"] = Banner.objects.filter(published=True)
    #     return context

    # def post(self, request, *args, **kwargs):
    #     name = request.POST.get("name")
    #     email = request.POST.get("email")
    #     content = request.POST.get("content")

    #     subject = f"[ACIPI] - Contato"
    #     to = ["acipioficial@gmail.com"]
    #     html_content = render_to_string("core/email.html", {"name": name, "content": content, "email": email})
    #     text_content = strip_tags(html_content)
    #     from_email = settings.DEFAULT_FROM_EMAIL
    #     msg = EmailMultiAlternatives(subject, text_content, from_email, to)
    #     msg.attach_alternative(html_content, "text/html")
    #     msg.send()

    #     messages.info(self.request, "E-mail enviado com Sucesso!")
    #     return HttpResponseRedirect(reverse("website:index"))
