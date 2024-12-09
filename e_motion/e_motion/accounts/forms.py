from datetime import timedelta

from django import forms
from django.contrib.auth import get_user_model
from django.contrib.auth.forms import UserChangeForm, UserCreationForm
from e_motion.accounts.models import Profile

UserModel = get_user_model()


class AppUserCreationForm(UserCreationForm):
    class Meta(UserCreationForm.Meta):
        model = UserModel
        fields = ('username', 'email', 'first_name', 'last_name')
        help_texts = {
            'username': None,
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['password1'].help_text = None
        self.fields['password2'].help_text = None


class AppUserChangeForm(UserChangeForm):
    class Meta(UserChangeForm.Meta):
        model = UserModel
        fields = ('username', 'email')


class ProfileEditForm(forms.ModelForm):
    email = forms.EmailField(required=True)
    first_name = forms.CharField(max_length=150, required=True)
    last_name = forms.CharField(max_length=150, required=True)

    class Meta:
        model = Profile
        fields = (
            'phone_number',
            'date_of_birth',
            'profile_picture',
            'subscription_plan',
            'subscription_start_date',
            'attendance_count',
        )
        widgets = {
            'date_of_birth': forms.DateInput(attrs={'type': 'date'}),
            'subscription_start_date': forms.DateInput(attrs={'type': 'date'}),
        }

    def __init__(self, *args, **kwargs):
        user = kwargs.pop('user', None)
        profile = kwargs.get('instance')
        super().__init__(*args, **kwargs)

        if not (user.has_perm("accounts.change_profile") and not user.has_perm("accounts.change_user")):
            self.fields.pop('subscription_plan')
            self.fields.pop('subscription_start_date')
            self.fields.pop('attendance_count')

        if profile:
            self.fields['email'].initial = profile.user.email
            self.fields['first_name'].initial = profile.user.first_name
            self.fields['last_name'].initial = profile.user.last_name

    def save(self, commit=True):
        profile = super().save(commit=False)

        if profile.subscription_plan and profile.subscription_start_date:
            duration = timedelta(days=30 * profile.subscription_plan.duration_months)
            profile.subscription_end_date = profile.subscription_start_date + duration

        user = profile.user

        user.email = self.cleaned_data['email']
        user.first_name = self.cleaned_data['first_name']
        user.last_name = self.cleaned_data['last_name']

        if commit:
            user.save()
            profile.save()

        return profile
