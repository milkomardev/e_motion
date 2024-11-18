from django import forms

from e_motion.trainings.models import TrainingSchedule


class BaseTrainingScheduleForm(forms.ModelForm):
    class Meta:
        model = TrainingSchedule
        fields = '__all__'


class TrainingCreateForm(BaseTrainingScheduleForm):
    pass


class TrainingEditForm(BaseTrainingScheduleForm):
    pass
