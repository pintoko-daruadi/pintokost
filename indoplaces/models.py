from django.db import models

class Province(models.Model):
    name = models.CharField('Nama', max_length=30)

    class Meta:
        ordering=['id']

    def __str__(self):
        return self.name

class Regency(models.Model):
    province = models.ForeignKey(Province, on_delete=models.PROTECT)
    name = models.CharField('Nama', max_length=50)

    class Meta:
        ordering=['id']

    def __str__(self):
        return self.name

class District(models.Model):
    regency = models.ForeignKey(Regency, on_delete=models.PROTECT)
    name = models.CharField('Nama', max_length=50)

    class Meta:
        ordering=['id']

    def __str__(self):
        return self.name

class Village(models.Model):
    district = models.ForeignKey(District, on_delete=models.PROTECT)
    name = models.CharField('Nama', max_length=50)

    class Meta:
        ordering=['id']

    def __str__(self):
        return self.name
