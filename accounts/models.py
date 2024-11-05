from django.contrib.auth.models import AbstractBaseUser, BaseUserManager, Group, Permission
from django.db import models
from django.core.validators import RegexValidator
from django.utils import timezone

class UserType:
    ADMINISTRATOR = 1
    COUNSELLOR = 2
    STUDENT = 3
    CHOICES = [
        (ADMINISTRATOR, 'Administrator'),
        (COUNSELLOR, 'Counsellor'),
        (STUDENT, 'Student'),
    ]
    
class MaritalStatus:
    SINGLE = 'Single'
    MARRIED = 'Married'
    DIVORCED = 'Divorced'
    WIDOWED = 'Widowed'
    CHOICES = [
        (SINGLE, 'Single'),
        (MARRIED, 'Married'),
        (DIVORCED, 'Divorced'),
        (WIDOWED, 'Widowed'),
    ]

class AccountManager(BaseUserManager):
    def create_user(self, email, full_name, account_type, password=None, **extra_fields):
        if not email:
            raise ValueError("Users must have an email address")
        email = self.normalize_email(email)
        user = self.model(
            email=email, 
            full_name=full_name, 
            account_type=account_type,
            **extra_fields
        )
        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_superuser(self, email, full_name, password=None):
        user = self.create_user(
            email=email,
            full_name=full_name,
            account_type=UserType.ADMINISTRATOR,
            password=password
        )
        user.is_superuser = True
        user.is_staff = True
        user.save(using=self._db)
        return user

class Account(AbstractBaseUser):
    # Basic Fields
    email = models.EmailField(
        unique=True,
        error_messages={
            'unique': 'A user with that email already exists.',
        }
    )
    full_name = models.CharField(max_length=255)
    account_type = models.PositiveSmallIntegerField(
        choices=UserType.CHOICES, 
        default=UserType.STUDENT
    )

    # Additional Student Fields
    student_reg_no = models.CharField(
        max_length=50, 
        unique=True, 
        null=True, 
        blank=True
    )
    course = models.CharField(
        max_length=100, 
        null=True, 
        blank=True
    )
    
    # Phone number validation
    phone_regex = RegexValidator(
    regex=r'^\+2547\d{8}$|^07\d{8}$|^01\d{8}$',
    message="Phone number must be in the format '+254712345678', '0712345678', or '0112345678'." # noqa
    )
    mobile_number = models.CharField(validators=[phone_regex], max_length=17, blank=True, null=True)
    
    year_of_study = models.PositiveSmallIntegerField(
        choices=[(i, str(i)) for i in range(1, 7)],  # 1 to 6 years
        null=True,
        blank=True
    )
    
    marital_status = models.CharField(
        max_length=20,
        choices=MaritalStatus.CHOICES,
        default=MaritalStatus.SINGLE,
        null=True,
        blank=True
    )
    
    date_of_birth = models.DateField(
        null=True,
        blank=True
    )

    # Status Fields
    is_active = models.BooleanField(default=True)
    is_counsellor = models.BooleanField(default=False)
    is_superuser = models.BooleanField(default=False)
    is_staff = models.BooleanField(default=False)
    
    # Relationships
    groups = models.ManyToManyField(Group, blank=True)
    user_permissions = models.ManyToManyField(Permission, blank=True)
    
    # Timestamps
    created_at = models.DateTimeField(default=timezone.now)
    updated_at = models.DateTimeField(auto_now=True, null=True)

    objects = AccountManager()

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ['full_name']
    
    class Meta:
        verbose_name = 'account'
        verbose_name_plural = 'accounts'

    def has_module_perms(self, app_label):
        return True
    
    @property
    def role(self):
        return UserType.CHOICES[self.account_type - 1][1]
    
    @property
    def is_student(self):
        return self.account_type == UserType.STUDENT

    def has_perm(self, perm, obj=None):
        return True

    def __str__(self):
        return f"{self.email} - {self.full_name}"
    
    def save(self, *args, **kwargs):
        # Make email lowercase before saving
        self.email = self.email.lower()
        super().save(*args, **kwargs)

