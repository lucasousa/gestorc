# Generated by Django 4.0.6 on 2022-08-23 23:47

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('finance', '0007_contract_invoice_value_and_more'),
    ]

    operations = [
        migrations.AlterField(
            model_name='invoice',
            name='payment_date',
            field=models.DateTimeField(null=True, verbose_name='Data de pagamento'),
        ),
    ]
