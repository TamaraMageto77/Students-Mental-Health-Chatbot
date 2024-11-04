# accounts/forms.py

import re
from django import forms
from django.contrib.auth import password_validation
from django.contrib.auth.forms import SetPasswordForm
from django.utils.translation import gettext_lazy as _
from .models import Account, MaritalStatus
from django.core.exceptions import ValidationError


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
    A form for updating user profiles with proper validation and field customization.
    """
    # Custom field definitions with appropriate widgets and validation
    full_name = forms.CharField(
        required=True,
        widget=forms.TextInput(attrs={
            'class': 'form-control',
            'placeholder': 'Full Name'
        })
    )
    
    mobile_number = forms.CharField(
        required=False,
        widget=forms.TextInput(attrs={
            'class': 'form-control',
            'placeholder': '0712345678 or +254712345678',
            'type': 'tel'
        })
    )

    date_of_birth = forms.DateField(
        required=False,
        widget=forms.DateInput(attrs={
            'class': 'form-control',
            'type': 'date'
        })
    )

    year_of_study = forms.ChoiceField(
        choices=[(None, '----')] + [(i, str(i)) for i in range(1, 7)],
        required=False,
        widget=forms.Select(attrs={
            'class': 'form-control'
        })
    )

    marital_status = forms.ChoiceField(
        choices=[(None, '----')] + list(MaritalStatus.CHOICES),
        required=False,
        widget=forms.Select(attrs={
            'class': 'form-control'
        })
    )

    student_reg_no = forms.CharField(
        required=False,
        widget=forms.TextInput(attrs={
            'class': 'form-control',
            'placeholder': 'Student Registration Number'
        })
    )

    course = forms.CharField(
        required=False,
        widget=forms.TextInput(attrs={
            'class': 'form-control',
            'placeholder': 'Course Name'
        })
    )

    class Meta:
        model = Account
        fields = [
            'full_name',
            'student_reg_no',
            'course',
            'mobile_number',
            'year_of_study',
            'marital_status',
            'date_of_birth'
        ]
    def __init__(self, *args, **kwargs):
            user = kwargs.pop('user', None)  # Pass user
            print(user)
            super().__init__(*args, **kwargs)
            
            # If the user is a student, remove all fields except 'full_name' and 'email'
            if user and user.role == 3:
                allowed_fields = {'full_name'}
                self.fields = {key: value for key, value in self.fields.items() if key in allowed_fields}

    def clean_mobile_number(self):
        """
        Validates and formats the mobile number according to the required patterns:
        - +254712345678 (international format)
        - 0712345678 (local format)
        - 0112345678 (local format)
        """
        mobile_number = self.cleaned_data.get('mobile_number')
        if not mobile_number:
            return None
            
        # Remove any spaces or non-numeric characters except '+'
        mobile_number = ''.join(c for c in mobile_number if c.isdigit() or c == '+')
        
        # Format acceptable mobile number formats
        if mobile_number.startswith('07') and len(mobile_number) == 10:
            mobile_number = '+254' + mobile_number[1:]
        elif mobile_number.startswith('01') and len(mobile_number) == 10:
            mobile_number = '+254' + mobile_number[1:]
        elif not mobile_number.startswith('+254') or len(mobile_number) != 13:
            raise ValidationError(
                "Please enter a valid mobile number in the format '+254712345678', '0712345678', or '0112345678'."
            )
        return mobile_number

    def clean_year_of_study(self):
        """
        Converts year_of_study to integer or None if not provided
        """
        year = self.cleaned_data.get('year_of_study')
        if year:
            try:
                return int(year)
            except (ValueError, TypeError):
                raise ValidationError("Invalid year of study")
        return None

    def clean_student_reg_no(self):
        """
        Validates student registration number format and uniqueness
        """
        reg_no = self.cleaned_data.get('student_reg_no')
        if reg_no:
            # Check if reg_no exists for another user
            existing = Account.objects.filter(student_reg_no=reg_no).exclude(pk=self.instance.pk if self.instance else None)
            if existing.exists():
                raise ValidationError("This registration number is already in use.")
        return reg_no

    def clean(self):
        """
        Cross-field validation if needed
        """
        cleaned_data = super().clean()
        
        # Example: If user is a student, require registration number
        if self.instance.account_type == 1:  # Assuming 1 is student type
            if not cleaned_data.get('student_reg_no'):
                self.add_error('student_reg_no', 'Student registration number is required for students.')
        
        return cleaned_data

    def save(self, commit=True):
        """
        Custom save method to handle any special processing before saving
        """
        user = super().save(commit=False)
        
        if commit:
            user.save()
        
        return user