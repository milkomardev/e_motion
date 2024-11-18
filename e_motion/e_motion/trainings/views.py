from django.shortcuts import render
from django.views.generic import ListView, DetailView

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

