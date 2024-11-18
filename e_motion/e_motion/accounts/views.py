from django.contrib.auth import get_user_model, login, logout
from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin
from django.contrib.auth.models import User
from django.shortcuts import get_object_or_404, redirect, render
from django.urls import reverse_lazy
from django.views import View
from django.views.generic import CreateView, DetailView, UpdateView, DeleteView

from e_motion.accounts.forms import AppUserCreationForm, ProfileEditForm
from e_motion.accounts.models import Profile

UserModel = get_user_model()


class UserRegisterView(CreateView):
    model = UserModel
    form_class = AppUserCreationForm
    template_name = 'registration/register.html'
    success_url = reverse_lazy('home')

    def form_valid(self, form):
        response = super().form_valid(form)

        # Determine the backend for the user
        backend = 'e_motion.accounts.authentication.EmailOrUsernameBackend'
        if hasattr(self.object, 'backend'):
            backend = self.object.backend  # If the user model already has a backend attribute

        # Log the user in with the specified backend
        login(self.request, self.object, backend=backend)
        return response


class ProfileDetailsView(LoginRequiredMixin, DetailView):
    model = Profile
    template_name = 'account/profile-details.html'
    context_object_name = 'profile'

    def get_object(self, queryset=None):
        pk = self.kwargs.get('pk')
        return get_object_or_404(Profile, pk=pk)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        profile = self.object

        context['next_training'] = profile.next_training()
        context['attended_trainings'] = profile.attended_trainings.all()

        return context


class ProfileEditView(LoginRequiredMixin, UserPassesTestMixin, UpdateView):
    model = Profile
    template_name = 'account/profile-edit.html'
    context_object_name = 'profile'
    form_class = ProfileEditForm

    def test_func(self):
        profile = get_object_or_404(Profile, pk=self.kwargs['pk'])
        return self.request.user == profile.user

    def get_form_kwargs(self):
        kwargs = super().get_form_kwargs()
        kwargs['user'] = self.object.user
        return kwargs

    def get_success_url(self):
        return reverse_lazy(
            'profile-details',
            kwargs={
                'pk': self.object.pk,
            }
        )


class ProfileDeleteView(LoginRequiredMixin, UserPassesTestMixin, View):
    template_name = 'account/profile-delete.html'
    success_url = reverse_lazy('home')

    def get(self, request, *args, **kwargs):
        profile = get_object_or_404(Profile, pk=self.kwargs.get('pk'))
        return render(request, self.template_name, {'profile': profile})

    def post(self, request, *args, **kwargs):
        profile = get_object_or_404(Profile, pk=self.kwargs.get('pk'))
        user = profile.user

        logout(request)
        request.session.flush()

        profile.delete()
        user.delete()

        return redirect(self.success_url)

    def test_func(self):
        profile = get_object_or_404(Profile, pk=self.kwargs.get('pk'))
        return self.request.user == profile.user