from django.db import models
from django.contrib.auth.models import AbstractBaseUser, PermissionsMixin, UserManager


class CustomUserManager(UserManager):
    def create_user(
        self, name=None, email=None, password=None, commit=True, **extra_fields
    ):
        email = self.normalize_email(email) if email else None
        user = self.model(name=name, email=email, **extra_fields)
        user.set_password(password)

        if commit:
            user.save(using=self._db)

        return user

    def create_superuser(self, name=None, email=None, password=None, **extra_fields):
        user = self.create_user(
            name=email, email=email, password=password, commit=False, **extra_fields
        )
        user.is_staff = True
        user.is_superuser = True
        user.save(using=self._db)

        return user


class CustomUser(AbstractBaseUser, PermissionsMixin):
    name = models.CharField(max_length=100)
    email = models.EmailField(unique=True)
    is_business = models.BooleanField(default=False)
    date_joined = models.DateTimeField(auto_now=True)
    is_staff = models.BooleanField(default=False)
    is_active = models.BooleanField(default=True)
    ACCOUNT_TYPES = ["Business", "Customer"]

    objects = CustomUserManager()
    USERNAME_FIELD = "email"

    @property
    def account_type(self):
        return "Business" if self.is_business else "Customer"

    def __str__(self):
        return f"{self.name} - {self.account_type}"

    class Meta:
        verbose_name = "User"
