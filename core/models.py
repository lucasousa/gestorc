import re
import uuid

from django.contrib.auth.models import AbstractBaseUser, PermissionsMixin
from django.core import validators
from django.db import models
from django.utils.translation import gettext_lazy as _

from core.managers import UserManager


class BaseModel(models.Model):
    uuid = models.UUIDField(unique=True, default=uuid.uuid4)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        abstract = True


class CustomUser(AbstractBaseUser, PermissionsMixin):
    username = models.CharField(
        "Username",
        max_length=50,
        unique=True,
        validators=[
            validators.RegexValidator(
                re.compile("^[\w.@+-]+$"),
                "Informe um nome de usuário válido. "
                "Este valor deve conter apenas letras, números "
                "e os caracteres: @/./+/-/_ .",
                "invalid",
            )
        ],
    )
    is_active = models.BooleanField(default=True)
    is_staff = models.BooleanField(default=False)

    USERNAME_FIELD = "username"
    REQUIRED_FIELDS = []

    objects = UserManager()

    def __str__(self) -> str:
        return self.username

    class Meta:
        verbose_name = "Usuário"
        verbose_name_plural = "Usuários"


class Profile(BaseModel):
    user = models.OneToOneField("core.CustomUser", verbose_name=_("usuário"), on_delete=models.CASCADE)
    name = models.CharField("Nome", max_length=50, null=False, blank=False)
    image = models.ImageField("Imagem", upload_to="media/avatar", default="default.jpg", null=True, blank=True)
    cpf = models.CharField(_("CPF"), max_length=11, blank=True, null=True, unique=True)
    cnpj = models.CharField(_("CNPJ"), max_length=14, blank=True, null=True, unique=True)

    class Meta:
        verbose_name = "Perfil"
        verbose_name_plural = "Perfis"
