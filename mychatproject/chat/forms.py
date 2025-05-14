from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User
from .models import Profile


class SignUpForm(UserCreationForm):
    avatar = forms.ImageField(required=False)

    class Meta:
        model = User
        fields = ('username', 'avatar', 'password1', 'password2')

    def save(self, commit=True):
        user = super().save(commit)
        avatar = self.cleaned_data.get('avatar')
        if avatar:
            profile = user.profile
            profile.avatar = avatar
            profile.save()
        return user


class ProfileForm(forms.ModelForm):
    class Meta:
        model = Profile
        fields = ['avatar']


class UserForm(forms.ModelForm):
    class Meta:
        model = User
        fields = ['first_name', 'last_name']