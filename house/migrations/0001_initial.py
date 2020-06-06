# Generated by Django 2.2.5 on 2020-06-06 04:00

import datetime
from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion
import house.models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='House',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=50, verbose_name='Nama')),
                ('address', models.CharField(max_length=300, verbose_name='Alamat')),
                ('pln_number', models.CharField(max_length=20, verbose_name='Nomor PLN')),
                ('owner', models.ForeignKey(limit_choices_to={'groups__name': 'owner'}, on_delete=django.db.models.deletion.PROTECT, to=settings.AUTH_USER_MODEL)),
            ],
        ),
        migrations.CreateModel(
            name='Rent',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('price', models.DecimalField(decimal_places=2, max_digits=12, verbose_name='Harga')),
                ('billing_date', models.DateField(default=None, verbose_name='Tanggal Tagihan')),
                ('active', models.BooleanField(default=True, verbose_name='Status Sewa')),
                ('start_date', models.DateField(default=datetime.date.today, help_text='Format: YYYY-MM-DD', verbose_name='Awal Masuk')),
                ('house', models.ForeignKey(on_delete=django.db.models.deletion.PROTECT, to='house.House', verbose_name='Rumah')),
                ('renter', models.ForeignKey(limit_choices_to={'groups__name': 'renter'}, on_delete=django.db.models.deletion.PROTECT, to=settings.AUTH_USER_MODEL, verbose_name='Penyewa')),
            ],
        ),
        migrations.CreateModel(
            name='Payment',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('price', models.DecimalField(decimal_places=2, default=0, max_digits=12, verbose_name='Harga')),
                ('pay_date', models.DateField(default=None, help_text='Format: YYYY-MM-DD', verbose_name='Tanggal Bayar')),
                ('start', models.DateField(default=None, help_text='Format: YYYY-MM-DD', verbose_name='Mulai Sewa')),
                ('rent', models.ForeignKey(on_delete=django.db.models.deletion.PROTECT, to='house.Rent')),
            ],
        ),
        migrations.CreateModel(
            name='ExpenseType',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=50, verbose_name='Tipe Pengeluaran')),
                ('owner', models.ForeignKey(limit_choices_to={'groups__name': 'owner'}, on_delete=django.db.models.deletion.PROTECT, to=settings.AUTH_USER_MODEL, verbose_name='Pemilik Rumah')),
            ],
        ),
        migrations.CreateModel(
            name='Expense',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('nominal', models.PositiveIntegerField(verbose_name='Biaya Pengeluaran')),
                ('date', models.DateField(verbose_name='Tanggal')),
                ('remark', models.CharField(max_length=200, verbose_name='Catatan')),
                ('receipt_photo', models.FileField(blank=True, null=True, upload_to=house.models.expense_path)),
                ('expense_type', models.ForeignKey(default=1, on_delete=django.db.models.deletion.PROTECT, to='house.ExpenseType')),
                ('house', models.ForeignKey(on_delete=django.db.models.deletion.PROTECT, to='house.House')),
            ],
        ),
    ]
