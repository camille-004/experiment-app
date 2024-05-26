from django import forms
from django.contrib.auth.models import User

from .models import UserProfile


class ProfileForm(forms.ModelForm):
    class Meta:
        model = User
        fields = ["username", "first_name", "last_name", "email"]


class UserProfileForm(forms.ModelForm):
    class Meta:
        model = UserProfile
        fields = ["organization", "location"]


class ProfilePictureForm(forms.ModelForm):
    class Meta:
        model = UserProfile
        fields = ["profile_picture"]
