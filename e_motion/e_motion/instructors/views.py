from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin
from django.shortcuts import redirect
from django.urls import reverse_lazy
from django.views.generic import ListView, DetailView, UpdateView, CreateView, DeleteView

from e_motion.instructors.forms import InstructorCreateForm, InstructorUpdateForm
from e_motion.instructors.models import Instructor


class InstructorListView(ListView):
    model = Instructor
    template_name = 'instructors/instructors-list.html'
    context_object_name = 'instructors'


class InstructorDetailView(DetailView):
    model = Instructor
    template_name = 'instructors/instructor-details.html'
    context_object_name = 'instructor'


class InstructorCreateView(LoginRequiredMixin, UserPassesTestMixin, CreateView):
    model = Instructor
    form_class = InstructorCreateForm
    template_name = 'instructors/instructor-create.html'
    success_url = reverse_lazy('instructors-list')

    def test_func(self):
        return self.request.user.has_perm("instructors.add_instructor")


class InstructorUpdateView(LoginRequiredMixin, UserPassesTestMixin, UpdateView):
    model = Instructor
    form_class = InstructorUpdateForm
    template_name = 'instructors/instructor-edit.html'
    context_object_name = 'instructor'

    def get_success_url(self):
        return reverse_lazy('instructor-details', kwargs={'pk': self.object.pk})

    def test_func(self):
        return self.request.user.has_perm("instructors.change_instructor")


class InstructorDeleteView(LoginRequiredMixin, UserPassesTestMixin, DeleteView):
    model = Instructor
    template_name = 'instructors/instructor-delete.html'
    context_object_name = 'instructor'
    success_url = reverse_lazy('instructors-list')

    def test_func(self):
        return self.request.user.has_perm("instructors.delete_instructor")