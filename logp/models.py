from django.db import models
from django.contrib.auth.hashers import make_password
from django.contrib.auth.models import AbstractBaseUser, BaseUserManager, PermissionsMixin

class RegistrationFormManager(BaseUserManager):
    def create_user(self, email, password=None, **extra_fields):
        if not email:
            raise ValueError("Email is required")
        email = self.normalize_email(email)
        extra_fields.setdefault("is_active", True)

        user = self.model(email=email, **extra_fields)
        user.set_password(password)  
        user.save(using=self._db)
        return user

    def create_superuser(self, email, password=None, **extra_fields):
        extra_fields.setdefault("is_admin", True)
        extra_fields.setdefault("is_staff", True)  
        extra_fields.setdefault("is_superuser", True)  
        
        return self.create_user(email, password, **extra_fields)

class RegistrationForm(AbstractBaseUser, PermissionsMixin):
    user_id = models.AutoField(primary_key=True)
    fname = models.CharField(max_length=20, blank=False)
    mname = models.CharField(max_length=15, blank=True)
    lname = models.CharField(max_length=20, blank=False)
    email = models.EmailField(unique=True)
    phone = models.CharField(max_length=20, blank=False)
    password = models.CharField(max_length=255, blank=False)

    is_active = models.BooleanField(default=True)
    is_admin = models.BooleanField(default=False)
    is_staff = models.BooleanField(default=False)  

    objects = RegistrationFormManager()

    USERNAME_FIELD = "email"
    REQUIRED_FIELDS = ["fname", "lname", "phone"]

    def save(self, *args, **kwargs):
        """Hash password before saving"""
        if not self.password.startswith('pbkdf2_sha256$'):  
            self.password = make_password(self.password)
        super().save(*args, **kwargs)

    def __str__(self):
        return f"{self.user_id} - {self.email}"

    def has_perm(self, perm, obj=None):
        """Grant all permissions to admins"""
        return self.is_admin or self.is_superuser

    def has_module_perms(self, app_label):
        """Grant module permissions to admins"""
        return self.is_admin or self.is_superuser

