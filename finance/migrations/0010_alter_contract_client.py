# Generated by Django 4.0.6 on 2022-09-20 23:49

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('finance', '0009_invoice_contract'),
    ]

    operations = [
        migrations.AlterField(
            model_name='contract',
            name='client',
            field=models.ForeignKey(on_delete=django.db.models.deletion.DO_NOTHING, to='finance.company', verbose_name='Cliente'),
        ),
    ]