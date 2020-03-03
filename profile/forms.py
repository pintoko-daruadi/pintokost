from django import forms

class UserCompleteNameField(forms.ModelChoiceField):
	def label_from_instance(self, obj):
		return "%s %s - %s" % (obj.first_name, obj.last_name, obj.username)
