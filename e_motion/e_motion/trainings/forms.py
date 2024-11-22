from django import forms

from e_motion.trainings.models import Training


class BaseTrainingScheduleForm(forms.ModelForm):
    class Meta:
        model = Training
        fields = '__all__'


class TrainingCreateForm(BaseTrainingScheduleForm):
    class Meta:
        model = Training
        fields = '__all__'
        widgets = {
            'date': forms.DateTimeInput(attrs={'type': 'date'}),
        }


class TrainingEditForm(BaseTrainingScheduleForm):
    pass
