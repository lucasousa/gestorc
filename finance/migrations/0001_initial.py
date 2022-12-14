# Generated by Django 4.0.6 on 2022-07-27 01:27

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion
import uuid


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='Address',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('uuid', models.UUIDField(default=uuid.uuid4, unique=True)),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('updated_at', models.DateTimeField(auto_now=True)),
                ('street', models.CharField(blank=True, max_length=500, null=True, verbose_name='Rua')),
                ('number', models.CharField(blank=True, max_length=60, null=True, verbose_name='Número')),
                ('city', models.CharField(blank=True, max_length=200, null=True, verbose_name='Cidade')),
                ('state', models.CharField(blank=True, max_length=10, null=True, verbose_name='Estado')),
                ('zipcode', models.CharField(blank=True, max_length=60, null=True, verbose_name='CEP')),
                ('complement', models.CharField(blank=True, max_length=200, null=True, verbose_name='Complemento')),
                ('neighborhood', models.CharField(default='neighborhood', max_length=200, null=True, verbose_name='Bairro')),
                ('reference', models.CharField(blank=True, default='', max_length=160, null=True, verbose_name='Referência')),
            ],
            options={
                'verbose_name': 'Endereço',
                'verbose_name_plural': 'Endereços',
            },
        ),
        migrations.CreateModel(
            name='Company',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('uuid', models.UUIDField(default=uuid.uuid4, unique=True)),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('updated_at', models.DateTimeField(auto_now=True)),
                ('cnpj', models.CharField(max_length=14, verbose_name='CPNJ do cliente')),
                ('fantasy_name', models.CharField(max_length=50, verbose_name='Nome fantasia')),
                ('social_reason', models.CharField(max_length=50, verbose_name='Razão social')),
                ('email', models.EmailField(max_length=254, verbose_name='E-mail')),
                ('address', models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, to='finance.address', verbose_name='Endereço')),
            ],
            options={
                'verbose_name': 'Cliente',
                'verbose_name_plural': 'Clientes',
            },
        ),
        migrations.CreateModel(
            name='Invoice',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('uuid', models.UUIDField(default=uuid.uuid4, unique=True)),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('updated_at', models.DateTimeField(auto_now=True)),
                ('value', models.DecimalField(decimal_places=2, max_digits=5, verbose_name='Valor da fatura')),
                ('status', models.CharField(choices=[('paid', 'Pago'), ('overdue', 'Vencido'), ('in_days', 'Em dias'), ('late_payment', 'Pago com atraso')], max_length=20, verbose_name='Status da fatura')),
                ('payment_date', models.DateTimeField(verbose_name='Data de pagamento')),
                ('due_date', models.DateTimeField(verbose_name='Data de vencimento')),
                ('accountant', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL, verbose_name='Contador')),
                ('client', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='finance.company', verbose_name='Cliente')),
            ],
            options={
                'verbose_name': 'Recibo',
                'verbose_name_plural': 'Recibos',
            },
        ),
        migrations.CreateModel(
            name='Contract',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('uuid', models.UUIDField(default=uuid.uuid4, unique=True)),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('updated_at', models.DateTimeField(auto_now=True)),
                ('start_date', models.DateTimeField(verbose_name='Data de início do contrato')),
                ('end_date', models.DateTimeField(verbose_name='Data de fim do contrato')),
                ('status', models.CharField(choices=[('no_debt', 'Sem débitos ativos'), ('late_payment', 'Pagamento atrasado'), ('finished', 'Contrato finalizado')], max_length=20, verbose_name='Status do contrato')),
                ('invoice_frequency', models.CharField(choices=[('weekly', 'Semanal'), ('monthly', 'Mensal'), ('quarterly', 'Trimestral'), ('semiannual', 'Semestral'), ('annually', 'Anual')], default='monthly', max_length=50, verbose_name='Frequência da cobrança')),
                ('accountant', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL, verbose_name='Contador')),
                ('client', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='finance.company', verbose_name='Cliente')),
            ],
            options={
                'verbose_name': 'Contrato',
                'verbose_name_plural': 'Contratos',
            },
        ),
    ]
