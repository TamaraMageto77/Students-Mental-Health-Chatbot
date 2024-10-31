from django.contrib.auth.models import AbstractBaseUser, BaseUserManager, Group, Permission
from django.db import models
class UserType:
    ADMINISTRATOR = 1
    COUNSELLOR = 2
    STUDENT = 3
    CHOICES = [
        (ADMINISTRATOR, 'Administrator'),
        (COUNSELLOR, 'Counsellor'),
        (STUDENT, 'Student'),
    ]

class AccountManager(BaseUserManager):
    def create_user(self, email, full_name, account_type, password=None):
        if not email:
            raise ValueError("Users must have an email address")
        email = self.normalize_email(email)
        user = self.model(email=email, full_name=full_name, account_type=account_type)
        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_superuser(self, email, full_name, password=None):
        user = self.create_user(email=email, full_name=full_name, account_type=UserType.ADMINISTRATOR, password=password)
        user.is_superuser = True
        user.is_staff = True
        user.save(using=self._db)
        return user

class Account(AbstractBaseUser):
    email = models.EmailField(unique=True)
    full_name = models.CharField(max_length=255)
    account_type = models.PositiveSmallIntegerField(choices=UserType.CHOICES, default=UserType.STUDENT)
    is_active = models.BooleanField(default=True)
    is_counsellor = models.BooleanField(default=False)
    is_superuser = models.BooleanField(default=False)
    is_staff = models.BooleanField(default=False)
    groups = models.ManyToManyField(Group, blank=True)
    user_permissions = models.ManyToManyField(Permission, blank=True)
    created_at = models.DateTimeField(auto_now_add=True,null=True)

    objects = AccountManager()

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ['full_name']
    
    def has_module_perms(self, app_label):
        """
        Return True if the user has any permissions in the given app label.
        """
        return True
    
    @property
    def role(self):
        return UserType.CHOICES[self.account_type - 1][1]

    def has_perm(self, perm, obj=None):
        """
        Return True if the user has the specified permission.
        """
        return True

    def __str__(self):
        return self.email

