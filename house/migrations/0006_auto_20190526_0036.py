# Generated by Django 2.1.7 on 2019-05-25 17:36

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('house', '0005_auto_20190526_0034'),
    ]

    operations = [
        migrations.AlterField(
            model_name='rent',
            name='renter',
            field=models.PositiveIntegerField(),
        ),
    ]
