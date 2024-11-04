# accounts/forms.py

import re
from django import forms
from django.contrib.auth import password_validation
from django.contrib.auth.forms import SetPasswordForm
from django.utils.translation import gettext_lazy as _
from .models import Account, MaritalStatus


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
        fields = ('email', 'full_name')

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
    # Custom validation for mobile number
    mobile_number = forms.CharField(
        required=False,
        widget=forms.TextInput(attrs={
            'class': 'form-control',
            'placeholder': 'Mobile Number',
            'type': 'tel'
        })
    )

    # Custom date input
    date_of_birth = forms.DateField(
        required=False,
        widget=forms.DateInput(attrs={
            'class': 'form-control',
            'type': 'date'
        })
    )

    # Year of study as select field
    year_of_study = forms.ChoiceField(
        choices=[(i, str(i)) for i in range(1, 7)],
        required=False,
        widget=forms.Select(attrs={'class': 'form-control'})
    )

    # Marital status as select field
    marital_status = forms.ChoiceField(
        choices=MaritalStatus.CHOICES,
        required=False,
        widget=forms.Select(attrs={'class': 'form-control'})
    )

    class Meta:
        model = Account
        fields = [
            'email',
            'full_name',
            'student_reg_no',
            'course',
            'mobile_number',
            'year_of_study',
            'marital_status',
            'date_of_birth'
        ]
        widgets = {
            'email': forms.EmailInput(attrs={
                'class': 'form-control',
                'placeholder': 'Email'
            }),
            'full_name': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'Full Name'
            }),
            'student_reg_no': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'Student ID'
            }),
            'course': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'Course'
            }),
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        # Make email read-only if it's an existing user
        if self.instance and self.instance.pk:
            self.fields['email'].widget.attrs['readonly'] = True

        # Add any custom validation messages
        self.fields['mobile_number'].error_messages = {
            'invalid': 'Please enter a valid mobile number.'
        }

    def clean_mobile_number(self):
        """Custom validation for mobile number"""
        mobile_number = self.cleaned_data.get('mobile_number')
        if mobile_number:
            # Remove any spaces or special characters except '+'
            mobile_number = ''.join(c for c in mobile_number if c.isdigit() or c == '+')
            # Validate number format
            if not mobile_number.startswith('+'):
                mobile_number = '+' + mobile_number
        return mobile_number

    def clean_email(self):
        """Prevent email changes for existing users"""
        email = self.cleaned_data.get('email')
        if self.instance and self.instance.pk:
            return self.instance.email
        return email

    def save(self, commit=True):
        user = super().save(commit=False)
        if commit:
            user.save()
        return user