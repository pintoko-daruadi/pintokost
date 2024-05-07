import os
import re
from django.db import models
from django.contrib.auth.models import User
from house.models import House
from pintokost.helpers import toRupiah

def expense_path(instance, filename):
	basefilename, file_extension= os.path.splitext(filename)
	new_filename = "{}_{}" % (instance.house, instance.expense_type)
	new_filename = re.sub('[^A-Za-z]', '_', new_filename)
	return 'expense/%Y/%m/%d/{filename}{ext}'.format(filename=new_filename, ext= file_extension)

class ExpenseType(models.Model):
	name = models.CharField(max_length=50)
	owner = models.ForeignKey(
		User,
		on_delete=models.PROTECT,
		limit_choices_to={'groups__name': 'owner'}
	)
	def __str__(self):
		return self.name

class Expense(models.Model):
	house = models.ForeignKey(House, on_delete=models.PROTECT)
	nominal = models.PositiveIntegerField()
	date = models.DateField()
	expense_type = models.ForeignKey(ExpenseType, on_delete=models.PROTECT, default=1)
	remark = models.CharField('Catatan', max_length=200)
	receipt_photo = models.FileField(blank=True, null=True, upload_to=expense_path)

	def __str__(self):
		return "%s <%s> (%s)" % (self.expense_type, toRupiah(self.nominal), self.house)

	def monthly_outcome(owner, year, month):
		qs = Expense.objects.filter(
			house__owner=owner,
			date__year=year,
			date__month=month,
		).aggregate(models.Sum('nominal'))

		return int(qs['nominal__sum'] or 0)
