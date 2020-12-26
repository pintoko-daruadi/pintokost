from django.contrib.auth.mixins import LoginRequiredMixin, PermissionRequiredMixin
from django.contrib.auth.models import User, Group
from django.contrib import messages
from django.shortcuts import render
from django.urls import reverse_lazy
from django.views.generic.edit import FormView
from .forms import RenterForm
from .models import Profile
import time

class ProfileCreateView(LoginRequiredMixin, PermissionRequiredMixin, FormView):
	permission_required = 'auth.add_user'
	form_class = RenterForm
	model = Profile
	success_url = reverse_lazy('house:list')
	template_name = 'profile/profile_form.html'

	def form_valid(self, form):
		timestamp = int(time.time())
		first_name = form.cleaned_data.get('first_name')
		last_name = form.cleaned_data.get('last_name')
		username = first_name[:1] + last_name + str(timestamp)
		user = User.objects.create_user(username=username.lower(), first_name=first_name, last_name=last_name)
		renter_group, created = Group.objects.get_or_create(name = 'renter')
		user.groups.add(renter_group)
		user.save()
		user.profile.nik = form.cleaned_data.get('nik')
		user.profile.occupation = form.cleaned_data.get('occupation')
		user.profile.phone = form.cleaned_data.get('phone')
		user.profile.save()
		messages.success(self.request, "Pengguna {} berhasil ditambah".format(first_name))
		return super(ProfileCreateView, self).form_valid(form)
