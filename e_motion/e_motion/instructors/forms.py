from django import forms

from e_motion.instructors.models import Instructor


class InstructorBaseForm(forms.ModelForm):
    class Meta:
        model = Instructor
        fields = ['user', 'bio']
        widgets = {
            'bio': forms.Textarea(attrs={'rows': 4, 'cols': 40}),
        }


class InstructorCreateForm(InstructorBaseForm):
    pass


class InstructorUpdateForm(InstructorBaseForm):
    class Meta:
        model = Instructor
        fields = ['bio']
        widgets = {
            'bio': forms.Textarea(attrs={'rows': 4, 'cols': 40}),
        }