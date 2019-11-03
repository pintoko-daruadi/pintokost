# Generated by Django 2.2.5 on 2019-11-03 10:51

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('person', '0007_auto_20190820_2015'),
        ('house', '0013_auto_20190813_1024'),
    ]

    operations = [
        migrations.CreateModel(
            name='ExpenseType',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=50, verbose_name='Nama Pengeluaran')),
                ('owner', models.ForeignKey(limit_choices_to={'is_owner': True}, on_delete=django.db.models.deletion.PROTECT, to='person.IdentityInfo', verbose_name='Pemilik')),
            ],
        ),
    ]
