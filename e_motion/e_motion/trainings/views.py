from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin
from django.urls import reverse_lazy
from django.views.generic import ListView, DetailView, CreateView, UpdateView, DeleteView

from e_motion.trainings.forms import TrainingCreateForm, TrainingEditForm
from e_motion.trainings.models import Training


class TrainingListView(ListView):
    model = Training
    template_name = 'trainings/trainings-list.html'
    context_object_name = 'trainings'


class TrainingDetailView(DetailView):
    model = Training
    template_name = 'trainings/training-details.html'
    context_object_name = 'training'


class TrainingCreateView(LoginRequiredMixin, UserPassesTestMixin, CreateView):
    model = Training
    form_class = TrainingCreateForm
    template_name = 'trainings/training-create.html'
    success_url = reverse_lazy('trainings-list')

    def test_func(self):
        return self.request.user.has_perm("trainings.add_training")


class TrainingEditView(LoginRequiredMixin, UserPassesTestMixin, UpdateView):
    model = Training
    form_class = TrainingEditForm
    template_name = 'trainings/training-edit.html'

    def get_success_url(self):
        return reverse_lazy(
            'training-details',
            kwargs={
                'pk': self.object.pk,
            }
        )

    def test_func(self):
        return self.request.user.has_perm("trainings.change_training")


class TrainingDeleteView(LoginRequiredMixin, UserPassesTestMixin, DeleteView):
    model = Training
    template_name = 'trainings/training-delete.html'
    context_object_name = 'training'
    success_url = reverse_lazy('trainings-list')

    def get_initial(self) -> dict:
        return self.get_object().__dict__

    def test_func(self):
        return self.request.user.has_perm("trainings.delete_training")