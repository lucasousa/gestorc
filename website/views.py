from django.conf import settings
from django.contrib import messages
from django.core.mail import EmailMultiAlternatives
from django.http import HttpResponseRedirect
from django.template.loader import render_to_string
from django.urls import reverse
from django.utils.html import strip_tags
from django.views.generic import TemplateView


class IndexView(TemplateView):
    template_name = "website/index.html"

    def post(self, request, *args, **kwargs):
        name = request.POST.get("name")
        email = request.POST.get("email")
        content = request.POST.get("content")

        subject = f"GestorC - Contato"
        to = ["locafacil432@gmail.com"]
        html_content = render_to_string("website/email.html", {"name": name, "content": content, "email": email})
        text_content = strip_tags(html_content)
        from_email = settings.EMAIL_HOST_USER
        msg = EmailMultiAlternatives(subject, text_content, from_email, to)
        msg.attach_alternative(html_content, "text/html")
        msg.send()

        messages.info(self.request, "E-mail enviado com sucesso!")
        return HttpResponseRedirect(reverse("website:index"))
