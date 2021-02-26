from django.db import models

class Province(models.Model):
    id = models.PositiveIntegerField('ID', primary_key=True)
    name = models.CharField('Nama', max_length=30)

    def __str__(self):
        return self.name

class Regency(models.Model):
    id = models.PositiveIntegerField('ID', primary_key=True)
    province = models.ForeignKey(Province, on_delete=models.PROTECT)
    name = models.CharField('Nama', max_length=50)

    def __str__(self):
        return self.name

class District(models.Model):
    id = models.PositiveIntegerField('ID', primary_key=True)
    regency = models.ForeignKey(Regency, on_delete=models.PROTECT)
    name = models.CharField('Nama', max_length=50)

    def __str__(self):
        return self.name

class Village(models.Model):
    id = models.PositiveIntegerField('ID', primary_key=True)
    district = models.ForeignKey(District, on_delete=models.PROTECT)
    name = models.CharField('Nama', max_length=50)

    def __str__(self):
        return self.name
