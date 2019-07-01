# Generated by Django 2.1.7 on 2019-05-25 17:28

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('house', '0002_auto_20190526_0027'),
    ]

    operations = [
        migrations.AlterField(
            model_name='house',
            name='owner',
            field=models.ForeignKey(limit_choices_to={'is_owner': True}, on_delete=django.db.models.deletion.PROTECT, to='person.IdentityInfo'),
        ),
        migrations.AlterField(
            model_name='rent',
            name='renter',
            field=models.ForeignKey(on_delete=django.db.models.deletion.PROTECT, to='person.IdentityInfo', verbose_name='Penyewa'),
        ),
    ]
