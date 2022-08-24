# Generated by Django 4.0.6 on 2022-08-24 01:02

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('finance', '0008_alter_invoice_payment_date'),
    ]

    operations = [
        migrations.AddField(
            model_name='invoice',
            name='contract',
            field=models.ForeignKey(default=1, on_delete=django.db.models.deletion.CASCADE, to='finance.contract', verbose_name='Contrato'),
            preserve_default=False,
        ),
    ]
