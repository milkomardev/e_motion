from django import forms

from e_motion.trainings.models import TrainingSchedule


class BaseTrainingScheduleForm(forms.ModelForm):
    class Meta:
        model = TrainingSchedule
        fields = '__all__'


class TrainingCreateForm(BaseTrainingScheduleForm):
    class Meta:
        model = TrainingSchedule
        fields = '__all__'
        widgets = {
            'date': forms.DateTimeInput(attrs={'type': 'date'}),
        }


class TrainingEditForm(BaseTrainingScheduleForm):
    pass
