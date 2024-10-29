# accounts/forms.py

import re
from django import forms
from django.contrib.auth import password_validation
from django.contrib.auth.forms import SetPasswordForm
from django.utils.translation import gettext_lazy as _
from .models import Account


class LoginForm(forms.Form):
    """
    Login form for handling user login.
    """
    email = forms.EmailField()
    password = forms.CharField(widget=forms.PasswordInput)


class RegisterForm(forms.ModelForm):
    """
    User registration form with password validation.
    """
    password = forms.CharField(widget=forms.PasswordInput)
    password2 = forms.CharField(widget=forms.PasswordInput)

    class Meta:
        model = Account
        fields = ('email', 'full_name', 'account_type')

    def clean_password2(self):
        password = self.cleaned_data.get("password")
        password2 = self.cleaned_data.get("password2")
        if password and password2 and password != password2:
            raise forms.ValidationError("Passwords don't match")
        return password2

    def save(self, commit=True):
        user = super().save(commit=False)
        user.set_password(self.cleaned_data["password"])
        if commit:
            user.save()
        return user


class CustomSetPasswordForm(SetPasswordForm):
    """
    A form that lets a user set their password without entering the old password.
    """
    error_messages = {
        'password_mismatch': _("The two password fields didn't match."),
        'password_notvalid': _("Password must contain at least 8 characters, including alphanumeric characters, one special character, and one uppercase letter."),
    }
    new_password1 = forms.CharField(
        widget=forms.PasswordInput(attrs={'class': 'form-style', 'placeholder': "New Password"}),
        strip=False,
    )
    new_password2 = forms.CharField(
        widget=forms.PasswordInput(attrs={'class': 'form-style', 'placeholder': "Confirm Password"}),
        strip=False,
    )

    def clean_new_password2(self):
        password1 = self.cleaned_data.get('new_password1')
        password2 = self.cleaned_data.get('new_password2')
        if password1 and password2:
            if password1 != password2:
                raise forms.ValidationError(self.error_messages['password_mismatch'], code='password_mismatch')

            regex = re.compile(r'((?=.*\d)(?=.*[a-z])(?=.*[A-Z])(?=.*[@#$%]).{8,30})')
            if not regex.search(password1):
                raise forms.ValidationError(self.error_messages['password_notvalid'], code='password_mismatch')

        password_validation.validate_password(password2, self.user)
        return password2


class UpdateProfileForm(forms.ModelForm):
    """
    A form for updating user profiles.
    """
    class Meta:
        model = Account
        fields = ['email', 'full_name', 'account_type']

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        for field in self.fields.values():
            field.widget.attrs.update({'class': 'form-control'})
