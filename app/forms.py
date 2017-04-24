from django.contrib.auth import get_user_model
from django import forms
from django.forms.forms import NON_FIELD_ERRORS
from django.forms import ModelForm
from . import models

class LoginForm(forms.Form):
    username = forms.CharField(
        label="username",
        max_length=128
    )
    password = forms.CharField(
        label="password",
        max_length=128,
        widget=forms.PasswordInput()
    )


class PasswordForm(forms.Form):
    password = forms.CharField(max_length=128, widget=forms.PasswordInput(), label="Enter password")
    password2 = forms.CharField(max_length=128, widget=forms.PasswordInput(), label="Enter password (again)")

    def clean_password2(self):
        password = self.cleaned_data.get('password', '')
        password2 = self.cleaned_data['password2']
        if password != password2:
            raise forms.ValidationError("Confirmation password doesn't match.")
        return password2


class SignupForm(PasswordForm):
    username = forms.CharField(
        label="username",
        max_length=30,
        required=True
    )
    first_name = forms.CharField(
        label="first name",
        max_length=30,
        required=True
    )
    last_name = forms.CharField(
        label="last name",
        max_length=30,
        required=True
    )
    email = forms.EmailField(
        label="email",
        max_length=255,
        required=True
    )


class UserProfileForm(ModelForm):
    class Meta:
        model = get_user_model()
        fields = ['first_name', 'last_name', 'email', 'last_location']
        widgets = {
            'last_location': forms.HiddenInput()
        }

