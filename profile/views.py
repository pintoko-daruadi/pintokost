from django.contrib.auth.mixins import LoginRequiredMixin, PermissionRequiredMixin, UserPassesTestMixin
from django.urls import reverse_lazy
from django.views.generic.edit import CreateView, FormView
from .forms import LandlordSignupForm, RenterForm

class LandlordSignupView(UserPassesTestMixin, CreateView):
	form_class = LandlordSignupForm
	template_name = 'profile/landlord_signup.html'
	success_url = reverse_lazy('house:list')

	def test_func(self):
		return self.request.user.is_authenticated == False

class ProfileCreateView(LoginRequiredMixin, PermissionRequiredMixin, CreateView):
	permission_required = 'auth.add_user'
	form_class = RenterForm
	success_url = reverse_lazy('house:list')
	template_name = 'profile/profile_form.html'
