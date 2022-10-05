# Generated by Django 4.0.6 on 2022-10-05 00:07

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('finance', '0011_alter_contract_end_date_alter_contract_start_date'),
    ]

    operations = [
        migrations.AlterField(
            model_name='invoice',
            name='due_date',
            field=models.DateField(verbose_name='Data de vencimento'),
        ),
        migrations.AlterField(
            model_name='invoice',
            name='payment_date',
            field=models.DateField(null=True, verbose_name='Data de pagamento'),
        ),
    ]
