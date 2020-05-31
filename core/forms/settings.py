from django import forms
from core.models.profile import Profile


class SettingsForm(forms.ModelForm):
    class Meta:
        model = Profile
        fields = ["image"]
