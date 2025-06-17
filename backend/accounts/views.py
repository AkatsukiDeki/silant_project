from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin
from django.views.generic import UpdateView
from django.urls import reverse_lazy
from .models import User

class ProfileUpdateView(LoginRequiredMixin, UpdateView):
    model = User
    fields = ['first_name', 'last_name', 'email', 'company_name', 'phone']
    template_name = 'accounts/profile_update.html'
    success_url = reverse_lazy('home')

    def get_object(self):
        return self.request.user