from django.contrib.auth import get_user_model, login, logout
from django.contrib.auth.decorators import login_required
from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin
from django.contrib.auth.models import Group
from django.db.models import Q
from django.http import HttpResponseRedirect
from django.shortcuts import get_object_or_404, redirect, render
from django.urls import reverse_lazy, reverse
from django.views import View
from django.views.generic import CreateView, DetailView, UpdateView, ListView
from rest_framework import status, generics
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.views import APIView

from e_motion.accounts.forms import AppUserCreationForm, ProfileEditForm
from e_motion.accounts.models import Profile
from e_motion.accounts.permissions import IsModerator
from e_motion.accounts.serializers import ProfileSerializer

UserModel = get_user_model()


class UserRegisterView(CreateView):
    model = UserModel
    form_class = AppUserCreationForm
    template_name = 'registration/register.html'
    success_url = reverse_lazy('home')

    def form_valid(self, form):
        response = super().form_valid(form)

        backend = 'e_motion.accounts.authentication.EmailOrUsernameBackend'
        if hasattr(self.object, 'backend'):
            backend = self.object.backend

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
        profile = get_object_or_404(Profile, pk=self.kwargs.get('pk'))
        return (self.request.user == profile.user or
                self.request.user.has_perm("accounts.change_profile"))

    def get_form_kwargs(self):
        kwargs = super().get_form_kwargs()
        kwargs['user'] = self.request.user
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
        return (self.request.user == profile.user or
                self.request.user.has_perm("accounts.delete_profile"))


class ReceptionistStudentsListView(LoginRequiredMixin, UserPassesTestMixin, ListView):
    model = Profile
    template_name = 'account/students-list.html'
    context_object_name = 'students'
    paginate_by = 1  # TODO Change this to 10 after testing

    def test_func(self):
        return self.request.user.groups.filter(name__in=["Receptionist"]).exists()

    def get_queryset(self):
        query = self.request.GET.get("q", "")
        moderator_group = Group.objects.get(name="Moderator")
        receptionist_group = Group.objects.get(name="Receptionist")
        queryset = Profile.objects.exclude(
            user__groups__in=[moderator_group, receptionist_group],

        )
        if query:
            queryset = queryset.filter(
                Q(user__first_name__icontains=query)
                | Q(user__last_name__icontains=query)
                | Q(user__email__icontains=query)
            )

        return queryset.order_by("user__first_name", "user__last_name")

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        queryset = self.get_queryset()
        paginator = self.paginator_class(queryset, self.paginate_by)
        page = self.request.GET.get('page') or 1
        paginated_students = paginator.get_page(page)
        context['students'] = paginated_students
        return context


class ModeratorStudentsListCreateAPIView(generics.ListCreateAPIView):
    """
    List all students or create a new student (GET, POST).
    """
    permission_classes = [IsAuthenticated, IsModerator]
    serializer_class = ProfileSerializer

    def get_queryset(self):
        return Profile.objects.exclude(
            user__groups__name__in=["Moderator", "Receptionist"]
        )


class ModeratorStudentDetailAPIView(generics.RetrieveUpdateDestroyAPIView):
    """
    Retrieve, update, or delete a specific student (GET, PUT, DELETE).
    """
    permission_classes = [IsAuthenticated, IsModerator]
    serializer_class = ProfileSerializer
    lookup_field = "pk"

    def get_queryset(self):
        return Profile.objects.exclude(
            user__groups__name__in=["Moderator", "Receptionist"]
        )


@login_required
def students_router_view(request):
    if request.user.groups.filter(name="Moderator").exists():
        return redirect("moderator-students-api")
    elif request.user.groups.filter(name="Receptionist").exists():
        return redirect("receptionist-students-list")
    else:
        return redirect("home")
