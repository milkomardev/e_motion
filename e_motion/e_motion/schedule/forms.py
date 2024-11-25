from django import forms
from .choices import DurationChoices
from .models import Schedule


class ScheduleBaseForm(forms.ModelForm):
    duration = forms.ChoiceField(
        choices=DurationChoices.choices,
        widget=forms.Select(attrs={'class': 'form-control'}),
    )

    class Meta:
        model = Schedule
        fields = ['training', 'date', 'duration', 'max_attendees']
        widgets = {
            'date': forms.DateTimeInput(attrs={'type': 'datetime-local'}),
        }


class ScheduleCreateForm(ScheduleBaseForm):
    pass


class ScheduleUpdateForm(ScheduleBaseForm):
    pass

