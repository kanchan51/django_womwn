from django import forms
from django.contrib.auth.models import User
from django.contrib.auth.forms import UserCreationForm
from .models import Profile


class UserRegisterForm(UserCreationForm):
    email = forms.EmailField()
    

    class Meta:
        model = User
        fields = ['username', 'first_name','last_name','email', 'password1', 'password2']


class UserUpdateForm(forms.ModelForm):
    email = forms.EmailField()
    contact=forms.IntegerField(max_value=10)

    class Meta:
        model = User

        fields = ['username', 'first_name','last_name', 'email','contact']


class ProfileUpdateForm(forms.ModelForm):
    class Meta:
        model = Profile
        fields = ['image',]
