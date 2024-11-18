from django.shortcuts import render
from django.urls import reverse_lazy
from django.views.generic import ListView, DetailView, CreateView, UpdateView, DeleteView

from e_motion.trainings.forms import TrainingCreateForm, TrainingEditForm
from e_motion.trainings.models import TrainingSchedule


# Create your views here.
class TrainingListView(ListView):
    model = TrainingSchedule
    template_name = 'trainings/trainings-list.html'
    context_object_name = 'trainings'


class TrainingDetailView(DetailView):
    model = TrainingSchedule
    template_name = 'trainings/training-details.html'
    context_object_name = 'training'


class TrainingCreateView(CreateView):
    model = TrainingSchedule
    form_class = TrainingCreateForm
    template_name = 'trainings/training-create.html'
    success_url = reverse_lazy('trainings-list')


class TrainingEditView(UpdateView):
    model = TrainingSchedule
    form_class = TrainingEditForm
    template_name = 'trainings/training-edit.html'

    def get_success_url(self):
        return reverse_lazy(
            'training-details',
            kwargs={
                'pk': self.object.pk,
            }
        )


class TrainingDeleteView(DeleteView):
    model = TrainingSchedule
    template_name = 'trainings/training-delete.html'
    context_object_name = 'training'
    success_url = reverse_lazy('trainings-list')

    def get_initial(self) -> dict:
        return self.get_object().__dict__